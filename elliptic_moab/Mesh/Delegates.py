from elliptic.Kernel.MeshComputeInterface.BackendBuilder import ContextType, ContextDelegate


class MoabDelegate(ContextDelegate):

    last_id: int = 0

    def __init__(self, context) -> None:
        super().__init__(context)

        self.unique_id = MoabDelegate.last_id
        MoabDelegate.last_id += 1


class BaseDelegate(MoabDelegate):

    def get_template_file(self):
        return 'base.pyx.etp'

    def template_kwargs(self):
        return {'declare_entityhandles': self.context['declare_entityhandle'],
                'declare_ranges': self.context['declare_range'],
                'declare_indexes': self.context['declare_index'],
                'declare_variables': self.context['declare_variable']}

    def context_enter(self):
        pass

    def context_exit(self):
        pass


class LoopDelegate(MoabDelegate):

    def __init__(self, context, loop_name):
        super().__init__(context)

        self.loop_var_prefix = loop_name + str(self.unique_id)

    def template_kwargs(self):
        return {'current_entity': self.get_value('current_entity_name'),
                'current_range': self.get_value('current_range_name'),
                'current_index': self.get_value('current_index_name'),
                'reduced_variables': self.context[self.loop_var_prefix + 'reduced'],
                'mapped_variables': self.context[self.loop_var_prefix + 'mapped'],
                'reduce_nested_children': self.context[self.loop_var_prefix + 'nested_children']}

    def context_enter(self):
        self.put_value('current_loop', self.loop_var_prefix)

        self.put_value('declare_range', self.loop_var_prefix + 'range')
        self.put_value('current_range_name', self.loop_var_prefix + 'range')

        self.put_value('declare_entityhandle', self.loop_var_prefix + 'entity')
        self.put_value('current_entity_name', self.loop_var_prefix + 'entity')

        self.put_value('declare_index', self.loop_var_prefix + 'index')
        self.put_value('current_index_name', self.loop_var_prefix + 'index')

    def context_exit(self):
        self.pop_value('current_range_name')
        self.pop_value('current_entity_name')
        self.pop_value('current_index_name')


class ByEntDelegate(LoopDelegate):

    def __init__(self, context, dim):
        super().__init__(context, 'by_ent')
        self.dim = dim

    def get_template_file(self):
        return 'Selector/by_ent.pyx.etp'

    def template_kwargs(self):
        return {'dim': self.dim,
                **super().template_kwargs()}


class ByAdjDelegate(LoopDelegate):

    def __init__(self, context, bridge_dim, to_dim):
        super().__init__(context, 'by_adj')
        self.bridge_dim = bridge_dim
        self.to_dim = to_dim

    def get_template_file(self):
        return 'Selector/by_adj.pyx.etp'

    def template_kwargs(self):
        return {'bridge_dim': self.bridge_dim,
                'to_dim': self.to_dim,
                'old_entity': self.context['current_entity_name'][-2],
                **super().template_kwargs()}


class MapDelegate(MoabDelegate):

    def __init__(self, context, mapping_function, fargs):
        super().__init__(context)
        self.mapping_function = mapping_function
        self.fargs = fargs

    def get_template_file(self):
        return 'Computer/map.pyx.etp'

    def template_kwargs(self):
        return {'map_function': self.mapping_function.name,
                'map_args': self.fargs,
                'current_entity': self.get_value('current_entity_name'),
                'current_variable': self.get_value('current_variable')}

    def context_enter(self):
        self.current_loop = self.get_value('current_loop')

        self.put_value('declare_variable', 'map_var' + str(self.unique_id))
        self.put_value(self.current_loop + 'mapped', 'reduce_var' + str(self.unique_id))
        self.put_value('current_variable', 'map_var' + str(self.unique_id))

    def context_exit(self):
        self.pop_value('current_variable')


class ReduceDelegate(MoabDelegate):

    def __init__(self, context, reducing_function, fargs):
        super().__init__(context)
        self.reducing_function = reducing_function
        self.fargs = fargs
        self.current_loop = ""

    def get_template_file(self):
        return 'Computer/reduce.pyx.etp'

    def template_kwargs(self):
        return {'reduce_function': self.reducing_function.name,
                'reduce_args': self.fargs,
                'current_variable': self.context['current_variable'][-2],
                'reduced_variable': self.get_value('current_variable')}

    def context_enter(self):
        self.current_loop = self.get_value('current_loop')

        self.put_value('declare_variable', 'reduce_var' + str(self.unique_id))
        self.put_value(self.current_loop + 'reduced', 'reduce_var' + str(self.unique_id))
        self.put_value('current_variable', 'reduce_var' + str(self.unique_id))

        # For nested reduces:
        self.pop_value('current_loop')

    def context_exit(self):
        self.pop_value('current_variable')

        # For other reduces in the same loop level:
        self.put_value('current_loop', self.current_loop)
        self.put_value(self.current_loop + 'nested_children', self.child)

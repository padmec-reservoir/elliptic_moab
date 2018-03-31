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
                'declare_indexes': self.context['declare_index']}

    def context_enter(self):
        pass

    def context_exit(self):
        pass


class ByEntDelegate(MoabDelegate):

    def __init__(self, context, dim):
        super().__init__(context)
        self.dim = dim

    def get_template_file(self):
        return 'Selector/by_ent.pyx.etp'

    def template_kwargs(self):
        return {'dim': self.get_value('current_entity_dim'),
                'current_entity': self.get_value('current_entity_name'),
                'current_range': self.get_value('current_range_name'),
                'current_index': self.get_value('current_index_name')}

    def context_enter(self):
        self.put_value('current_entity_dim', str(self.dim))

        self.put_value('declare_range', 'by_ent_range' + str(self.unique_id))
        self.put_value('current_range_name', 'by_ent_range' + str(self.unique_id))

        self.put_value('declare_entityhandle', 'by_ent_entity' + str(self.unique_id))
        self.put_value('current_entity_name', 'by_ent_entity' + str(self.unique_id))

        self.put_value('declare_index', 'by_ent_index' + str(self.unique_id))
        self.put_value('current_index_name', 'by_ent_index' + str(self.unique_id))

    def context_exit(self):
        self.pop_value('current_entity_dim')
        self.pop_value('current_range_name')
        self.pop_value('current_entity_name')
        self.pop_value('current_index_name')


class ByAdjDelegate(MoabDelegate):

    def __init__(self, context, bridge_dim, to_dim):
        super().__init__(context)
        self.bridge_dim = bridge_dim
        self.to_dim = to_dim

    def get_template_file(self):
        return 'Selector/by_adj.pyx.etp'

    def template_kwargs(self):
        return {'bridge_dim': self.bridge_dim,
                'to_dim': self.to_dim,
                'old_entity': self.context['current_entity_name'][-2],
                'current_entity': self.get_value('current_entity_name'),
                'current_range': self.get_value('current_range_name'),
                'current_index': self.get_value('current_index_name')}

    def context_enter(self):
        self.put_value('current_entity_dim', str(self.to_dim))

        self.put_value('declare_range', 'by_adj_range' + str(self.unique_id))
        self.put_value('current_range_name', 'by_adj_range' + str(self.unique_id))

        self.put_value('declare_entityhandle', 'by_adj_entity' + str(self.unique_id))
        self.put_value('current_entity_name', 'by_adj_entity' + str(self.unique_id))

        self.put_value('declare_index', 'by_adj_index' + str(self.unique_id))
        self.put_value('current_index_name', 'by_adj_index' + str(self.unique_id))

    def context_exit(self):
        self.pop_value('current_entity_dim')
        self.pop_value('current_range_name')
        self.pop_value('current_entity_name')
        self.pop_value('current_index_name')


class MapDelegate(MoabDelegate):
    pass
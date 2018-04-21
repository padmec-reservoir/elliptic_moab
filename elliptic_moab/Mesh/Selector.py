from typing import Type

from elliptic.Kernel.Context import ContextDelegate
from elliptic_meshql.Selector import SelectorImplementationBase


class LoopDelegate(ContextDelegate):

    loop_name = ''

    def __init__(self, context, unique_id):
        super().__init__(context, unique_id)

        self.loop_var_prefix = self.loop_name + str(self.unique_id)

    def template_kwargs(self):
        return {'current_entity': self.context.get_value('current_entity_name'),
                'current_range': self.context.get_value('current_range_name'),
                'current_index': self.context.get_value('current_index_name'),
                'reduced_variables': self.context.context[self.loop_var_prefix + 'reduced'],
                'mapped_variables': self.context.context[self.loop_var_prefix + 'mapped'],
                'reduce_nested_children': self.context.context[self.loop_var_prefix + 'nested_children']}

    def context_enter(self):
        self.context.put_value('current_loop', self.loop_var_prefix)

        self.context.put_value('declare_range', self.loop_var_prefix + 'range')
        self.context.put_value('current_range_name', self.loop_var_prefix + 'range')

        self.context.put_value('declare_entityhandle', self.loop_var_prefix + 'entity')
        self.context.put_value('current_entity_name', self.loop_var_prefix + 'entity')

        self.context.put_value('declare_index', self.loop_var_prefix + 'index')
        self.context.put_value('current_index_name', self.loop_var_prefix + 'index')

    def context_exit(self):
        self.context.pop_value('current_range_name')
        self.context.pop_value('current_entity_name')
        self.context.pop_value('current_index_name')


class SelectorImplementation(SelectorImplementationBase):

    def by_ent_delegate(self, dim: int) -> Type[ContextDelegate]:
        class ByEntDelegate(LoopDelegate):

            loop_name = 'by_ent'

            def get_template_file(self):
                return 'Selector/by_ent.pyx.etp'

            def template_kwargs(self):
                return {'dim': dim,
                        **super().template_kwargs()}

        return ByEntDelegate

    def by_adj_delegate(self, bridge_dim: int, to_dim: int) -> Type[ContextDelegate]:
        class ByAdjDelegate(LoopDelegate):

            loop_name = 'by_adj'

            def get_template_file(self):
                return 'Selector/by_adj.pyx.etp'

            def template_kwargs(self):
                return {'bridge_dim': bridge_dim,
                        'to_dim': to_dim,
                        'old_entity': self.context.context['current_entity_name'][-2],
                        **super().template_kwargs()}

        return ByAdjDelegate

    def where_delegate(self, conditions):
        pass

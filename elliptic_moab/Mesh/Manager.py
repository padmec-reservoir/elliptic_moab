from typing import Type

from elliptic.Kernel.Context import ContextDelegate
from elliptic_meshql.Manager import ManagerImplementationBase


class ManagerImplementation(ManagerImplementationBase):
    def solve_delegate(self) -> Type[ContextDelegate]:
        pass

    def store_delegate(self, field_name) -> Type[ContextDelegate]:

        class MapDelegate(ContextDelegate):

            def get_template_file(self):
                return 'Manager/store.pyx.etp'

            def template_kwargs(self):
                return {'field_name': field_name,
                        'current_entity': self.context.get_value('current_entity_name'),
                        'current_variable': self.context.get_value('current_variable')}

            def context_enter(self):
                self.context.put_value('declare_tags', field_name)

            def context_exit(self):
                pass

        return MapDelegate

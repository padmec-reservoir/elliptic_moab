from typing import Type

from elliptic.Kernel.Context import ContextDelegate

from .Selector import SelectorImplementation
from .Manager import ManagerImplementation
from .Computer import ComputerImplementation


class MeshQLImplementation(ComputerImplementation, ManagerImplementation, SelectorImplementation):
    def base_delegate(self) -> Type[ContextDelegate]:

        class BaseDelegate(ContextDelegate):

            def get_template_file(self):
                return 'base.pyx.etp'

            def template_kwargs(self):
                return {'declare_entityhandles': self.context.context['declare_entityhandle'],
                        'declare_ranges': self.context.context['declare_range'],
                        'declare_indexes': self.context.context['declare_index'],
                        'declare_variables': self.context.context['declare_variable']}

            def context_enter(self):
                pass

            def context_exit(self):
                pass

        return BaseDelegate

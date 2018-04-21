from typing import Type

from elliptic.Kernel.Context import ContextDelegate
from elliptic_meshql.Computer import ComputerImplementationBase, MeshQLFunction


class ComputerImplementation(ComputerImplementationBase):

    def map_delegate(self, fun: MeshQLFunction) -> Type[ContextDelegate]:

        class MapDelegate(ContextDelegate):

            def get_template_file(self):
                return 'Computer/map.pyx.etp'

            def template_kwargs(self):
                return {'map_function': fun.fun,
                        'map_args': fun.fargs,
                        'current_entity': self.context.get_value('current_entity_name'),
                        'current_variable': self.context.get_value('current_variable')}

            def context_enter(self):
                current_loop = self.context.get_value('current_loop')

                self.context.put_value('declare_variable', 'map_var' + str(self.unique_id))
                self.context.put_value(current_loop + 'mapped', 'reduce_var' + str(self.unique_id))
                self.context.put_value('current_variable', 'map_var' + str(self.unique_id))

            def context_exit(self):
                self.context.pop_value('current_variable')

        return MapDelegate

    def reduce_delegate(self, fun: MeshQLFunction) -> Type[ContextDelegate]:

        class ReduceDelegate(ContextDelegate):

            def get_template_file(self):
                return 'Computer/reduce.pyx.etp'

            def template_kwargs(self):
                return {'reduce_function': fun.fun,
                        'reduce_args': fun.fargs,
                        'current_variable': self.context.context['current_variable'][-2],
                        'reduced_variable': self.context.get_value('current_variable')}

            def context_enter(self):
                self.current_loop = self.context.get_value('current_loop')

                self.context.put_value('declare_variable', 'reduce_var' + str(self.unique_id))
                self.context.put_value(self.current_loop + 'reduced', 'reduce_var' + str(self.unique_id))
                self.context.put_value('current_variable', 'reduce_var' + str(self.unique_id))

                # For nested reduces:
                self.context.pop_value('current_loop')

            def context_exit(self):
                self.context.pop_value('current_variable')

                # For other reduces in the same loop level:
                self.context.put_value('current_loop', self.current_loop)
                self.context.put_value(self.current_loop + 'nested_children', self.child)

        return ReduceDelegate

from elliptic.Kernel.MeshComputeInterface.BackendBuilder import ContextType, ContextDelegate


class BaseDelegate(ContextDelegate):

    def get_template_file(self):
        return 'base.pyx.etp'

    def template_kwargs(self, context: ContextType):
        return {'a': self.get_value('a'),
                'b': self.get_value('b')}

    def context_enter(self, context: ContextType):
        self.put_value('a', 'x')
        self.put_value('b', 'a')
        self.put_value('cur_var', 'base_str')

    def context_exit(self, context: ContextType):
        self.pop_value('a')
        self.pop_value('b')
        self.pop_value('cur_var')


class ByEntDelegate(ContextDelegate):

    def __init__(self, context, dim):
        super().__init__(context)
        self.dim = dim

    def get_template_file(self):
        return 'Selector/by_ent.pyx.etp'

    def template_kwargs(self, context: ContextType):
        return {'append_var': self.get_value('cur_var'),
                'append_val': self.get_value('a')}

    def context_enter(self, context: ContextType):
        self.put_value('a', str(self.dim))

    def context_exit(self, context: ContextType):
        self.pop_value('a')

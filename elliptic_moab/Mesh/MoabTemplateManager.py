from elliptic.Kernel.TreeBuilder import TemplateManagerBase


class MoabTemplateManager(TemplateManagerBase):

    def __init__(self) -> None:
        super().__init__(__package__, 'Templates')

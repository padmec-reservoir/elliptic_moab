from typing import List

from elliptic.Kernel.DSL import DSLMeta


class MoabMeta(DSLMeta):
    def libs(self) -> List[str]:
        return ["MOAB"]

    def include_dirs(self) -> List[str]:
        return []

from typing import Type

from elliptic.Kernel.Context import ContextDelegate
from elliptic_meshql.Manager import ManagerImplementationBase


class ManagerImplementation(ManagerImplementationBase):
    def solve_delegate(self) -> Type[ContextDelegate]:
        pass

    def store_delegate(self) -> Type[ContextDelegate]:
        pass
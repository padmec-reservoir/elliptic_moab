from elliptic.Kernel.MeshComputeInterface.BackendBuilder import BackendBuilder
from elliptic.Kernel.MeshComputeInterface.Expression.Computer import EllipticFunction, EllipticReduce

from elliptic_moab.Mesh.Delegates import *


class MoabBackendBuilder(BackendBuilder):

    def base_delegate(self, context):
        return BaseDelegate(context)

    def by_ent_delegate(self, context, dim: int):
        return ByEntDelegate(context, dim)

    def by_adj_delegate(self, context, bridge_dim: int, to_dim: int):
        return ByAdjDelegate(context, bridge_dim, to_dim)

    def where_delegate(self, context, conditions):
        pass

    def map_delegate(self, context, mapping_function: 'EllipticFunction', fargs):
        return MapDelegate(context, mapping_function, fargs)

    def reduce_delegate(self, context, reducing_function: 'EllipticReduce', fargs):
        return ReduceDelegate(context, reducing_function, fargs)

    def put_field_delegate(self, context, field_name: str):
        pass

    def create_matrix_delegate(self, context, field_name: str):
        pass

    def fill_columns_delegate(self, context, matrix: int):
        pass

    def fill_diag_delegate(self, context, matrix: int):
        pass

    def solve_delegate(self, context):
        pass

    def put_scalar(self, value):
        return {"value": value}

    def reduce_sum(self, initial_value):
        return {"initial_value": initial_value}
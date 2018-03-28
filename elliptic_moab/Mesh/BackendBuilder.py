from elliptic.Kernel.MeshComputeInterface.BackendBuilder import BackendBuilder

from elliptic_moab.Mesh.Delegates import *


class MoabBackendBuilder(BackendBuilder):

    def base_delegate(self, context):
        return BaseDelegate(context)

    def by_ent_delegate(self, context, dim: int):
        return ByEntDelegate(context, dim)

    def by_adj_delegate(self, context, bridge_dim: int, to_dim: int):
        pass

    def where_delegate(self, context, conditions):
        pass

    def map_delegate(self, context, mapping_function: 'EllipticFunction', fargs):
        pass

    def reduce_delegate(self, context, reducing_function: 'EllipticReduce', fargs):
        pass

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

    def base(self):
        return "base.pyx.etp"

    def by_ent(self):
        return "Selector/by_ent.pyx.etp"

    def where(self):
        return "Selector/where.pyx.etp"

    def map(self):
        return "Computer/map.pyx.etp"

    def put_field(self):
        return "Manager/put_field.pyx.etp"

    def create_field(self):
        return "Declare/create_field.pyx.etp"

    def get_field(self):
        return "Declare/get_field.pyx.etp"

    def declare_variable(self):
        return "Declare/declare_variable.pyx.etp"

from elliptic.Kernel.MeshComputeInterface.Expression import Selector
from elliptic.Kernel.MeshComputeInterface.Expression.Computer.Map import Map
from elliptic.Kernel.MeshComputeInterface.Expression.Computer.Reduce import Reduce
from elliptic.Kernel.MeshComputeInterface.Expression.Computer.MapFunctions import PutScalar
from elliptic.Kernel.MeshComputeInterface.Expression.Computer.ReduceFunctions import Sum


class TestTreeBuilder:

    def test_by_ent(self, mci, elliptic):
        with mci.root() as root:
            ents = root(Selector.Dilute.ByEnt, dim=3)
            vols_adj_ents = ents(Selector.Dilute.ByAdj, bridge_dim=2, to_dim=3)

            one = vols_adj_ents(Map, mapping_function=PutScalar(value=1.0))
            count = one(Reduce, reducing_function=Sum(initial_value=0.0))
            count_other = vols_adj_ents(Reduce, reducing_function=Sum(initial_value=0.0))

            #root.export_tree('res1.png')

        elliptic.run_kernel(mci)

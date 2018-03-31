from elliptic.Kernel.MeshComputeInterface.Expression import Selector


class TestTreeBuilder:

    def test_by_ent(self, mci, elliptic):
        with mci.root() as root:
            ents = root(Selector.Dilute.ByEnt, dim=3)
            vols_adj_ents = internal_ents(Selector.Dilute.ByAdj, bridge_dim=2, to_dim=3)


            #root.export_tree('res1.png')

        elliptic.run_kernel(mci)

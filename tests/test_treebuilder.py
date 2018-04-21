from elliptic.Kernel.DSL import DSL
from elliptic_meshql.MeshQL import MeshQLContract
from pymoab import core

from elliptic_moab.Mesh.MeshQL import MeshQLImplementation
from elliptic_moab.Mesh.MoabMeta import MoabMeta
from elliptic_moab.Mesh.MoabTemplateManager import MoabTemplateManager


class TestTreeBuilder:

    def test_meshql(self):
        dsl = DSL(MoabTemplateManager(),
                  MeshQLContract(MeshQLImplementation()),
                  MoabMeta())

        mb = core.Core()
        mb.load_file('cube_small.h5m')

        with dsl.root() as root:
            ents = root.ByEnt(3)
            vols_adj_ents = ents.ByAdj(2, 3)

            #one = vols_adj_ents(Map, mapping_function=PutScalar(value=1.0))
            #count = one(Reduce, reducing_function=Sum(initial_value=0.0))
            #count2 = count(Reduce, reducing_function=Sum(initial_value=0.0))

            #root.export_tree('res1.png')

        dsl.get_built_module().execute(mb)

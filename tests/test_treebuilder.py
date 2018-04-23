import time

from elliptic.Kernel.DSL import DSL
from elliptic_meshql.MapFunctions import SetScalar
from elliptic_meshql.ReduceFunctions import Sum
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
            ents = root.ByEnt(3)\
                .ByAdj(2, 3)\
                .Map(SetScalar(1.0))\
                .ByAdj(2, 3).Map(SetScalar(1.0))\
                .Reduce(Sum(initial_value=0.0)).Reduce(Sum(initial_value=0.0)).Reduce(Sum(initial_value=0.0))\
                .Store("TEST_TAG")

            #one = vols_adj_ents(Map, mapping_function=PutScalar(value=1.0))
            #count = one(Reduce, reducing_function=Sum(initial_value=0.0))
            #count2 = count(Reduce, reducing_function=Sum(initial_value=0.0))

            root.expr.export_tree('res1.png')

        t0 = time.time()
        for i in range(1000):
            dsl.get_built_module().execute(mb)
        print(f'{(time.time() - t0)/1000}')

        #mb.write_file('cube_small_tagged.h5m')

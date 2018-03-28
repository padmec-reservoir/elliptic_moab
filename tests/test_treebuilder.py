from elliptic.Kernel.MeshComputeInterface.Expression import StatementRoot
from elliptic.Kernel.MeshComputeInterface.Expression.Selector.Dilute import ByEnt
from elliptic.Kernel.TreeBuilder import TreeBuild


class TestTreeBuilder:

    def test_render_single_node(self, template_manager, backend_builder):
        tree_builder = TreeBuild(template_manager, backend_builder)
        statement_root = StatementRoot()

        built_module = tree_builder.build(statement_root)

        assert built_module.test_fun() == 'x a'

    def test_render_two_node(self, template_manager, backend_builder):
        tree_builder = TreeBuild(template_manager, backend_builder)
        statement_root = StatementRoot()
        statement_root.children = (ByEnt(2),)

        built_module = tree_builder.build(statement_root)

        assert built_module.test_fun() == 'x a2'

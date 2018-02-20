from types import ModuleType

from pymoab import core

from .MoabTemplateManager import MoabTemplateManager
from .TreePreprocessor import TreePreprocessor


class Mesh:

    def __init__(self, mb) -> None:
        self.mb = mb

    def export(self, filename):
        self.mb.write_file(filename)

class Grid:

    def __init__(self, nx, ny, nz, dx, dy, dz):
        self.nx = nx
        self.ny = ny
        self.nz = nz
        self.dx = dx
        self.dy = dy
        self.dz = dz

    def get_coord(self, i, j, k):
        return [i * self.dx, j * self.dy, k * self.dz]


class MeshBuilder:

    def read_file(self, filename):
        mb = core.Core()
        mb.load_file(filename)

        the_mesh = Mesh(mb)

        return the_mesh

    def grid(self, nx, ny, nz, dx, dy, dz):
        return Grid(nx, ny, nz, dx, dy, dz)


class MeshBackend:

    def __init__(self, output_formats, report_format, fields):
        self.template_manager = MoabTemplateManager()

    def run_kernel(self, kernel_module, mesh) -> None:
        kernel_module.execute(mesh.mb)

    def mesh_builder(self):
        return MeshBuilder()

    def get_template_manager(self) -> MoabTemplateManager:
        return self.template_manager

    def get_backend_builder(self) -> ModuleType:
        from . import build_functions
        return build_functions

    def get_libraries(self):
        return ["MOAB"]

    def get_include_dirs(self):
        return []

    def tree_preprocess(self, root):
        preprocessor = TreePreprocessor(root)
        preprocessor.run()

    def export(self, mesh, filename):
        mesh.export(filename)
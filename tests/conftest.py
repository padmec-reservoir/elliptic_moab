import pytest
from elliptic import Elliptic
from elliptic.Kernel.MeshComputeInterface import MCI

from elliptic_moab.Mesh import MeshBackend
from elliptic_moab.Mesh.MoabTemplateManager import MoabTemplateManager


@pytest.fixture()
def mesh_backend():
    mesh_backend_ = MeshBackend(None, None, None)

    return mesh_backend_


@pytest.fixture()
def elliptic(mocker, mesh_backend):
    elliptic_ = Elliptic(mesh_backend, mocker.Mock())
    elliptic_.set_mesh(mocker.sentinel.mesh)

    return elliptic_


@pytest.fixture()
def mci(elliptic):
    mci_ = MCI(elliptic)

    return mci_


@pytest.fixture()
def template_manager():
    template_manager_ = MoabTemplateManager()

    return template_manager_


@pytest.fixture()
def backend_builder(elliptic):
    backend_builder_ = elliptic.get_mesh_backend_builder()

    return backend_builder_

import collections
import numpy as np

from pymoab import core, topo_util, types


mb = core.Core()
mtu = topo_util.MeshTopoUtil(mb)


mb.load_file('mesh/case.msh')

mb.tag_get_handle("TEST_TAG", 1, types.MB_TYPE_DOUBLE, types.MB_TAG_SPARSE, True)

fields = [('DIFFUSIVITY', 50, 1.0),
          ('INLET', 101, 1.0),
          ('OUTLET', 102, 0.0),
          ('WALL', 103, 0.0)]

tag_data = collections.defaultdict(list)

for tag_name, phys_id, data in fields:
    data_size = 1  # scalar

    tag_handle = mb.tag_get_handle(
        tag_name, data_size, types.MB_TYPE_DOUBLE, True,
        types.MB_TAG_SPARSE)

    elems_tag = mb.tag_get_handle(
        tag_name + "_elems", 1, types.MB_TYPE_HANDLE, True,
        types.MB_TAG_MESH)

    tag_data[int(phys_id)].append({
        'elems_tag': elems_tag,
        'tag': tag_handle,
        'data': data})


physical_tag = mb.tag_get_handle("MATERIAL_SET")

physical_sets = mb.get_entities_by_type_and_tag(
    0, types.MBENTITYSET,
    np.array((physical_tag,)), np.array((None,)))

gid_tag = mb.tag_get_handle('GLOBAL_ID')


for tag_ms in physical_sets:
    tag_id = mb.tag_get_data(
        physical_tag, np.array([tag_ms]), flat=True)[0]

    elems = mb.get_entities_by_handle(tag_ms, True)

    for tag_data_values in tag_data[tag_id]:
        elems_tag = tag_data_values['elems_tag']
        data_tag_handle = tag_data_values['tag']
        data = tag_data_values['data']
        gids = mb.tag_get_data(gid_tag, elems, flat=True)

        root_set = mb.get_root_set()
        elems_set = mb.create_meshset()
        mb.add_entities(elems_set, elems)
        mb.tag_set_data(elems_tag, root_set, elems_set)

        for gid, elem in zip(gids, elems):
            mb.tag_set_data(
                data_tag_handle, elem, data)

mb.tag_delete(physical_tag)

mb.write_file('output.vtk')

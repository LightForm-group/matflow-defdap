'`matflow_defdap.main.py`'

import hickle

from matflow_defdap import (
    input_mapper,
    output_mapper,
    cli_format_mapper,
    register_output_file,
    func_mapper,
    software_versions,
    sources_mapper
)
from matflow_defdap.scripting import get_wrapper_script


@sources_mapper(task='load_microstructure', method='EBSD+DIC',
                script='load_microstructure')
def load_microstructure_EBSD_DIC():

    script_name = 'load_microstructure.py'
    snippets = [
        {'name': 'load_EBSD_map.py'},
        {'name': 'load_DIC_map.py'},
        {'name': 'link_EBSD_DIC_maps.py'},
        {'name': 'get_DIC_image.py'},
    ]
    outputs = ['DIC_image']
    out = {
        'script': {
            'content': get_wrapper_script(script_name, snippets, outputs),
            'filename': script_name,
        }
    }
    return out


@input_mapper(input_file='inputs.hdf5', task='load_microstructure', method='EBSD+DIC')
def write_param_file(path, DIC, EBSD, transform_type, root_path):
    obj = {
        'dic_filename': DIC['filename'],
        'dic_crop': DIC['crop'],
        'dic_scale': DIC['scale_num'] / DIC['scale_denom'],
        'dic_homog_points': DIC['homog_points'],
        'dic_min_grain_size': DIC['min_grain_size'],
        'ebsd_filename': EBSD['filename'],
        'ebsd_structure': EBSD['structure'],
        'ebsd_flip_vert': EBSD['flip_vert'],
        'ebsd_boundary_tol': EBSD['boundary_tol'],
        'ebsd_min_grain_size': EBSD['min_grain_size'],
        'ebsd_homog_points': EBSD['homog_points'],
        'transform_type': transform_type,
        'root_path': root_path,
    }
    hickle.dump(obj, path)


@output_mapper(
    output_name='microstructure_image',
    task='load_microstructure',
    method='EBSD+DIC',
)
def read_DIC_image_file(path):
    return hickle.load(path)

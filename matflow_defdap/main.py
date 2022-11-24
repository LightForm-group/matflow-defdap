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
def write_param_file(path, DIC, EBSD, transform_type, root_path, scaling_factor, find_grains_algorithm):
    obj = {
        'dic_filename': DIC['filename'],
        'dic_crop': DIC.get('crop', None),
        'dic_scale': DIC.get('scale', None),
        'dic_min_grain_size': DIC.get('min_grain_size', 10),
        'dic_homog_points': DIC['homog_points'],
        'ebsd_filename': EBSD['filename'],
        'ebsd_boundary_tol': EBSD.get('boundary_tol', 10),
        'ebsd_min_grain_size': EBSD.get('min_grain_size', 10),
        'ebsd_homog_points': EBSD['homog_points'],
        'transform_type': transform_type,
        'root_path': root_path,
        'scaling_factor': scaling_factor,
        'find_grains_algorithm': find_grains_algorithm,
    }
    hickle.dump(obj, path)


@output_mapper(
    output_name='microstructure_image',
    task='load_microstructure',
    method='EBSD+DIC',
)
def read_DIC_image_file(path):
    return hickle.load(path)


@sources_mapper(task='load_microstructure', method='EBSD',
                script='load_microstructure')
def load_microstructure_EBSD():

    script_name = 'load_microstructure.py'
    snippets = [
        {'name': 'load_EBSD_map.py'},
        {'name': 'get_EBSD_image.py'},
    ]
    outputs = ['EBSD_image']
    out = {
        'script': {
            'content': get_wrapper_script(script_name, snippets, outputs),
            'filename': script_name,
        }
    }
    return out


@input_mapper(input_file='inputs.hdf5', task='load_microstructure', method='EBSD')
def write_param_file_2(path, EBSD, root_path, scaling_factor):
    obj = {
        'ebsd_filename': EBSD['filename'],
        'ebsd_boundary_tol': EBSD.get('boundary_tol', 10),
        'ebsd_min_grain_size': EBSD.get('min_grain_size', 10),
        'root_path': root_path,
        'scaling_factor': scaling_factor,
    }
    hickle.dump(obj, path)


@output_mapper(
    output_name='microstructure_image',
    task='load_microstructure',
    method='EBSD',
)
def read_EBSD_image_file(path):
    return hickle.load(path)

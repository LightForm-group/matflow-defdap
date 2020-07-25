'`matflow_defdap.__init__.py`'

from functools import partial

from matflow_defdap._version import __version__

from matflow.extensions import (
    input_mapper,
    output_mapper,
    cli_format_mapper,
    register_output_file,
    func_mapper,
    software_versions,
    sources_mapper,
)

SOFTWARE = 'DefDAP'

input_mapper = partial(input_mapper, software=SOFTWARE)
output_mapper = partial(output_mapper, software=SOFTWARE)
cli_format_mapper = partial(cli_format_mapper, software=SOFTWARE)
register_output_file = partial(register_output_file, software=SOFTWARE)
func_mapper = partial(func_mapper, software=SOFTWARE)
software_versions = partial(software_versions, software=SOFTWARE)
sources_mapper = partial(sources_mapper, software=SOFTWARE)

def main_func(func):
    '''Decorator used to annotate which function within a snippet is the main function.'''
    def main_inner(*args, **kwargs):
        func(*args, **kwargs)
    return main_inner

# Import any modules that contain functions decorated by the matflow function decorators.
# This import must come after the above `partial`s.
from matflow_defdap import main

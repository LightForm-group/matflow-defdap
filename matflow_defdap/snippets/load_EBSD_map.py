from pathlib import Path

import numpy as np
import defdap.ebsd as ebsd

from matflow_defdap import main_func


@main_func
def load_EBSD_map(root_path, ebsd_filename, ebsd_boundary_tol,
                  ebsd_min_grain_size):
    'Load EBSD map and detect grains.'

    ebsd_map = ebsd.Map(Path(root_path).joinpath(ebsd_filename))

    # check for non-indexed points
    if np.count_nonzero(ebsd_map.phaseArray == 0) != 0:
        raise ValueError('EBSD map contains non-indexed points.')

    ebsd_map.buildQuatArray()

    ebsd_map.findBoundaries(boundDef=ebsd_boundary_tol)
    ebsd_map.findGrains(minGrainSize=ebsd_min_grain_size)
    ebsd_map.calcGrainAvOris()

    return ebsd_map

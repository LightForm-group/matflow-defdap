from pathlib import Path

import defdap.ebsd as ebsd

from matflow_defdap import main_func


@main_func
def load_EBSD_map(root_path, ebsd_filename, ebsd_structure, ebsd_flip_vert, ebsd_boundary_tol,
                  ebsd_min_grain_size):
    'Load EBSD map and detect grains.'

    EbsdMap = ebsd.Map(Path(root_path).joinpath(ebsd_filename), ebsd_structure)

    # Flip EBSD map in vertical direction if needed
    if ebsd_flip_vert:
        EbsdMap.eulerAngleArray = EbsdMap.eulerAngleArray[:, ::-1, ::-1]
        EbsdMap.bandContrastArray = EbsdMap.bandContrastArray[::-1, ::-1]
        EbsdMap.phaseArray = EbsdMap.phaseArray[::-1, ::-1]

    EbsdMap.buildQuatArray()

    EbsdMap.findBoundaries(boundDef=ebsd_boundary_tol)
    EbsdMap.findGrains(minGrainSize=ebsd_min_grain_size)
    EbsdMap.calcGrainAvOris()

    return EbsdMap

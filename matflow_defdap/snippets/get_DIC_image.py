import numpy as np

from matflow_defdap import main_func


@main_func
def get_DIC_image(DicMap):

    grain_eulers = np.empty((len(DicMap), 3))

    for i, grain in enumerate(DicMap):
        grain_eulers[i] = grain.ebsdGrain.refOri.eulerAngles()

    grain_eulers *= 180 / np.pi

    DIC_image = {
        'orientations': grain_eulers,
        'grains': DicMap.grains,
        'scale': DicMap.scale,
    }
    return DIC_image

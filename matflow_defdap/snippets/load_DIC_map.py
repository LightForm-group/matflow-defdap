import defdap.hrdic as hrdic

from matflow_defdap import main_func


@main_func
def load_DIC_map(root_path, dic_filename, dic_crop, dic_scale):
    'Load in DIC, crop and set scale.'

    DicMap = hrdic.Map(root_path, dic_filename)
    if dic_crop is not None:
        DicMap.setCrop(
            xMin=dic_crop[0],
            xMax=dic_crop[1],
            yMin=dic_crop[2],
            yMax=dic_crop[3]
        )
    if dic_scale is not None:
        DicMap.setScale(dic_scale)

    return DicMap

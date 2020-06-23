import defdap.hrdic as hrdic


def load_DIC_map(root_path, dic_filename, dic_crop, dic_scale):
    'Load in DIC, crop and set scale.'

    DicMap = hrdic.Map(root_path, dic_filename)
    DicMap.setCrop(
        xMin=dic_crop[0],
        xMax=dic_crop[1],
        yMin=dic_crop[2],
        yMax=dic_crop[3]
    )
    DicMap.setScale(dic_scale)

    return DicMap

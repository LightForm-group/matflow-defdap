from matflow_defdap import main_func


@main_func
def link_EBSD_DIC_maps(EbsdMap, DicMap, dic_homog_points, dic_min_grain_size,
                       ebsd_homog_points, transform_type):

    DicMap.homogPoints = dic_homog_points
    EbsdMap.homogPoints = ebsd_homog_points
    DicMap.linkEbsdMap(EbsdMap, transformType=transform_type)

    DicMap.findGrains(minGrainSize=dic_min_grain_size)

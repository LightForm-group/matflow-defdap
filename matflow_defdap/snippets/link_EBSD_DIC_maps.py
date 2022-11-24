from matflow_defdap import main_func


@main_func
def link_EBSD_DIC_maps(ebsd_map, dic_map, dic_homog_points, dic_min_grain_size,
                       ebsd_homog_points, transform_type):

    dic_map.homogPoints = dic_homog_points
    ebsd_map.homogPoints = ebsd_homog_points
    dic_map.linkEbsdMap(ebsd_map, transformType=transform_type)

    dic_map.findGrains(minGrainSize=dic_min_grain_size)

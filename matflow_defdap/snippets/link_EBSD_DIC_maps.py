from matflow_defdap import main_func


@main_func
def link_EBSD_DIC_maps(EbsdMap, DicMap, dic_homog_points, dic_min_grain_size,
                       ebsd_homog_points, transform_type):

    DicMap.homogPoints = dic_homog_points
    EbsdMap.homogPoints = ebsd_homog_points
    DicMap.linkEbsdMap(EbsdMap, transformType=transform_type)

    # Check everything looks okay:
    DicMap.plotMaxShear(
        plotGBs=True,
        plotScaleBar=True,
        dilateBoundaries=True,
        vmin=0,
        vmax=0.1
    )

    DicMap.findGrains(minGrainSize=dic_min_grain_size)

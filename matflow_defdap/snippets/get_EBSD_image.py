import numpy as np
from defdap.quat import Quat
from scipy.stats import mode
from scipy.ndimage import zoom

from matflow_defdap import main_func


@main_func
def get_EBSD_image(EbsdMap, scaling_factor):

    # Construct an array of Euler angles
    grain_quats = np.empty((len(EbsdMap), 4))

    # Transformation orientations from EBSD orientation reference frame
    # to EBSD spatial reference frame
    frame_transform = Quat.fromAxisAngle(np.array((1, 0, 0)), np.pi)

    if EbsdMap.crystalSym == 'hexagonal':
        # Convert hex convention from y // a2 of EBSD map to x // a1 for DAMASK
        hex_transform = Quat.fromAxisAngle(np.array([0, 0, 1]), -np.pi/6)
        for i, grain in enumerate(EbsdMap):
            grain_quats[i] = (hex_transform * grain.refOri * frame_transform).quatCoef

    else:
        for i, grain in enumerate(EbsdMap):
            grain_quats[i] = (grain.refOri * frame_transform).quatCoef

    # Filter out -2 (too small grains) values in the grain image
    grain_image = EbsdMap.grains
    remove_small_grain_points(grain_image)

    # scale down image if needed
    if scaling_factor != 1:
        grain_image = zoom(grain_image, scaling_factor, order=0,
                           prefilter=False, mode='nearest')

    # downstream expects grain numbering to start at 0 not 1
    grain_image -= 1

    EBSD_image = {
        'orientations': {
            'type': 'quat',
            'unit_cell_alignment': {'x': 'a'},
            'quaternions': grain_quats,
            'P': 1,  # DefDAP uses P=+1 (e.g see `defdap.quat.Quat.__mul__`)
            'quat_component_ordering': 'scalar-vector',
        },
        'grains': grain_image,
        'scale': EbsdMap.scale,
    }

    return EBSD_image


def select_area(i, j, grain_image):
    i_min, i_max = 1, 1
    j_min, j_max = 1, 1

    on_edge = 0

    if i == 0:
        i_min = 0
        on_edge += 1
    elif i == grain_image.shape[0]-1:
        i_max = 0
        on_edge += 1

    if j == 0:
        j_min = 0
        on_edge += 1
    elif j == grain_image.shape[1]-1:
        j_max = 0
        on_edge += 1

    # select 3x3 region around point
    area = grain_image[i-i_min:i+i_max+1, j-j_min:j+j_max+1]

    return area, on_edge


def remove_small_grain_points(grain_image, max_iterations=200):
    # num_neighbours - must have at least this many pixels surrounding
    # start checking for 8 neighbours, then 7 until 2
    all_done = False
    for num_neighbours in list(range(8, 1, -1)):
        print(f"Starting iterations with at least {num_neighbours} equal neighbours")

        num_bad_prev = 0
        iteration = 0
        while True:
            num_bad = np.count_nonzero(grain_image == -2)
            if num_bad == 0:
                # No bad values left, done
                print("All bad points removed.")
                all_done = True
                break
            elif num_bad == num_bad_prev:
                # Not removing any more
                print("Number of bad points is not decreasing!")
                break
            if iteration > max_iterations:
                print("Max iterations.")
                break

            iteration += 1
            print("Starting iteration {}, num bad: {}".format(iteration, num_bad))

            grain_image_new = np.copy(grain_image)

            for i, j in zip(*np.where(grain_image == -2)):

                area, on_edge = select_area(i, j, grain_image)
                area = area.flatten()
                area = area[np.where(area > 0)]   # remove -1 and -2

                mode_vals, mode_counts = mode(area)
                for mode_val, mode_count in zip(mode_vals, mode_counts):
                    if mode_count >= num_neighbours:
                        grain_image_new[i, j] = mode_val
                        break

            num_bad_prev = num_bad
            # [:, :] required to update the array passed in
            grain_image[:, :] = grain_image_new

        if all_done:
            break

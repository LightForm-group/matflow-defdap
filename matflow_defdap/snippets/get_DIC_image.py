import numpy as np
from defdap.quat import Quat
from scipy.stats import mode

from matflow_defdap import main_func


@main_func
def get_DIC_image(DicMap):

    # Construct an array of Euler angles
    grain_eulers = np.empty((len(DicMap), 3))

    # Transformation orientations from EBSD orientation reference frame to EBSD spatial reference frame
    transform_quat = Quat.fromAxisAngle(np.array((1, 0, 0)), np.pi)
    
    for i, grain in enumerate(DicMap):
        grain_eulers[i] = (grain.ebsdGrain.refOri * transform_quat).eulerAngles()
    
    grain_eulers *= 180 / np.pi

    # Filter out -1 (grain boundary points) and -2 (too small grains) values in the grain image
    grain_image = DicMap.grains
    remove_boundary_points(grain_image)
    remove_small_grain_points(grain_image)
    remove_boundary_points(grain_image)
    remove_boundary_points(grain_image, force_remove=True)

    # downstream expects grain numbering to start at 0 not 1
    grain_image -= 1

    DIC_image = {
        'orientations': grain_eulers,
        'grains': grain_image,
        'scale': DicMap.scale,
    }

    return DIC_image


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

    area = grain_image[i-i_min:i+i_max+1, j-j_min:j+j_max+1]  # select 3x3 region around point
    
    return area, on_edge


def remove_boundary_points(grain_image, force_remove=False, max_iterations=200):
    num_bad_prev = 0
    iteration = 0
    while True:
        num_bad = np.count_nonzero(grain_image == -1)
        if num_bad == 0:
            # No bad values left, done
            print("All bad points removed.")
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

        # because of how boundaries are defined, best to take from -ve side
        for i, j in zip(*np.where(grain_image == -1)):
            if i != 0 and j != 0 and grain_image[i-1, j] > 0 and grain_image[i, j-1] > 0:
                # if both left and above pixels defined, check the diagonal
                if grain_image[i-1, j-1] == grain_image[i-1, j]:
                    grain_image_new[i, j] = grain_image[i-1, j]

                elif grain_image[i-1, j-1] == grain_image[i, j-1]: 
                    grain_image_new[i, j] = grain_image[i, j-1]

                else:
                    # give up, try in next iteration

                    if force_remove:
                        area, on_edge = select_area(i, j, grain_image)
                        area = area.flatten()
                        area = area[np.where(area > 0)]   # remove -1 and -2

                        mode_vals, mode_counts = mode(area)
                        for mode_val, mode_count in zip(mode_vals, mode_counts):
                #         mode_val, mode_count = mode_vals[0], mode_counts[0]
    #                         if mode_count >= num_neighbours:
                            grain_image_new[i, j] = mode_val
                            break


            elif i != 0 and grain_image[i-1, j] > 0:
                grain_image_new[i, j] = grain_image[i-1, j]

            elif j != 0 and grain_image[i, j-1] > 0:
                grain_image_new[i, j] = grain_image[i, j-1]

            # give up, try in next iteration

        num_bad_prev = num_bad
        grain_image[:, :] = grain_image_new  # [:, :] required to update the array passed in


def remove_small_grain_points(grain_image, max_iterations=200):
    # num_neighbours - must have at least this many pixels surrounding
    # start checking for 8 neighbours, then 7 until 2
    all_done = False
    for num_neighbours in list(range(8, 1, -1)):
        print("Starting iterations with at least {:} equal neighbours".format(num_neighbours))

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
            grain_image[:, :] = grain_image_new  # [:, :] required to update the array passed in

        if all_done:
            break
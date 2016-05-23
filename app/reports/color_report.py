# ============================================================================
#
#
#                            RGB Report
#
#
# ============================================================================

import sys

import numpy as np
from matplotlib import pyplot as plt
from scipy.cluster.vq import kmeans, vq

from app.models import MbandImage


def rgb(image, original=True):
    """
        Show the RGB channels of a picture separated in one figure.

        :params:
            :params image: ImageND representing an image
            :params original: boolean flag to show or not the original image.
    """

    red, green, blue = image.rgb()

    # put the 4 images in a plot that looks like (positions):
    #             |
    #    pos 1    |   pos 2
    # ------------|------------
    #    pos 4    |   pos 4
    #             |

    pos1, pos2, pos3, pos4 = (221, 222, 223, 224)

    figure = plt.figure()
    figure.suptitle(
        "RGB for {0} using {1}".format(image.filename, image.SENSOR))

    plt.subplot(pos1)
    plt.imshow(red)
    plt.title("Red Channel")

    plt.subplot(pos2)
    plt.imshow(green)
    plt.title("Green Channel")

    plt.subplot(pos3)
    plt.imshow(blue)
    plt.title("Blue Channel")

    if original:
        plt.subplot(pos4)
        plt.imshow(image.image())
        plt.title("Original Image")

    plt.show()


def blue_channels(ibands_image, mbands_image, fc_image):
    """
        Create plot of RBG blue layer for fc, ibands, mband
    """

    blue1 = ibands_image.channel('blue')
    blue2 = mbands_image.channel('blue')
    blue3 = fc_image.channel('blue')

    blues = plt.figure()
    blues.suptitle("RBG blue layer for fc, ibands, mbands", fontsize=16)

    ibands_plot = plt.subplot(221)
    ibands_plot.set_title("ibands blue")
    ibands_plot.imshow(blue1)

    mbands_plot = plt.subplot(222)
    mbands_plot.set_title("mbands blue")
    mbands_plot.imshow(blue2)

    fc_plot = plt.subplot(223)
    fc_plot.set_title("fc blue")
    fc_plot.imshow(blue3)

    plt.show()


def find_water(mbands, ibands, lm):
    """
        Find water ice clusters using imbands and mbands

    """

    MAX_NAN_PERCENTAGE = 10.00

    # if image.nan_percentage() > MAX_NAN_PERCENTAGE:
        # print "{0} has more than {1}% NaN values".format(
            # image.filename, MAX_NAN_PERCENTAGE)
        # sys.exit(1)
    # if not isinstance(image, MbandImage):
        # print "{0} is not mbands".format(image.filename)
        # sys.exit(1)

    lm = lm.image()[2500:, range(2500, 3000)]

    # mbands 4 layer show landmask in great detail, making it different
    # from ice and water, ice shows up red.
    mbands = mbands.image()[:, :, 3][2500:, range(2500, 3000)]
    valid_mask = np.isfinite(mbands)
    data_mask = valid_mask & ~lm
    x = mbands[data_mask.astype(bool)]

    # Show the first mbands image to be used
    plt.imshow(mbands)
    plt.show()

    # ibands show ice very red water show's up very blue, land maske it's
    # a similar blue to ice, owever this shouldn't be a problem because we
    # are removeing lm from the analysis.
    ibands = ibands.image()[:, :, 2][2500:, range(2500, 3000)]
    valid_mask = np.isfinite(ibands)
    data_mask = valid_mask & ~lm
    y = ibands[data_mask.astype(bool)]

    # Show the first mbands image to be used
    plt.imshow(ibands)
    plt.show()

    z = np.column_stack((x, y))

    # k-means implementations
    centroids, _ = kmeans(z, 2)
    idx, _ = vq(z, centroids)

    plt.plot(
        z[idx == 0, 0], z[idx == 0, 1], 'ob',
        z[idx == 1, 0], z[idx == 1, 1], 'or')

    plt.plot(centroids[:, 0], centroids[:, 1], 'sg', markersize=8)
    plt.show()

def color_clusters(ibands_image, mbands_image, fc_image, lm):
    """
        Use k-means to clister the results and show the differences
        to define clouds, sea ice, land and ice clouds.
    """

    MAX_NAN_PERCENTAGE = 10.00

    # Verify that the image doesn't have too many NaN values
    for image in [ibands_image, mbands_image, fc_image]:
        if image.nan_percentage() > MAX_NAN_PERCENTAGE:
            print "{0} has more than {1}".format(
                image.filename, MAX_NAN_PERCENTAGE)
            sys.exit(1)

    lm = lm.image()[2500:, range(2500, 3000)]

    blue1 = ibands_image.image()[:, :, 2][2500:, range(2500, 3000)]
    valid_mask = np.isfinite(blue1)
    data_mask = valid_mask & ~lm
    x = blue1[data_mask.astype(bool)]

    blue2 = mbands_image.image()[:, :, 0][2500:, range(2500, 3000)]
    valid_mask = np.isfinite(blue2)
    data_mask = valid_mask & ~lm
    y = blue2[data_mask.astype(bool)]

    blue3 = fc_image.image()[:, :, 2][2500:, range(2500, 3000)]
    valid_mask = np.isfinite(blue2)
    data_mask = valid_mask & ~lm
    z = blue3[data_mask.astype(bool)]

    blues = np.column_stack((x, y, z))

    centroids, _ = kmeans(blues, 3)
    idx, _ = vq(blues, centroids)

    plt.plot(
        blues[idx == 0, 0], blues[idx == 0, 1], 'ob',
        blues[idx == 1, 0], blues[idx == 1, 1], 'or',
        blues[idx == 2, 0], blues[idx == 2, 1], 'og')
    # plt.plot(centroids[:, 0], centroids[:, 1], 'sg', markersize=8)
    plt.plot(centroids[:, 0], centroids[:, 1], centroids[:, 2], 'sg', markersize=8)
    plt.show()

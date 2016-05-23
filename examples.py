# --------------------------------------------------------------------------
#
#    This file contains several examples on the different operations
#    readily availble after load the .tmat files.
#
# --------------------------------------------------------------------------


import sys

import numpy as np
from matplotlib import pyplot as plt

from tools import data


# ===============================================
#            Image manipulation
# ===============================================


def show_rgb(image, original=True):

    # Check images size
    if len(image.shape) != 3:
        print "the image it's not af the shape (n, n, n)"
        sys.exit(1)
    if (image.shape)[2] != 3:
        try:
            image = np.dstack(image)
        except:
            print "The image's shape is not of the form (n, n, 3)"
            sys.exit(1)

    # Get RGB by slicing
    red = image[:, :, 0]
    green = image[:, :, 1]
    blue = image[:, :, 2]

    # put the 4 images in a plot that looks like (positions):
    #             |
    #    pos 1    |   pos 2
    # ------------|------------
    #    pos 4    |   pos 4
    #             |

    pos1, pos2, pos3, pos4 = (221, 222, 223, 224)

    plt.subplot(pos1)
    plt.imshow(red, cmap=plt.cm.Reds_r)

    plt.subplot(pos2)
    plt.imshow(green, cmap=plt.cm.Greens_r)

    plt.subplot(pos3)
    plt.imshow(blue, cmap=plt.cm.Blues_r)

    if original:
        plt.subplot(pos4)
        plt.imshow(image)

    plt.show()


def find_clouds(images):
    """
        While very basic in principle. I found out that by applying a blue
        layer to the reflectance instruments images ibands and mbands; I was
        able to see the clouds clearly.

        Method:
        - Get the blue layer out of the 3D images ibands and mbands
        - Add the two images to make sure that we are getting the clouds total
          reflectance.
    """
    pass


def sea_surface_temp(images, lm):

    # Sea water freezing temp in kelvin degrees (271.15 aprox 271)
    SEA_FREEZE_TEMP = 271

    #fill nan pixels with 0 and flatten array for temp
    #NaNs = np.isnan(images)
    #sst[NaNs] = 400
    #flat_sst = images.flatten()

    #img = plt.imshow(images)
    img = plt.imshow(lm)
    plt.colorbar(img)
    plt.show(img)

    #plt.hist(flat_sst, range(0, SEA_FREEZE_TEMP))
    #plt.hist(images, range(0, SEA_FREEZE_TEMP))
    #plt.show()


virs = data.file_names(instrument_id=0)
mods = data.file_names(instrument_id=1)
allfiles = data.file_names(instrument_id=2)


# load only first image
mat = data.mat_generator(virs).next()
#mat = mat_generator(mods).next()

# instruments' image
lm = mat['lm']
sst = mat['sst']
#sic = mat['mw_sic']
#ngr = mat['mw_ngr']
#npr = mat['mw_npr']
#fc = np.dstack(mat['fc'])
#ibands = np.dstack(mat['ibands'])

sea_surface_temp(sst, lm)


# ------------------------------------------------------------
# Create plot of RBG blue layer for fc, ibands, mbands
# ------------------------------------------------------------

#blue1 = ibands[:, :, 2]
#blue2 = mbands[:, :, 2]
#blue3 = fc[:, :, 2]
#clouds = np.add(blue1, blue2, blue3)

#blues = plt.figure()
#blues.suptitle("RBG blue layer for fc, ibands, mbands", fontsize=16)

#ibands_plot = plt.subplot(221)
#ibands_plot.set_title("ibands blue")
#ibands_plot.imshow(blue1)

#mbands_plot = plt.subplot(222)
#mbands_plot.set_title("mbands blue")
#mbands_plot.imshow(blue2)

#fc_plot = plt.subplot(223)
#fc_plot.set_title("fc blue")
#fc_plot.imshow(blue3)

#no_clouds_plot = plt.subplot(224)
#no_clouds_plot.set_title("Summation of fc, ibands, mbands blue")
#no_clouds_plot.imshow(clouds)


# Plot colors in picture
# ------------------------------------------------------------

#blue_plot = plt.figure()
#blue_plot.suptitle("RBG blue layer for ibands plot", fontsize=16)

#ibands_plot = plt.subplot(221)
#ibands_plot.set_title("ibands blue plot")
#ibands_plot.plot(blue1)

#ibands_plot = plt.subplot(222)
#ibands_plot.set_title("ibands blue image")
#ibands_plot.imshow(blue1)

#ibands_plot = plt.subplot(223)
#ibands_plot.set_title("ibands blue acordion")
#ibands_plot.hist(blue1[:, 0], bins=50)
#plt.hist(blue1.flatten(), bins=50)

#ibands_plot = plt.subplot(224)
#ibands_plot.set_title("ibands blue acordion")
#ibands_plot.acorr(blue1)

#plt.show()

import os
import sys

import numpy as np
from matplotlib import pyplot as plt

from tools import data


class ImageND(object):

    SENSOR = None

    def __init__(self, filename, dimensions=3):

        if dimensions < 3:
            print "The image doesn't have the minimum of 3 dimensions"
            sys.exit(1)

        self.dimensions = dimensions
        self.filename = filename
        self.filepath = os.path.join(data.DATA_DIR, self.filename)
        self.title = filename[2:15]

    def __validate(self, image):
        """
            Validate image, check that's n-'dimensions' channel image
        """
        if image is not None and len(image.shape) >= self.dimensions:
            return True
        return False

    def image(self):
        """
            Returns the raw ndarray image

            :rtype: ndarray
        """
        image = data.mat_file(self.filepath).get(self.SENSOR)
        if not self.__validate(image):
            print "Invalid dimensions or sensor {0} isn't in the image".format(
                self.sensor)
            sys.exit(1)
        return np.dstack(image)

    def nan_percentage(self):
        nan_count = np.count_nonzero(~np.isnan(self.image()))
        return (nan_count / self.image().size) * 100

    def date(self):
        return data.parse_date(self.filename)

    def show(self, colorbar=True):
        plt.imshow(self.image())
        plt.title(self.filename)
        if colorbar:
            plt.colorbar()
        plt.show()

    # =====================================
    #                Analysis
    # =====================================

    def rgb(self):
        """
            Return 3-tuple with (r, g, b)
        """

        red = self.channel("red")
        green = self.channel("green")
        blue = self.channel("blue")

        return (red, green, blue)

    def channel(self, channel=None):
        """
            This function is to be overwritten in by subclass
        """
        return None


class IbandImage(ImageND):

    SENSOR = "ibands"

    def channel(self, channel=None):
        """
            Returns a specific channel, the options are:
                - red, green, blue

            :params:
                :params channel: string with the specified channel

            :rType: ndarray
        """

        if channel == 'red':
            return self.image()[:, :, 0]
        elif channel == 'green':
            return self.image()[:, :, 1]
        elif channel == 'blue':
            return self.image()[:, :, 2]
        else:
            print "Channel requested wasn't red, green or blue"


class MbandImage(ImageND):

    SENSOR = "mbands"

    def channel(self, channel=None):
        """
            Returns a specific channel, the options are:
                - red
                - blue

            :params:
                :params channel: string with the specified channel

            :rType: ndarray
        """
        channel = channel.strip().lower()

        if channel == 'red':
            return self.image()[:, :, 2]
        elif channel == 'green':
            return self.image()[:, :, 1]
        elif channel == 'blue':
            return self.image()[:, :, 0]
        else:
            print "Channel requested wasn't red, green or blue"


class FcImage(ImageND):

    SENSOR = "fc"

    def channel(self, channel=None):
        """
            Returns a specific channel, the options are:
                - red
                - blue

            :params:
                :params channel: string with the specified channel

            :rType: ndarray
        """
        channel = channel.strip().lower()

        if channel == 'red':
            return self.image()[:, :, 0]
        elif channel == 'green':
            return self.image()[:, :, 1]
        elif channel == 'blue':
            return self.image()[:, :, 2]
        else:
            print "Channel requested wasn't red, green or blue"

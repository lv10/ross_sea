import os
import sys

import numpy as np
from scipy.stats import itemfreq
from matplotlib import pyplot as plt
from scipy.ndimage import filters, sobel

from tools import data


class Image2D(object):

    SENSOR = None

    def __init__(self, filename):
        self.filename = filename
        self.filepath = os.path.join(data.DATA_DIR, self.filename)
        self.title = filename[2:15]

    def image(self):
        """
            Returns the raw ndarray image

            :rtype: ndarray
        """
        return data.mat_file(self.filepath).get(self.SENSOR)

    def date(self):
        return data.parse_date(self.filename)

    def instrument(self):
        if 'VIR' in self.filename:
            return 'VIRS'
        elif 'MOD' in self.filename:
            return 'MODIS'
        else:
            print "Image is not VIRS or MODIS, check your file"
            sys.exit(1)

    def nan_percentage(self):
        nan_count = np.count_nonzero(~np.isnan(self.image()))
        return (nan_count / self.image().size) * 100

    def show(self, colorbar=True):
        plt.imshow(self.image())
        plt.title(self.filename)
        if colorbar:
            plt.colorbar()
        plt.show()


class LMImage(Image2D):
    """
        Land Mask (LM) Model
    """
    SENSOR = 'lm'

    # =================================================
    #
    #                Analysis Functions
    #
    # =================================================

    def percentage(self):
        """
            rType: dict()
        """
        percentages = {
            'timestamp': self.date(),
            LMImage.SENSOR: 0,
            'other': 0,
        }

        freqs = itemfreq(self.image())

        percentages['lm'] = (float(freqs[1][1]) / self.image().size) * 100
        percentages['other'] = (float(freqs[0][1]) / self.image().size) * 100

        return percentages

    def silhoutte(self):
        """
            Returns the border of the land mask.

            :rtype: ndarray
        """
        silhoutte = filters.generic_laplace(self.image(), sobel)
        condlist = [silhoutte < 0, silhoutte > 0]
        choicelist = [1, 1]
        return np.select(condlist, choicelist)


class SICImage(Image2D):

    SENSOR = 'mw_sic'

    # =================================================
    #
    #                 Analysis Functions
    #
    # =================================================

    def surface(self, ice_concentration_level=40, boolean=True):
        """
            Returns a boolean array that contains the area where there is ice.

            :params:
                :param ice_concentration_level: integer containing the ice co-
                                                ncencentration level. Defaults
                                                to 40 because at this level is
                                                ice and not water, other leves
                                                can be used for different types
                                                of analysis.
                :param boolean: flag to tell this function to return a boolean
                                array. By default is True.
            :rType: ndarray
        """

        # Converto boolean ndarray, ice is marked as True and for it to be true
        # we are assuming that sea ice above 40
        sea_ice = [self.image() > ice_concentration_level][0]
        if not boolean:
            return sea_ice.astype(int)
        return sea_ice

    def percentage(self):
        """
            rType: dict()
        """
        percentages = {
            "timestamp": self.title,
            "ice": 0,
            "other": 0,
        }

        sea_ice = self.surface()
        freqs = itemfreq(sea_ice)

        percentages['ice'] = (float(freqs[1][1]) / self.image().size) * 100
        percentages['other'] = (float(freqs[0][1]) / self.image().size) * 100

        return percentages


class SSTImage(Image2D):
    """
        Sea Surface Temperature ('sst') Model
    """
    SENSOR = 'sst'

    def instrument(self):
        return "VIRS"


class NPRImage(Image2D):
    """
        Microwave Normalized Polarization Ratio ('mw_npr') Model
    """
    SENSOR = 'mw_npr'


class NGRImage(Image2D):
    """
        Microwave Normalized Gradient Ratio ('mw_ngr') Model
    """
    SENSOR = 'mw_ngr'


class TEMPImage(Image2D):
    """
        Ice Surface Temperature ('temp') Model
    """
    SENSOR = 'temp'

    def instrument(self):
        return "MODIS"

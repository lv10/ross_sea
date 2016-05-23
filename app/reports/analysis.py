import sys

import numpy as np

from tools import data
from matplotlib import pyplot as plt
from app.models import SICImage as SIC, LMImage as LM


def day_image(instrument, lense):
    """
        Using histogram matching come up with an image for the day.

        :params:
            :param instrument_id: Integer that tells the function which of the
                                  instruments it should use to get the list of
                                  names. The integer is mapped to INSTRUMENT
                                  constant/map.
            :param lense: string with the key/lense to be used. Options are
                          mw_sic, lm
    """

    MAX_NAN_PERCENTAGE = 10.00

    if instrument is None:
        print "Provide an instrument id, see tools/data.py for details."
        sys.exit(1)

    files = data.file_names(data.INSTRUMENT_MAP.get(instrument))

    if len(files) == 0:
        print "There are no files to be analyzed. Check file path"
        sys.exit(1)

    matched = None
    for idx, f in enumerate(files):

        if (idx + 1) >= len(files):
            return matched

        #Load first VIRS file
        if matched is None:
            if lense == 'mw_sic':
                matched = SIC(f)
            if lense == 'lm':
                matched = LM(f)

            # Calculate NaN's percentage
            if matched.nan_percentage() > MAX_NAN_PERCENTAGE:
                matched = None
                continue
            else:
                matched = matched.image()

        #Load second VIRS file
        if lense == 'mw_sic':
            template = SIC(files[idx+1])
        if lense == 'lm':
            template = LM(files[idx+1])

        # Calculate NaN's percentage
        if template.nan_percentage() > MAX_NAN_PERCENTAGE:
            continue
        else:
            # match the files
            matched = hist_match(matched, template.image())

def single_histmatch_analysis(source, template, side_by_side=False):
    """
        Show a histogram match figure that includes Source, template, matched
        and the histogram.

        :params:
            :param source: Image2D or ImageND representing the source image.
            :param template: Image2D or ImageND representing the template image.
            :param side_by_side: bool flag to show side by side the 2 plots
    """

    matched = hist_match(source.image(), template.image())

    # Empirical CDF axes of source, template and histogram
    x1, y1 = ecdf(source.image().ravel())
    x2, y2 = ecdf(template.image().ravel())
    x3, y3 = ecdf(matched.ravel())

    if side_by_side:
        fig = plt.figure()
        fig.suptitle(
            "1. {0}. 2. {1}. 3. Histogram Match".format(
                source.filename, template.filename),
            fontsize=14
        )

        fig.add_subplot(1, 3, 1)
        plt.imshow(source.image())

        fig.add_subplot(1, 3, 2)
        plt.imshow(template.image())

        fig.add_subplot(1, 3, 3)
        plt.imshow(matched)
    else:
        fig, axes = plt.subplots(2, 2)
        fig.subplots_adjust(hspace=0.6, wspace=0.22)

        axes[0][0].imshow(source.image())
        axes[0][0].set_title("Source: {0}".format(source.title))

        axes[0][1].imshow(template.image())
        axes[0][1].set_title("Template: {0}".format(template.title))

        axes[1][0].imshow(matched)
        axes[1][0].set_title("Hist. Mactch of Source and Template")

        # Red dashes for MODIS. Blue dots for VIRS
        axes[1][1].plot(x1, y1, 'r--', x2, y2, 'b:')
        axes[1][1].set_title("Hist. Mactch of Source and Template")

    plt.show()


def histmatch_plot(source, template, multi_plots=False):
    """
        Show a histogram for the histogram match of two images.

        :params:
            :param source: Image2D or ImageND representing the source image.
            :param template: Image2D or ImageND representing the template image.
            :param sensor: String representing sensor to be used by source and
                           and template.
    """

    matched = hist_match(source.image(), template.image())

    # Empirical CDF axes of source, template and histogram
    x1, y1 = ecdf(source.image().ravel())
    x2, y2 = ecdf(template.image().ravel())
    x3, y3 = ecdf(matched.ravel())

    if multi_plots:
        fig, (ax1, ax2, ax3) = plt.subplots(3, sharex=True, sharey=False)
        fig.suptitle("1. MODIS. 2. VIRS. 3. Histogram Match", fontsize=14)

        ax1.plot(x1, y1)
        ax1.set_title('Source - {0}'.format(source.filename))

        ax2.plot(x2, y2)
        ax2.set_title('Reference - {0}'.format(source.filename))

        ax3.plot(x3, y3)
        ax3.set_title('Histogram Match')

        # Fine-tune figure; make subplots close to each other and hide x ticks
        # for all but bottom plot.
        fig.subplots_adjust(hspace=0)
        plt.setp([a.get_xticklabels() for a in fig.axes[:-1]], visible=False)
    else:
        plt.plot(x1, y1, 'r--', x2, y2, 'b:')
        plt.title("Histogram for {0} and {1}".format(source.title, template.title))

    plt.show()

def hist_match(source, template):
    """
        Adjust the pixel values of a grayscale image such that its histogram
        matches that of a target image

        :params:
            :param source: np.ndarray Image to transform; the histogram is
                           computed over the flattened
            :param template: np.ndarray Template image; can have different
                             dimensions to source
        :return: match output array, the transformed output image
        :rtype: np.ndarray
    """

    oldshape = source.shape

    source = source.ravel()
    template = template.ravel()

    # get the set of unique pixel values and their corresponding indices and
    # counts
    s_values, bin_idx, s_counts = np.unique(
        source, return_inverse=True, return_counts=True)
    t_values, t_counts = np.unique(template, return_counts=True)

    # take the cumsum of the counts and normalize by the number of pixels to
    # get the empirical cumulative distribution functions for the source and
    # template images (maps pixel value --> quantile)
    s_quantiles = np.cumsum(s_counts).astype(np.float64)
    s_quantiles /= s_quantiles[-1]
    t_quantiles = np.cumsum(t_counts).astype(np.float64)
    t_quantiles /= t_quantiles[-1]

    # interpolate linearly to find the pixel values in the template image
    # that correspond most closely to the quantiles in the source image
    interp_t_values = np.interp(s_quantiles, t_quantiles, t_values)

    return interp_t_values[bin_idx].reshape(oldshape)


def ecdf(x):
    """
        convenience function for computing the empirical CDF
    """
    vals, counts = np.unique(x, return_counts=True)
    ecdf = np.cumsum(counts).astype(np.float64)
    ecdf /= ecdf[-1]
    return  vals, ecdf

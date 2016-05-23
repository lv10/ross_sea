# ============================================================================
#
#
#                            Sea Ice Report
#
#
# ============================================================================

import sys

import numpy as np
from pandas import DataFrame
from scipy.stats import itemfreq
from matplotlib import pyplot as plt
from scipy.ndimage import filters, sobel

from tools import data
from app.models import LMImage as LM
from app.models import SICImage as SIC
from app.reports.analysis import day_image, hist_match


# ====================================================================
#                       Basic Statistical Analysis
# ====================================================================


def land_sic_overlap(lm_image, sic_image):
    """
        Show Sea Ice Concentration and Land Mask together. This figure shows
        the overlaps between mw_sic and lm.
    """

    lm = lm_image
    sic = sic_image

    sic_surface = sic.surface(boolean=False)
    lm_surface = lm.image()
    condlist = [lm_surface == 1]
    choicelist = [3]
    merge = np.add(sic_surface, np.select(condlist, choicelist))
    freqs = itemfreq(merge)

    # Pie Chart config params
    labels = "Sea Water", "Sea Ice", "Land", "Land - Sea Ice Overlap"
    colors = ["blue", "lightblue", "yellow", "red"]
    values = [freqs[0][1], freqs[1][1], freqs[2][1], freqs[3][1]]

    # Make and cofigure figure to be displayed
    fig, axes = plt.subplots(1, 2)

    fig.subplots_adjust(hspace=0.3, wspace=0.05)

    #populate each axis of the figure
    axes[0].imshow(merge)
    axes[0].set_title("Sea Ice and Land Mask")
    axes[1].pie(values, explode=[0.1, 0.1, 0.1, 0.4], labels=labels,
                colors=colors, shadow=True, autopct='%1.2f%%')
    plt.show()


def land_sic_overlap_timeseries(instrument,
                                title="Land-Sea Ice Border Variations"):
    """
        Time Series that shows the percentage variations of the land mask
        border given the expansion of sea ice in VIRS.
    """

    files = data.file_names(instrument_id=data.INSTRUMENT_MAP.get(instrument))
    out = []

    for idx, mat in enumerate(data.mat_generator(files)):

        sic = SIC(files[idx])
        lm = LM(files[idx])

        sic_surface = sic.surface(boolean=False)
        lm_surface = lm.silhoutte()

        silhoutte_freq = itemfreq(lm_surface)
        border = silhoutte_freq[1][1]

        merge = np.add(sic_surface, lm_surface)
        merge_freq = itemfreq(merge)
        intercept = merge_freq[2][1]

        land_ice_overlap = (float(intercept) / border) * 100
        temp = {'timestamp': lm.title, 'intercept': land_ice_overlap}
        out.append(temp)

    index = [elem['timestamp'] for elem in out]
    df = DataFrame(out, index=index)
    sdf = df.sort_values(by='timestamp')
    sdf.plot(title=title)
    plt.show()


def time_series(instrument='vir', title="SIC Percentage Changes"):
    """
        Show the change over time in sea ice conectration level by displaying
        a graph of the percentage change over time in sea ice concentration.

        :params:
            :param instrument: use the tools/data.py map to choose the right
                               instrument. defaults to vir.
    """

    # VIRS or Modis files
    files = data.file_names(instrument_id=data.INSTRUMENT_MAP[instrument])

    out = []

    for idx, mat in enumerate(data.mat_generator(files)):
        sic = SIC(files[idx])
        out.append(sic.percentage())

    index = [elem['timestamp'] for elem in out]
    df = DataFrame(out, index=index)
    sdf = df.sort_values(by='timestamp')
    sdf.plot(title=title)
    plt.show()


def surface_analysis(sic_image, save=False, path=None):
    """
        Shows the difference in Sea Ice Concentration for one image by
        showing a subplot that includes the original image the sea ice in
        black and white.

        :params:
            :param sic_image: SICImage, the sea ice concentration image object
                              that contains an image's information.
            :param save: boolean to save
    """

    sic = sic_image
    pos1, pos2, pos3 = (221, 222, 223)

    seaice_surface = sic.surface()

    figure = plt.figure()
    figure.suptitle(
        "Sea Ice concentration and Surface for {0}".format(sic.filename))

    original = plt.subplot(pos1)
    original.set_title("{0}".format(sic.title))
    org = original.imshow(sic.image())
    figure.colorbar(org, orientation="vertical")

    sea_ice_surface = plt.subplot(pos2)
    sea_ice_surface.set_title("Sea Ice Surface".format(sic.title))
    sea_ice_surface.imshow(seaice_surface)

    silhoutte = plt.subplot(pos3)
    silhoutte.set_title("Generic Laplace - Ice silhoutte")
    silhoutte.imshow(
        filters.generic_laplace(seaice_surface, sobel), cmap='Greys_r')

    plt.show()


def silhoutte(img):
    """
        Show's the silhoutte of the area where sea ice is located. The final
        result is shown in black ond white.
    """

    if isinstance(img, SIC):
        seaice_surface = img.surface()
        im = filters.generic_laplace(seaice_surface, sobel)
        #TODO: The output can be more clear, we need to find a filter that
        #      better connects the edges of the output.
        plt.imshow(im, cmap='Greys_r')
        plt.title('Sea Ice Concentration (mw_sic) silhoutte')
    elif isinstance(img, LM):
        plt.imshow(img.silhoutte(), cmap='Greys', interpolation='nearest')
        plt.title('Land Mask (lm) silhoutte')
    else:
        print "The image passed is not SICImage or LMImage"
        sys.exit(1)

    plt.show()


def distribution(img):
    """
        Shows a pie chart with the sea ice or land mask percentage on a given
        image/time of the day.
    """

    percentages = img.percentage()

    if isinstance(img, SIC):
        labels = 'Ice', 'other'
        colors = ['lightskyblue', 'yellowgreen']
        values = [percentages['ice'], percentages['other']]
        plt.pie(values, explode=[0.1, 0], labels=labels, colors=colors,
                shadow=True, autopct='%1.2f%%')
        plt.title('SIC (mw_sic) Distribution - {0}'.format(img.title))

    elif isinstance(img, LM):
        labels = 'Land', 'Other'
        colors = ['yellowgreen', 'lightskyblue']
        values = [percentages['lm'], percentages['other']]
        plt.pie(values, explode=[0.1, 0], labels=labels, colors=colors,
                shadow=True, autopct='%1.2f%%')
        plt.title('Land Mask (lm) Distribution - {0}'.format(img.title))
    else:
        print "The image passed is not SICImage or LMImage"
        sys.exit(1)

    plt.axis('equal')
    plt.show()


# ====================================================================
#                  Histogram Matching Analysis
# ====================================================================


def unified_day_image(lense, interval=20):
    """
        :params:
            :param lense: string with the key/lense to be used. Options are
                          mw_sic, lm
            :param interval: integer, that indicates the maximum time interval
                             between pictures of different instruments. This
                             interval is in minutes.
    """

    virs_files = data.file_names(data.INSTRUMENT_MAP.get('vir'))
    modis_files = data.file_names(data.INSTRUMENT_MAP.get('mod'))

    processed = list()
    titles = list()

    for idx, vir in enumerate(virs_files):

        if idx >= len(virs_files):
            break

        virs_date = data.parse_date(vir)
        modis_date = data.parse_date(modis_files[idx])

        if data.date_dff(virs_date, modis_date) <= interval:
            source = SIC(virs_files[idx])
            template = SIC(modis_files[idx])

            out = hist_match(source.image(), template.image())
            processed.append(out)
            titles.append("{0} and {1}".format(source.title, template.title))

    # Make and cofigure figure to be displayed
    if len(processed) == 0:
        print "No pictures were processed, consider changing the interval"
        sys.exit(0)
    elif len(processed) == 1:
        plt.imshow(processed[0])
    else:
        boxes = len(processed)
        if boxes % 2 > 0:
            boxes = boxes + 1
        levels = boxes / 2

        fig, axes = plt.subplots(levels, 2)
        fig.subplots_adjust(hspace=0.5, wspace=0.2)
        fig.suptitle(
            "VIRS-MODIS Hist. Matched {0} mins apart with {1} images".format(
                interval, len(processed)),
            fontsize=20)

        if len(processed) <= 2:
            for idx, img in enumerate(processed):
                axes[idx].imshow(processed[idx])
                axes[idx].set_title(titles[idx])
        else:
            idx = 0
            for level in range(levels):
                for box in range(2):
                    if idx < len(processed):
                        axes[level][box].imshow(processed[idx])
                        axes[level][box].set_title(
                            "{0} and {1}l".format(titles[idx], tiltes[idx]))
                        idx += 1
                    else:
                        break

    plt.show()


def show_day_images_by_instrument():
    """
        Show day images after histogram matching by instrument virs and modis
    """

    virs = day_image(instrument='vir', lense="mw_sic")
    modis = day_image(instrument='mod', lense="mw_sic")

    # Make and cofigure figure to be displayed
    fig, axes = plt.subplots(1, 2)
    fig.subplots_adjust(hspace=0.3, wspace=0.05)

    #populate each axis of the figure
    axes[0].imshow(virs)
    axes[0].set_title("VIRS")
    axes[1].imshow(modis)
    axes[1].set_title("MODIS")

    plt.show()

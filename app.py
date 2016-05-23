import sys

import argparse
from matplotlib import pyplot as plt

from app.models import SICImage as SIC, LMImage as LM, TEMPImage as TEMP, \
    SSTImage as SST, NPRImage as NPR, NGRImage as NGR, IbandImage as IBAND, \
    MbandImage as MBAND, FcImage as FC
from app.reports.analysis import hist_match, day_image, histmatch_plot, \
    single_histmatch_analysis
from app.reports.color_report import color_clusters, blue_channels, rgb, \
    find_water
from app.reports.sic_report import time_series, land_sic_overlap_timeseries, \
    show_day_images_by_instrument, unified_day_image, surface_analysis, \
    silhoutte, distribution, land_sic_overlap


def main():

    parser = argparse.ArgumentParser(description="Ross Sea Ice Project")

    parser.add_argument(
        "--instrument", "-i", action='store', dest='instrument',
        help="Instrument vir or mod (VIRS or MODIS)")

    # Show an image
    # =============
    parser.add_argument(
        '--show', action='store_true', dest='show', help="Shown Image Flag")

    # SIC Report
    # ==================
    parser.add_argument(
        '--sic', action='store_true', dest='sic', default=False,
        help="Run SIC Report")

    # SIC or LM distribution
    parser.add_argument(
        '-d', action='store_true', dest='distribution', default=False,
        help="Run SIC or LM distribution at a given time of the day")

    # SIC or LM silhoutte
    parser.add_argument(
        '-s', action='store_true', dest='silhoutte', default=False,
        help="Run SIC or LM silhoutte at a given time of the day")

    # SIC surface
    parser.add_argument(
        '-srf', action='store_true', dest='surface', default=False,
        help="Run SIC surface analysis at a given time of the day")

    parser.add_argument(
        '-overlap', action='store_true', dest='overlap', default=False,
        help="Run SIC overlap analysis for two images")

    # Histogram Matching
    # ==================

    parser.add_argument(
        '--hist', action='store_true', dest='hist',
        help="Run Histogram matching on 2 files add flags -img and -img2")

    # Image of the day using histogram matching
    parser.add_argument(
        '--imgday', action='store_true', dest='imgday',
        help="Get image for the day using histogram matching")

    parser.add_argument(
        '-shist', action='store_true', dest='shist',
        help="Show a Histogram matching for two images given a sensor")

    parser.add_argument(
        '-histplot', action='store_true', dest='histplot',
        help="Plot a histogram for a Histogram matching")

    parser.add_argument(
        '-multiplot', action='store_true', dest='multiplot',
        help="Plot the histograms for a Histogram matching")

    parser.add_argument(
        '-sideplot', action='store_true', dest='sideplot',
        help="Plot side by side the results of histogram matching")

    # Color Channel Report
    # ====================
    parser.add_argument(
        '--color', '-c', action='store_true', dest='color', default=False,
        help="Use to enable Color Analysis functions")

    parser.add_argument(
        '-rgb', action='store_true', dest='rgb', default=False,
        help="Get the RGB of ibands, mbands or fc")

    parser.add_argument(
        '-water', action='store_true', dest='water', default=False,
        help="Find water using the 3 bands from mbands")

    # General args
    # ============
    parser.add_argument('--sensor', action='store', dest='sensor',
                        help="sensors like 'mw_sic, 'lm'")
    parser.add_argument(
        '-img', action='store', dest='img', help="Image to be matched")
    parser.add_argument(
        '-img2', action='store', dest='img2', help="Image Template")

    args = parser.parse_args()

    if args.sic:
        sic_report(args.instrument.lower())
    if args.overlap:
        land_ice_overlap(args.img)
    elif args.hist:
        histogram_matching(args.sensor, args.img, args.img2)
    elif args.imgday:
        instrument_image_of_the_day(args.instrument.lower(), args.sensor)
    elif args.color:
        color_report(args.img)
    elif args.rgb:
        show_rgb(args.img, args.sensor)
    elif args.distribution:
        sic_or_lm_distribution(args.img, args.sensor)
    elif args.silhoutte:
        sic_or_lm_silhoutte(args.img, args.sensor)
    elif args.surface:
        sic_surface_analysis(args.img)
    elif args.show:
        img_show(args.img, args.sensor)
    elif args.shist:
        single_histogram_matched(args.img, args.img2, args.sensor)
    elif args.histplot:
        single_histogram_matched(
            args.img, args.img2, args.sensor, plot_only=True)
    elif args.multiplot:
        single_histogram_matched(
            args.img, args.img2, args.sensor, multi_plots=True)
    elif args.sideplot:
        single_histogram_matched(
            args.img, args.img2, args.sensor, side_plot=True)
    elif args.water:
        show_water(args.img)
    else:
        print "Mer Mer Mer"


def sic_report(instrument, sensor='mw_sic', interval=20):
    """
        :params:
            :param interval: minutes interval for unified day image
    """

    print "\nRunning SIC Report"

    if instrument == 'vir':
        title = "VIRS"
    elif instrument == 'mod':
        title = "MODIS"
    else:
        print "Invalid instrument"
        sys.exit(1)

    # Run the time series report
    msg = "\n{0} - SIC Percentage Changes".format(title)

    print msg
    time_series(
        instrument=instrument,
        title=msg
    )

    # Run the time series to show percentage variations of the Land Mask's
    # border while being covered by sea ice.
    msg = "\n{0} - Land Mask Border Percentage Change Overtime".format(title)
    print msg

    land_sic_overlap_timeseries(
        instrument=instrument,
        title=msg
    )

    # # Run Histogram Matching by day for each instrumenent VIRS and MODIS
    print "\nVIRS & MODIS day image after histogram matching"
    show_day_images_by_instrument()

    # Run unified day image from both instruments using VIRS as reference and
    # only implementing histogram matching to VIRS-MODIS images that are at
    # most <internval> mins apart
    print "\nVIRS-MODIS histogram matched on Images {0} mins apart".format(
        interval)
    unified_day_image(sensor, interval)


def land_ice_overlap(image):
    """
        :params:
            :param image: string with the filename of an image
    """
    print "Preparing Image Overlap for {0}".format(image)

    lm = LM(image)
    sic = SIC(image)

    land_sic_overlap(lm, sic)


def color_report(image):
    """
        :params:
            :param image: string with the filename of an image
    """

    print "\nColor Report"

    lm = LM(image)
    fc = FC(image)
    ibands = IBAND(image)
    mbands = MBAND(image)

    print "\nK-means clustering for {0}".format(image)
    color_clusters(ibands, mbands, fc, lm)

    print "\nBlue Channels for {0}".format(image)
    blue_channels(ibands, mbands, fc)

    print "\nRGB for {0}".format(image)
    for img in [fc, ibands, mbands]:
        rgb(img)


def show_rgb(image, sensor):
    """
        :params:
            :param image: string with the filename of an image
    """
    print "Preparing RGB for {0} using {1}".format(image, sensor)
    if sensor == 'ibands':
        image = IBAND(image)
    elif sensor == 'mbands':
        image = MBAND(image)
    elif sensor == 'fc':
        image = FC(image)
    else:
        print "Sensor {0} not available yet".format(sensor)

    # disply rgb
    rgb(image)


def show_water(image):
    """
        :params:
            :param image: string with the filename of an image
    """
    mbands = MBAND(image)
    ibands = IBAND(image)
    lm = LM(image)
    find_water(mbands, ibands, lm)


def histogram_matching(sensor, img_a, img_b):
    """
        :params:
            :param sensor: string which is a key to determine which image
                          object to load.
            :param img_a: string with the filename for img_a, it assumes the
                          the filename is correct and the file exists
            :param img_b: string with the filename for img_b, it assumes the
                          the filename is correct and the file exists
                """

    print "\nHistogram Matching for {0} and {1}".format(img_a, img_b)

    title = "Histogram Matching for:\n{0} and {1}".format(img_a, img_b)

    if sensor == 'mw_sic':
        source = SIC(img_a)
        template = SIC(img_b)
    elif sensor == 'lm':
        source = LM(img_a)
        template = LM(img_b)
    elif sensor == 'sst':
        print "Support for SST hasn't been implemented yet"
        sys.exit(0)
    else:
        print "Support for {0} hasn't been implemented yet".format(sensor)
        sys.exit(1)

    matched = hist_match(source.image(), template.image())
    plt.imshow(matched)
    plt.title(title)
    plt.show()


def single_histogram_matched(src, template, sensor, plot_only=False,
                             multi_plots=False, side_plot=False):
    """
        Show histogram matching at work with 2 images given a sensor.
    """
    print "Preparing Histogram match for {0} and {1}".format(src, template)

    if sensor == 'mw_sic':
        img = SIC(src)
        img2 = SIC(template)
    elif sensor == 'mw_ngr':
        img = NPR(src)
        img2 = NPR(template)
    elif sensor == 'mw_ngr':
        img = NPR(src)
        img2 = NPR(template)
    elif sensor == 'lm':
        img = LM(src)
        img2 = LM(template)
    else:
        print "{0} doesn't have support yet".format(sensor)

    if multi_plots:
            histmatch_plot(img, img2, multi_plots=True)
    elif plot_only:
        histmatch_plot(img, img2)
    elif side_plot:
        single_histmatch_analysis(img, img2, side_by_side=True)
    else:
        single_histmatch_analysis(img, img2)


def instrument_image_of_the_day(instrument, sensor):

    if instrument == 'vir':
        title = "VIIS - Image of the day"
    if instrument == 'mod':
        title = "MODIS - Image of the day"

    matched = day_image(instrument, sensor)
    plt.imshow(matched)
    plt.title(title)
    plt.show()


def sic_or_lm_distribution(image, sensor):
    """
        :param sensor: string with the sensor to be used, options:
                       - mw_sic
                       - lm
    """
    print "Preparing pie chart {0} percentage using {1}".format(image, sensor)
    if sensor == 'mw_sic':
        img = SIC(image)
    if sensor == 'lm':
        img = LM(image)

    distribution(img)


def sic_or_lm_silhoutte(image, sensor):
    """
        :param sensor: string with the sensor to be used, options:
                       - mw_sic
                       - lm
    """
    print "Preparing silhoutte for {0} using {1}".format(image, sensor)
    if sensor == 'mw_sic':
        img = SIC(image)
    if sensor == 'lm':
        img = LM(image)

    silhoutte(img)


def sic_surface_analysis(image):
    print "Preparing Surface anylysis for {0}".format(image)
    img = SIC(image)
    surface_analysis(img)


def img_show(image, sensor):

    if not sensor:
        print "Sensor missing. Specify one with -sensor"
        sys.exit(1)

    if sensor == "mw_sic":
        image = SIC(image)
    elif sensor == "lm":
        image = LM(image)
    elif sensor == "mw_npr":
        image = NPR(image)
    elif sensor == "mw_ngr":
        image = NGR(image)
    elif sensor == "sst":
        image = SST(image)
    elif sensor == "temp":
        image = TEMP(image)
    elif sensor == 'ibands':
        image = IBAND(image)
    elif sensor == 'mbands':
        image = MBAND(image)
    elif sensor == 'fc':
        image = FC(image)
    else:
        print "Sensor not identified"
        sys.exit(1)

    image.show()

if __name__ == '__main__':
    main()

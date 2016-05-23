import os
import sys
import time

from scipy.io import loadmat

BASE_DIR = os.path.dirname(os.path.dirname(__file__))
DATA_DIR = os.path.join(BASE_DIR, 'data')

INSTRUMENT = {
    0: "VIR",
    1: "MOD",
    2: "both"
}

INSTRUMENT_MAP = {
    "vir": 0,
    "mod": 1,
    "both": 2
}


def mat_generator(file_list=[]):
    """
        Generates a file from the data directory from a list of file names

        :params:
            :param file_list: List of files (names) that will be yielded

        :rType: Genarator
    """

    if not file_list:
        print "File list is empty, no mat files will be generated"
    else:
        for f in file_list:
            yield mat_file(os.path.join(DATA_DIR, f))


def mat_file(filepath=None):
    """
        Returns a dictionary whith the contents of the .mat file. This is an
        auxiliary function, that can be used outside data.py context.

        :params:
            :param filepath: Set to None by default, contains the path where
                             where the mat file to be loaded is

        :rType: dict()
    """

    if not filepath or not os.path.isfile(filepath):
        print "Error: File {0} doesn't exist".format(filepath)
        sys.exit(1)
    else:
        try:
            return loadmat(filepath)
        except IOError, ioex:
            print "mat_file: {0}".format(os.strerror(ioex.errno))


def file_names(instrument_id=2):
    """
        Returns a list of the file names in the data directory. This is an
        auxiliary function, that can be used outside data.py context.

        :params:
            :param instrument_id: Integer that tells the function which of the
                                  instruments it should use to get the list of
                                  names. The integer is mapped to INSTRUMENT
                                  constant/map.
    """

    files = os.listdir(DATA_DIR)

    if instrument_id == 2:
        return sorted([f for f in files])
    else:
        return sorted([f for f in files if INSTRUMENT[instrument_id] in f])


def parse_date(filename):
    """
        From a string passed that in the format of the file name convert it
        and return in time.struct_time.

        :params:
            :param filename: string that represents a filename, date is in the
                             in filname.

        :return: time, a 9-valued tuple: ( year, month, day, hour, minute,
                                           second, day of week, day of year,
                                           dst-flag )
        :rtype: time.struct_time, tuple
    """
    date_str = filename[2:-13]
    year, jday, hour = date_str.split('_')
    year, jday, hr, mins = int(year), int(jday), int(hour[:2]), int(hour[2:])

    AUTO_DETECT_DAYLIGHT = -1
    return time.struct_time(
        (year, 0, 0, hr, mins, 0, 0, jday, AUTO_DETECT_DAYLIGHT)
    )


def date_dff(date_a, date_b):
    """
        :params:
            :param date_a: time.struct_time
            :param date_a: time.struct_time

        :return: the difference in minutes between two dates
        :rtype: float
    """
    return abs((time.mktime(date_a) - time.mktime(date_b)) / 60)

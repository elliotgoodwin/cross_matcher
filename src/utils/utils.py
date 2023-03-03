import numpy as np


def hms2dec(h, m, s):
    """
    Convert right-ascension in hms notation to decimal degrees.

    Args:
        h (int): hour angle
        m (int): arcminutes (degrees/60)
        s (float): arcseconds (degrees/60**2)

    Returns:
        float: right ascension in decimal degrees
    """
    ONE_HOUR_IN_DEGREES = 15
    time_in_hours = h + m / 60 + s / (60**2)
    return ONE_HOUR_IN_DEGREES * time_in_hours


def dms2dec(d, m, s):
    """
    Converts declination in dms notation to decimal degrees.

    Args:
        d (float): degrees
        m (float): arcminutes (degrees/60)
        s (float): arcseconds (degrees/60**2)

    Returns:
        float: declination in decimal degrees
    """
    return (abs(d) + m / 60 + s / (60**2)) * (d / abs(d))


def angular_dist(r1, d1, r2, d2, radians=False):
    """
    Computes the angular distance from right ascension
    and declination using the Haversine formula.

    Args:
        r1 (float): right ascension in decimal degrees for object 1
        d1 (float): declination in decimal degrees for object 1
        r2 (float): right ascension in decimal degrees for object 2
        d2 (float): declination in decimal degrees for object 2
        radians (bool, optional): True if using radians,
                                  False if using degrees.
                                  Defaults to False.

    Returns:
        float: angular distance between object 1 and object
               2 in decimal degrees
    """
    if radians:
        a = np.sin(np.abs(d1 - d2) / 2) ** 2
        b = np.cos(d1) * np.cos(d2) * np.sin(np.abs(r1 - r2) / 2) ** 2
        angle = 2 * np.arcsin(np.sqrt(a + b))
        return np.degrees(angle)

    a = np.sin(np.abs(np.radians(d1) - np.radians(d2)) / 2) ** 2
    b = (
        np.cos(np.radians(d1))
        * np.cos(np.radians(d2))
        * np.sin(np.radians(np.abs(r1 - r2) / 2)) ** 2
    )

    angle = 2 * np.arcsin(np.sqrt(a + b))

    return np.degrees(angle)


def import_dat(dat_file):
    """
    Load catalogue from fixed-width .dat file.

    Args:
        dat_file (string): Path to .dat file

    Returns:
        list([float, float]): Each element contains a list with two float
                              values which correspond to the right ascension
                              and declination (both in decimal degrees) of
                              the catalogue object
    """

    cat = np.loadtxt(dat_file, usecols=range(1, 7))

    data = []
    for (h1, m1, s1, d2, m2, s2) in cat:
        # h1, m1, s1 is right ascension in hms notation
        # d2, m2, s2 is declination in dms notation
        data.append([hms2dec(h1, m1, s1), dms2dec(d2, m2, s2)])

    return data


def import_csv(csv_file):
    """
    Load catalogue from .csv file

    Args:
        csv_file (str): Path to .csv file

    Returns:
        list([float, float]): Each element contains a list with two float
                              values which correspond to the right ascension
                              and declination (both in decimal degrees) of
                              the catalogue object
    """

    cat = np.loadtxt(csv_file, delimiter=",", skiprows=1, usecols=[0, 1])

    data = []
    for (ra, dec) in cat:
        data.append([ra, dec])

    return data

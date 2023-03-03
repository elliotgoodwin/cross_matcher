import numpy as np
import src.utils.utils as utils


def find_closest(cat, ra, dec, radians=False):
    """
    Finds the closest object inside a catalogue, cat, to a given point (ra, dec)

    Args:
        cat (list([float, float])): Each element contains a list with two float
                                    values which correspond to the right ascension
                                    and declination (both in decimal degrees) of
                                    the catalogue object
        ra (float): Right ascension in decimal degrees of object to cross-match with
                    the catalogue
        dec (float): Declination in decimal degrees of object to cross-match with the
                     catalogue
        radians (bool, optional): True if using radians, False if using degrees.
                                  Defaults to False.

    Returns:
        min_id (int): The id of the catalogue object with the minimum distance to the
                      input coordinates
        min_dist (float): The distance between the catalogue object with `min_id` and
                          the input coordinates
    """
    min_dist = np.inf
    min_id = None

    for id1, (ra1, dec1) in enumerate(cat):
        if radians:
            dist = utils.angular_dist(ra1, dec1, ra, dec, radians=True)
        else:
            dist = utils.angular_dist(ra1, dec1, ra, dec)

        if dist < min_dist:
            min_id = id1
            min_dist = dist

    return min_id, min_dist


def naive_crossmatch(bss_cat, super_cat, max_dist):
    """
    Cross-matches objects in the bss catalogue to objects in the SuperCosmos
    catalogue. For each object in bss, we loop through all objects in super
    to find the object with the minimum distance from the bss object. If the
    distance is above the uncertainty (max_dist, related to the beam profile
    of the telescope and other factors) then there is no match.

    Args:
        bss_cat (list([float, float])): _description_
        super_cat (list([float, float])): _description_
        max_dist (float): _description_

    Returns:
        matches (list(tuple(int, int, float))): _description_
        no_matches (list(int)): _description_
    """
    matches = []
    no_matches = []

    for bss_id, (bss_ra, bss_dec) in enumerate(bss_cat):
        min_id, min_dist = find_closest(super_cat, bss_ra, bss_dec)

        if min_dist > max_dist:
            no_matches.append(bss_id)
        else:
            matches.append((bss_id, min_id, min_dist))

    return matches, no_matches


def numpy_crossmatch(bss_cat, super_cat, max_dist):
    """
    Essentially the same functino as naive_crossmatch(). The only difference
    here is that some effort has been made to avoid redundant computation and
    to use more effecient data structures for this task.

    Instead of lists we use numpy arrays. This allows us vectorise the coodinate
    conversion from degrees to radians. We move this outside the loop so that the
    conversion occurs once per set of coordinates as opposed to every call to
    find_closest()

    Args:
        bss_cat (list([float, float])): _description_
        super_cat (list([float, float])): _description_
        max_dist (float): _description_

    Returns:
        matches (list(tuple(int, int, float))): _description_
        no_matches (list(int)): _description_
    """
    matches = []
    no_matches = []

    # Convert bss_cat and super_cat to radians once outside the loop
    bss_cat = np.radians(np.asarray(bss_cat))
    super_cat = np.radians(np.asarray(super_cat))

    for bss_id, (bss_ra, bss_dec) in enumerate(bss_cat):
        min_id, min_dist = find_closest(super_cat, bss_ra, bss_dec, radians=True)

        if min_dist > max_dist:
            no_matches.append(bss_id)
        else:
            matches.append((bss_id, min_id, min_dist))

    return matches, no_matches

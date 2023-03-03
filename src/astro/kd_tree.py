import numpy as np
import src.utils.utils as utils
from scipy.spatial import KDTree


def KD_crossmatch(bss_cat, super_cat, max_dist):
    """
    For each element in bss_cat, the index of the nearest neighbour
    in super_cat is return providing their distance is below max_dist.
    The algorithm uses SciPy's implementation of the KDTree search
    algorithm [1].

    [1] - https://docs.scipy.org/doc/scipy/reference/generated/scipy.spatial.KDTree.html#scipy.spatial.KDTree

    Args:
        x_cat (list([float, float])): The right ascension and declination
                                      of items in a catalogue in radians.
        max_dist (float): The maximum distance to return a nearest
                          neighbour match.

    Returns:
        list([int|None]): For each child node in bss_tree, search through
                          super_tree to find matches, returning a list of
                          indexes of the matched objects in super_cat
    """
    bss_tree = KDTree(bss_cat, balanced_tree=False)
    super_tree = KDTree(super_cat, balanced_tree=False)
    return bss_tree.query_ball_tree(super_tree, r=max_dist)


def process_KD_crossmatch(match_indexes, bss_cat, super_cat):
    """
    Processes catalogues to return the formatted results from the
    list of match indexes.

    Args:
        match_indexes (list([int])): A list of lists where each element
                                     contains the integer index of the
                                     search catalogue's objects if there is
                                     a match, or an empty list if there was
                                     no match.
        x_cat (list([float, float])): The right ascension and declination
                                      of items in a catalogue in radians.

    Returns:
        list((int, int, float)): A list of tuples whose elements are the index
                                 of the input catalogue object, the index of the
                                 matched search catalogue object and the angular
                                 distance in degrees between the two objects.
        no_matches (list(int)): A list of integers corresponding to the index
                                of the input catalogue objects which weren't
                                matched to an object in the search catalogue
    """
    matches = []
    no_matches = []

    for bss_id, match_idx in enumerate(match_indexes):
        if match_idx == []:
            no_matches.append(bss_id)
        else:
            r1, d1 = bss_cat[bss_id]
            r2, d2 = super_cat[match_idx[0]]
            matches.append(
                (bss_id, match_idx[0], utils.angular_dist(r1, d1, r2, d2, radians=True))
            )
    return matches, no_matches

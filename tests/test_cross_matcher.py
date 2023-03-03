import pytest
import numpy as np
from src.astro import cross_matcher


def test_find_closest(super_cat):
    """
    Tests numerical output of the find_closest function with known values

    Args:
        super_cat (list([float, float])):
    """
    id, dist = cross_matcher.find_closest(super_cat, 175.3, -32.5)
    assert id == 268
    assert dist == 3.7669389663491515

    id, dist = cross_matcher.find_closest(super_cat, 32.2, 40.7)
    assert id == 20
    assert dist == 46.18843872662329


def test_naive_crossmatch(bss_cat, super_cat):
    """
    Tests numerical output of the test_naive_crossmatch function

    Args:
        bss_cat (list([float, float])): _description_
        super_cat (list([float, float])): _description_
    """
    matches, no_matches = cross_matcher.naive_crossmatch(
        bss_cat, super_cat, max_dist=40 / 3600
    )
    assert len(matches) == 151
    assert len(no_matches) == 9
    assert matches[0][2] == 0.00010988610938711933
    assert matches[2][1] == 4
    assert no_matches[2] == 10


def test_naive_vs_numpy_crossmatch(bss_cat, super_cat):
    """
    Tests the outputs of the naive and numpy implementations of the
    crossmatch algorithm

    Args:
        x_cat (list([float, float])): A list of lists of float elements
                                      which contain the right ascension and
                                      declination in degrees of catalogue objects
    """
    np_matches, np_no_matches = cross_matcher.numpy_crossmatch(
        bss_cat, super_cat, max_dist=40 / 3600
    )

    naive_matches, naive_no_matches = cross_matcher.naive_crossmatch(
        bss_cat, super_cat, max_dist=40 / 3600
    )

    assert len(np_no_matches) == len(naive_no_matches)
    assert np.round(np_matches[3][2], 5) == np.round(naive_matches[3][2], 5)
    assert np_no_matches == naive_no_matches

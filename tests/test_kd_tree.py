import pytest
import numpy as np
from src.astro import cross_matcher, kd_tree


def test_numpy_vs_kd_tree_crossmatch(bss_cat, super_cat):
    np_matches, np_no_matches = cross_matcher.numpy_crossmatch(
        bss_cat, super_cat, max_dist=40 / 3600
    )

    bss_cat = np.radians(np.asarray(bss_cat))
    super_cat = np.radians(np.asarray(super_cat))

    match_indexes = kd_tree.KD_crossmatch(bss_cat, super_cat, max_dist=40 / 3600)
    kd_matches, kd_no_matches = kd_tree.process_KD_crossmatch(
        match_indexes, bss_cat, super_cat
    )

    assert len(np_no_matches) == len(kd_no_matches)
    assert np_matches[:3] == kd_matches[:3]
    assert np_no_matches[:3] == kd_no_matches[:3]

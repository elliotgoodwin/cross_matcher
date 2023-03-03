import pytest
import numpy as np
import src.utils.utils as utils


def test_hms2dec():
    assert utils.hms2dec(23, 12, 6) == 348.025


def test_dms2dec():
    assert utils.dms2dec(22, 57, 18) == 22.955


def test_angular_dist():
    r1 = 21.07
    d1 = 0.1
    r2 = 21.15
    d2 = 8.2
    assert np.round(utils.angular_dist(r1, d1, r2, d2, radians=False), 3) == 8.100

    # Convert to radians
    r1 = np.radians(r1)
    d1 = np.radians(d1)
    r2 = np.radians(r2)
    d2 = np.radians(d2)
    assert np.round(utils.angular_dist(r1, d1, r2, d2, radians=True), 3) == 8.100


# def test_import_dat


# Test conversion to radians
# print(bss_cat[:3])
# bss_cat = np.radians( np.asarray(bss_cat) )
# super_cat = np.radians( np.asarray(super_cat) )
# print(bss_cat[:3])

# Test loading data
# Test shape of result
# Test sample of result values

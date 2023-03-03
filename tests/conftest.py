import pytest
import src.utils.utils as utils

"""
Define test fixtures, which our unit tests are able to request as arguments.

scope="session" loads the fixture once during the test session, re-uses the
contents across all tests, then destroys the fixture at the end of the test
session.
"""


@pytest.fixture(scope="session")
def super_cat():
    return utils.import_csv("./cats/super.csv")


@pytest.fixture(scope="session")
def bss_cat():
    return utils.import_dat("./cats/bss.dat")

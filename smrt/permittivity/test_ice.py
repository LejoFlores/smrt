
from nose.tools import raises
from nose.tools import eq_
# import warnings
import numpy as np

from smrt.permittivity.ice import ice_permittivity_matzler87
from smrt.permittivity.ice import _ice_permittivity_HUT
from smrt.permittivity.ice import _ice_permittivity_DMRTML
from smrt.permittivity.ice import _ice_permittivity_MEMLS
from smrt.core.error import SMRTError

# Input temperature array functionality removed. If ever needed, use numpy instead of math in ice.py, but slower.

# @raises(SMRTError)
# def test_zero_temperature_exception_raised():
#    ice_permittivity_matzler87(10e9, np.array([0]), 0, 0)


# This tests a warning is raised
# with warnings.catch_warnings(record=True) as w:
#     # Cause all warnings to always be triggered.
#     warnings.simplefilter("always")
#     # Trigger a warning.
#     ice_permittivity(np.array([230]), 10e9)
#     # Verify some things
#     assert len(w) == 1
#     assert 'Warning: temperature is below 240K. Ice permittivity is out of range of applicability' in str(w[-1].message)

# Test output of this module against output from MEMLS code
def test_real_ice_permittivity_output_matzler_temp_270():
    eps = ice_permittivity_matzler87(10e9, 270)
    np.testing.assert_allclose(eps.real, 3.1857, atol=1e-4)


# Test output of this module against output from MEMLS code
# Weaker tolerance for 250K as MEMLS calculation is based on freezing point temperature of 273K not 273.15K
def test_real_ice_permittivity_output_matzler_temp_250():
    eps = ice_permittivity_matzler87(10e9, 250)
    np.testing.assert_allclose(eps.real, 3.1675, atol=1e-3)


def test_imaginary_ice_permittivity_output_matzler_temp_270_freq_10GHz():
    eps = ice_permittivity_matzler87(10e9, 270)
    np.testing.assert_allclose(eps.imag, 9.093e-04, atol=1e-4)


def test_imaginary_ice_permittivity_output_matzler_temp_250_freq_10GHz():
    eps = ice_permittivity_matzler87(10e9, 250)
    np.testing.assert_allclose(eps.imag, 6.0571e-4, atol=1e-4)


def test_imaginary_ice_permittivity_output_matzler_temp_270_freq_20GHz():
    eps = ice_permittivity_matzler87(20e9, 270)
    np.testing.assert_allclose(eps.imag, 0.0017449, atol=1e-4)


def test_imaginary_ice_permittivity_output_matzler_temp_250_freq_20GHz():
    eps = ice_permittivity_matzler87(20e9, 250)
    np.testing.assert_allclose(eps.imag, 0.0012002, atol=1e-4)


def test_imaginary_ice_permittivity_output_matzler_temp_270_freq_30GHz():
    eps = ice_permittivity_matzler87(30e9, 270)
    np.testing.assert_allclose(eps.imag, 0.0025971, atol=1e-4)


def test_imaginary_ice_permittivity_output_matzler_temp_250_freq_30GHz():
    eps = ice_permittivity_matzler87(30e9, 250)
    np.testing.assert_allclose(eps.imag, 0.0017973, atol=1e-4)


def test_imaginary_ice_permittivity_output_matzler_temp_270_freq_40GHz():
    eps = ice_permittivity_matzler87(40e9, 270)
    np.testing.assert_allclose(eps.imag, 0.0034535, atol=1e-4)


def test_imaginary_ice_permittivity_output_matzler_temp_250_freq_40GHz():
    eps = ice_permittivity_matzler87(40e9, 250)
    np.testing.assert_allclose(eps.imag, 0.0023952, atol=1e-4)


# Test output of HUT version
def test_real_ice_permittivity_output_HUT():
    eps = _ice_permittivity_HUT(10e9, 270)
    eq_(eps.real, 3.18567)


# Test output of HUT version
def test_imaginary_ice_permittivity_output_HUT():
    eps = _ice_permittivity_HUT(10e9, 270)
    np.testing.assert_allclose(eps.imag, 8.86909246416410e-04, atol=1e-8)


# Test output of DMRT version
def test_real_ice_permittivity_output_DMRTML():
    eps = _ice_permittivity_DMRTML(10e9, 270)
    eq_(eps.real, 3.18567)


# Test output of DMRT version
def test_imaginary_ice_permittivity_output_DMRTML():
    eps = _ice_permittivity_DMRTML(10e9, 270)
    np.testing.assert_allclose(eps.imag, 9.0679820556720323e-04, atol=1e-8)


# Test output MEMLS version
def test_real_ice_permittivity_output_matzler_temp_270():
    eps = _ice_permittivity_MEMLS(10e9, 270, 0)
    eq_(eps.real, 3.18567)


# Test output MEMLS version
def test_imaginary_ice_permittivity_output_matzler_temp_270_freq_10GHz():
    eps = _ice_permittivity_MEMLS(10e9, 270, 0)
    np.testing.assert_allclose(eps.imag, 9.09298888985990e-04, atol=1e-8)


# Test output MEMLS version
def test_salty_imaginary_ice_permittivity_output_matzler_temp_270_freq_10GHz():
    eps = _ice_permittivity_MEMLS(10e9, 270, 50)
    np.testing.assert_allclose(eps.imag, 7.74334595964606, atol=1e-8)

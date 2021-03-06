# coding: utf-8

from nose.tools import raises
from nose.tools import eq_
from nose.tools import ok_
import numpy as np
import scipy.integrate

from smrt.emmodel.iba import IBA, IBA_MM, derived_IBA
from smrt.emmodel.rayleigh import Rayleigh
from smrt.core.error import SMRTError
from smrt.core.sensor import active
from smrt.inputs.sensor_list import amsre
from smrt import make_snow_layer
from smrt.emmodel import commontest, effective_permittivity

# import the microstructure
from smrt.microstructure_model.exponential import Exponential
from smrt.microstructure_model.independent_sphere import IndependentSphere
from smrt.microstructure_model.sticky_hard_spheres import StickyHardSpheres

tolerance = 1e-7
tolerance_pc = 0.05  # 5% error is allowable for differences from MEMLS values. Tests pass at 2%. Some fail at 1%.


def setup_func_sp():
    # Could import iba_example, but hard code here in case iba_example changes
    # ### Make a snow layer
    exp_lay = make_snow_layer(layer_thickness=0.2, microstructure_model=Exponential, density=250, temperature=265, corr_length=5e-4)
    return exp_lay


def setup_func_indep(radius=5e-4):
    # ### Make a snow layer
    indep_lay = make_snow_layer(layer_thickness=0.2, microstructure_model=IndependentSphere, density=250, temperature=265, radius=radius)
    return indep_lay


def setup_func_shs():
    # ### Make a snow layer
    shs_lay = make_snow_layer(layer_thickness=0.2, microstructure_model=StickyHardSpheres, density=250, temperature=265, radius=5e-4, stickiness=0.2)
    return shs_lay


def setup_func_pc(pc):
    # ### Make a snow layer
    exp_lay = make_snow_layer(layer_thickness=0.1, microstructure_model=Exponential, density=300, temperature=265, corr_length=pc)
    return exp_lay


def setup_func_em(testpack=None):
    if testpack is None:
        testpack = setup_func_sp()
    sensor = amsre('37V')
    emmodel = IBA(sensor, testpack)
    return emmodel


def setup_func_active(testpack=None):
    if testpack is None:
        testpack = setup_func_sp()
    scatt = active(frequency=10e9, theta_inc=50)
    emmodel = IBA(scatt, testpack)
    return emmodel


def setup_func_mm(testpack=None):
    if testpack is None:
        testpack = setup_func_sp()
    sensor = amsre('37V')
    emmodel = IBA_MM(sensor, testpack)
    return emmodel


def setup_func_rayleigh():
    testpack = setup_func_indep(radius=1e-4)
    sensor = amsre('10V')
    emmodel_iba = IBA(sensor, testpack)
    emmodel_ray = Rayleigh(sensor, testpack)
    return emmodel_iba, emmodel_ray


def setup_mu(stepsize, bypass_exception=None):
    mu_pos = np.arange(1.0, 0., - stepsize)
    if bypass_exception:
        # exclude mu = 1
        mu_pos = mu_pos[1:]
    mu_neg = - mu_pos
    mu = np.concatenate((mu_pos, mu_neg))
    mu = np.array(mu)
    return mu


# Tests to compare with MEMLS IBA, graintype = 2 (small spheres) outputs


def test_pvs_effective_permittivity_real():
    testpack = setup_func_pc(0.3e-3)
    em = setup_func_mm(testpack)
    # Allow 5% error
    ok_(abs(em._effective_permittivity.real - 1.52441173e+00) < tolerance_pc * em._effective_permittivity.real)
    # eq_(em._effective_permittivity.real, 1.52441173e+00)


def test_ks_pc_is_0p3_mm():
    testpack = setup_func_pc(0.3e-3)
    em = setup_func_em(testpack)
    # Allow 5% error
    memls_ks = 4.13718676e+00
    # eq_(em.ks, memls_ks)
    ok_(abs(em.ks - memls_ks) < tolerance_pc * em.ks)


def test_ks_pc_is_0p25_mm():
    testpack = setup_func_pc(0.25e-3)
    em = setup_func_em(testpack)
    # Allow 5% error
    memls_ks = 2.58158887e+00
    # eq_(em.ks, memls_ks)
    ok_(abs(em.ks - memls_ks) < tolerance_pc * em.ks)


def test_ks_pc_is_0p2_mm():
    testpack = setup_func_pc(0.2e-3)
    em = setup_func_em(testpack)
    # Allow 5% error
    memls_ks = 1.41304849e+00
    # eq_(em.ks, memls_ks)
    ok_(abs(em.ks - memls_ks) < tolerance_pc * em.ks)


def test_ks_pc_is_0p15_mm():
    testpack = setup_func_pc(0.15e-3)
    em = setup_func_em(testpack)
    # Allow 5% error
    memls_ks = 6.30218291e-01
    # eq_(em.ks, memls_ks)
    ok_(abs(em.ks - memls_ks) < tolerance_pc * em.ks)


def test_ks_pc_is_0p1_mm():
    testpack = setup_func_pc(0.1e-3)
    em = setup_func_em(testpack)
    # Allow 5% error
    memls_ks = 1.94727497e-01
    # eq_(em.ks, memls_ks)
    ok_(abs(em.ks - memls_ks) < tolerance_pc * em.ks)


def test_ks_pc_is_0p2_mm():
    testpack = setup_func_pc(0.05e-3)
    em = setup_func_em(testpack)
    # Allow 5% error
    memls_ks = 2.49851702e-02
    # eq_(em.ks, memls_ks)
    ok_(abs(em.ks - memls_ks) < tolerance_pc * em.ks)


def test_ks_pc_is_0p1_mm():
    testpack = setup_func_pc(0.1e-3)
    em = setup_func_mm(testpack)
    # Allow 5% error
    memls_ks = 1.94727497e-01
    # eq_(em.ks, memls_ks)
    ok_(abs(em.ks - memls_ks) < tolerance_pc * em.ks)


def test_memlsks_pc_is_0p05_mm():
    testpack = setup_func_pc(0.05e-3)
    em = setup_func_mm(testpack)
    # Allow 5% error
    memls_ks = 2.49851702e-02
    # eq_(em.ks, memls_ks)
    ok_(abs(em.ks - memls_ks) / em.ks < tolerance_pc)


def test_memls_ka():
    testpack = setup_func_pc(0.05e-3)  # Corr fn is irrelevant
    em = setup_func_mm(testpack)
    # Allow 5% error
    memls_ka = 3.00937657e-01
    # eq_(em.ka, memls_ka)
    ok_(abs(em.ka - memls_ka) / em.ka < tolerance_pc)


def test_energy_conservation_exp():
    em = setup_func_em()
    commontest.test_energy_conservation(em, tolerance_pc)


def test_energy_conservation_indep():
    indep_pack = setup_func_indep()
    em = setup_func_em(testpack=indep_pack)
    commontest.test_energy_conservation(em, tolerance_pc)


def test_energy_conservation_shs():
    shs_pack = setup_func_shs()
    em = setup_func_em(testpack=shs_pack)
    commontest.test_energy_conservation(em, tolerance_pc)


def test_npol_passive_is_2():
    em = setup_func_em()
    eq_(em.npol, 2)


def test_npol_active_is_3():
    em = setup_func_active()
    eq_(em.npol, 3)


def test_energy_conservation_exp_active():
    em = setup_func_active()
    commontest.test_energy_conservation(em, tolerance_pc, npol=2)


def test_energy_conservation_indep_active():
    indep_pack = setup_func_indep()
    em = setup_func_active(testpack=indep_pack)
    commontest.test_energy_conservation(em, tolerance_pc, npol=2)


def test_energy_conservation_shs_active():
    shs_pack = setup_func_shs()
    em = setup_func_active(testpack=shs_pack)
    commontest.test_energy_conservation(em, tolerance_pc, npol=2)


# def test_energy_conservation_shs_active_but_npol_is_2():
#     shs_pack = setup_func_shs()
#     em = setup_func_active(testpack=shs_pack)
#     commontest.test_energy_conservation(em, tolerance_pc, npol=2)


def test_iba_vs_rayleigh_passive_m0():
    em_iba, em_ray = setup_func_rayleigh()
    mu = setup_mu(1. / 64)
    ok_((abs(em_iba.ft_even_phase(0, mu, npol=2) / em_iba.ks - em_ray.ft_even_phase(0, mu, npol=2) / em_ray.ks) < tolerance_pc).all())


def test_iba_vs_rayleigh_active_m0():
    # Have to set npol = 2 for m=0 mode in active otherwise rayleigh will produce 3x3 matrix
    em_iba, em_ray = setup_func_rayleigh()
    mu = setup_mu(1. / 64, bypass_exception=True)
    ok_((abs(em_iba.ft_even_phase(0, mu, npol=2) / em_iba.ks - em_ray.ft_even_phase(0, mu, npol=2) / em_ray.ks) < tolerance_pc).all())


def test_iba_vs_rayleigh_active_m1():
    em_iba, em_ray = setup_func_rayleigh()
    mu = setup_mu(1. / 64, bypass_exception=True)
    # Clear cache
    em_iba.cached_mu = None
    ok_((abs(em_iba.ft_even_phase(1, mu, npol=3) / em_iba.ks - em_ray.ft_even_phase(1, mu, npol=3) / em_ray.ks) < tolerance_pc).all())


def test_iba_vs_rayleigh_active_m2():
    em_iba, em_ray = setup_func_rayleigh()
    mu = setup_mu(1. / 64, bypass_exception=True)
    ok_((abs(em_iba.ft_even_phase(2, mu, npol=3) / em_iba.ks - em_ray.ft_even_phase(2, mu, npol=3) / em_ray.ks) < tolerance_pc).all())


def test_permittivity_model():

    new_iba = derived_IBA(effective_permittivity_model=effective_permittivity.maxwell_garnett)
    layer = setup_func_pc(0.3e-3)
    sensor = amsre('37V')
    new_iba(sensor, layer)


@raises(SMRTError)
def test_iba_raise_exception_mu_is_1():
    shs_pack = setup_func_shs()
    em = setup_func_active(testpack=shs_pack)
    bad_mu = np.array([0.2, 1])
    em.ft_even_phase(2, bad_mu, npol=3)

# def test_equivalence_ft_phase_and_phase():
#     em = setup_func_em()
#     em.set_max_mode(4)
#     mu = setup_mu()
#     phi = np.arange(0., 2. * np.pi, 2. * np.pi / mu.size)
#     phi_diff = phi - phi[:, np.newaxis]
#     p = em.phase(mu, phi)
#     pft = em.ft_phase(0, mu)
#     # Construct phi_diff matrix to recombine ft_phase
#     npol = 2
#     n = len(phi_diff)
#     pd = np.empty((npol * n, npol * n))
#     pd[0::npol, 0::npol] = phi_diff
#     pd[0::npol, 1::npol] = phi_diff
#     pd[1::npol, 0::npol] = phi_diff
#     pd[1::npol, 1::npol] = phi_diff
#     # Sum over decomposition modes
#     for m in range(1, 3):
#         pft += em.ft_phase(m, mu).real * np.cos(m * pd) + em.ft_phase(m, mu).imag * np.sin(m * pd)  # Imaginary component should be zero
#     phase_diff = p - pft
#     ok_(phase_diff.all() < TOLERANCE)

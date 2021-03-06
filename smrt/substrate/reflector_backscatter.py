# coding: utf-8

""" Implement a reflective boundary conditions with prescribed reflection coefficient in the specular direction.
The reflection is set to a value or a function of theta. Azimuthal symmetry is assumed (no dependence on phi).

The `specular_reflection` parameter can be a scalar, a function or a dictionary.

    - scalar: same reflection is use for all angles
    - function: the function must take a unique argument theta array (in radians) and return the reflection as an array of the same size as theta
    - dictionary: in this case, the keys must be 'H' and 'V' and the values are a scalar or a function and are interpreted as for the non-polarized case.

To make a reflector, it is recommended to use the helper function :py:func:`~smrt.substrate.reflector.make_reflector`.


Examples::

    # the full path import is required
    from smrt.substrate.reflector import make_reflector

    # return a perfect reflector (the temperature is useless in this specific case)
    ref = make_reflector(temperature=260, specular_reflection=1)

    # return a perfect absorber / black body.
    ref = make_reflector(temperature=260, specular_reflection=0)

.. note::

    the backscatter coefficient argument is not implemented/documented yet.

"""

import numpy as np
import scipy.sparse

# local import
from smrt.core.substrate import Substrate
from smrt import SMRTError


def make_reflector(temperature=None, specular_reflection=None, backscattering_coefficient=None):

    """ Construct a reflector or absorber instance.

    """

    # create the instance
    return Reflector(temperature=temperature, specular_reflection=specular_reflection, backscattering_coefficient=backscattering_coefficient)


class Reflector(Substrate):

    args = []
    optional_args = {'specular_reflection': None, 'backscattering_coefficient': None}

    def specular_reflection_matrix(self, frequency, eps_1, mu1, npol, compute_coherent_only):

        if npol > 2 and not hasattr(self, "stop_pol2_warning"):
            print("active model is not yet fully implemented, need modification for the third component")  # !!!
            self.stop_pol2_warning = True

        if self.specular_reflection is None and self.backscattering_coefficient is None:
            self.specular_reflection = 1

        if isinstance(self.specular_reflection, dict):  # we have a dictionary with polarization
            spec_refl_coeff = np.empty(npol*len(mu1))
            spec_refl_coeff[0::npol] = self._get_refl(self.specular_reflection['V'], mu1)
            spec_refl_coeff[1::npol] = self._get_refl(self.specular_reflection['H'], mu1)
        else:  # we have a scalar, both polarization are the same
            spec_refl_coeff = np.repeat(self._get_refl(self.specular_reflection, mu1), npol)

        return scipy.sparse.diags(spec_refl_coeff, 0)

    def ft_even_diffuse_reflection_matrix(self, m, frequency, eps_1, mu1, npol):

        if m>0:
            return 0  # we've to assume that the backscattering is hemispheric, dealing with a dirac is not possible here
        if isinstance(self.backscattering_coefficient, dict):  # we have a dictionary with polarization
            diffuse_refl_coeff = np.empty(npol*len(mu1))
            if m == 0:
                coef = 0.5
            elif (m % 2) == 1:
                coef = -1.0
            else:
                coef = 1.0

            # correct for the angle between the air and the medium
            #relsin2 = (1 - mu1 ** 2) * eps_1.real
            #coef *= np.where(relsin2 < 1, 1/np.sqrt(1 - relsin2), 0)

            # no, no, it does not work, there is something to be clarified...
            coef /= mu1

            diffuse_refl_coeff[0::npol] += coef * self._get_refl(self.backscattering_coefficient['VV'], mu1)
            diffuse_refl_coeff[1::npol] += coef * self._get_refl(self.backscattering_coefficient['HH'], mu1)
        elif self.backscattering_coefficient is not None:
            raise SMRTError("backscattering_coefficient must be a dictionary")
        else:
            return 0

        return scipy.sparse.diags(diffuse_refl_coeff, 0)

    def absorption_matrix(self, frequency, eps_1, mu1, npol, compute_coherent_only):

        if self.specular_reflection is None and self.backscattering_coefficient is None:
            self.specular_reflection = 1

        if npol > 2 and not hasattr(self, "stop_pol2_warning"):
            print("active model is not yet fully implemented, need modification for the third component") # !!!
            self.stop_pol2_warning = True

        if isinstance(self.specular_reflection, dict):  # we have a dictionary with polarization
            abs_coeff = np.empty(npol*len(mu1))
            abs_coeff[0::npol] = 1 - self._get_refl(self.specular_reflection['V'], mu1)
            abs_coeff[1::npol] = 1 - self._get_refl(self.specular_reflection['H'], mu1)
        else:  # we have a scalar, both polarization are the same
            abs_coeff = 1 - np.repeat(self._get_refl(self.specular_reflection, mu1), npol)

        return scipy.sparse.diags(abs_coeff, 0)

    def _get_refl(self, specular_reflection, mu1):
        if callable(specular_reflection):  # we have a function, call it and see what we get
            user_refl = specular_reflection(np.arccos(mu1))
            if len(user_refl) == len(mu1):  # we have only one polarization
                return user_refl
            else:
                raise SMRTError("The length/shape or the specular_reflection function is incorrect")
        else:  # we have a scalar
            return np.full(len(mu1), specular_reflection, dtype=np.float64)

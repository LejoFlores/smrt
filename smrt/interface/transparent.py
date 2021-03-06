"""A transparent interface (no reflection). Useful for the unit-test mainly.

"""


class Transparent(object):

    @classmethod  # we use a classmethod here because Flat does not have parameter, no need to create instances.
    # Most if not all the other interface classes should be normal object as they contain parameter (e.g. roughness)
    def specular_reflection_matrix(cls, frequency, eps_1, eps_2, mu1, npol, compute_coherent_only):
        """compute the reflection coefficients for the azimuthal mode m
           and for an array of incidence angles (given by their cosine)
           in medium 1. Medium 2 is where the beam is transmitted.

        :param eps_1: permittivity of the medium where the incident beam is propagating.
        :param eps_2: permittivity of the other medium
        :param mhu1: array of cosine of incident angles
        :param npol: number of polarization

"""
        assert len(mu1.shape) == 1  # 1D array

        return 0

    @classmethod  # we use a classmethod here because Flat does not have parameter, no need to create instances.
    # Most if not all the other interface classes should be instance as they contain parameters (e.g. roughness)
    def coherent_transmission_matrix(cls, frequency, eps_1, eps_2, mu1, npol, compute_coherent_only):
        """compute the transmission coefficients for the azimuthal mode m
           and for an array of incidence angles (given by their cosine)
           in medium 1. Medium 2 is where the beam is transmitted.

<<<<<<< local
=======
        :param npol: number of polarizations
>>>>>>> other
        :param eps_1: permittivity of the medium where the incident beam is propagating.
        :param eps_2: permittivity of the other medium
        :param mu1: array of cosine of incident angles
        :param npol: number of polarization

        :return: the transmission matrix
"""
        return 1




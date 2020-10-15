# CLMM Cosmology object abstract superclass

import numpy as np

class CLMMCosmology:
    """
    Cosmology object superclass for supporting multiple back-end cosmology objects

    Attributes
    ----------
    get_par: dict
        Dictionary with functions to get each specific parameter
    set_par: dict
        Dictionary with functions to update each specific parameter
    """
    def __init__(self, **kwargs):
        self.name     = 'not-set'
        self.backend  = None
        self.be_cosmo = None
        self.set_be_cosmo (**kwargs)

    def __getitem__ (self, key):
        if isinstance (key, str):
            return self._get_param (key)
        else:
            raise TypeError(f'input must be str, not {type(key)}')

    def __setitem__ (self, key, val):
        if isinstance (key, str):
            self._set_param (key, val)
        else:
            raise TypeError(f'key input must be str, not {type(key)}')

    def _init_from_cosmo (self, cosmo):
        """
        To be filled in child classes
        """
        raise NotImplementedError

    def _init_from_params (self, **kwargs):
        """
        To be filled in child classes
        """
        raise NotImplementedError

    def _set_param (self, key, val):
        """
        To be filled in child classes
        """
        raise NotImplementedError

    def _get_param (self, key):
        """
        To be filled in child classes
        """
        raise NotImplementedError

    def set_be_cosmo (self, be_cosmo = None, H0 = 70.0, Omega_b0 = 0.05, Omega_dm0 = 0.25, Omega_k0 = 0.0):
        if be_cosmo:
            self._init_from_cosmo (be_cosmo)
        else:
            self._init_from_params (H0 = H0, Omega_b0 = Omega_b0, Omega_dm0 = Omega_dm0, Omega_k0 = Omega_k0)
        
    def get_Omega_m (self, z):
        r"""Gets the value of the dimensionless matter density 

        .. math::
            \Omega_m (z) = \frac{\rho_m(z)}{\rho_\mathrm{crit}(z)}.

        Parameters
        ----------
        z : float
            The redshift.

        Returns
        -------
        Omega_m : float
            dimensionless matter density, :math:`\Omega_m (z)`.

        Notes
        -----
        Need to decide if non-relativist neutrinos will contribute here.
        """        
        raise NotImplementedError

    def eval_da_z1z2 (self, z1, z2):
        r"""Computes the angular diameter distance between z1 and z2.

        .. math::
            d_a (z1, z2) = \dots.

        Parameters
        ----------
        z1 : float
            Redshift.
        z2 : float
            Redshift.

        Returns
        -------
        angular diameter distance : array_like, float
            :math:`d_a (z1, z2)`.

        Notes
        -----
        Describe the vectorization.
        """        
        raise NotImplementedError

    def eval_da (self, z):
        r"""Computes the angular diameter distance between 0.0 and z.

        .. math::
            d_a (z) = \dots.

        Parameters
        ----------
        z : float
            Redshift.

        Returns
        -------
        angular diameter distance : array_like, float
            :math:`d_a (z)`.

        Notes
        -----
        Describe the vectorization.
        """        
        
        return self.eval_da_z1z2 (0.0, z)

    def _get_a_from_z (self, z):
        """ Convert redshift to scale factor

        Parameters
        ----------
        z : array_like
            Redshift

        Returns
        -------
        scale_factor : array_like
            Scale factor
        """
        z = np.array (z)
        if np.any (z < 0.0):
            raise ValueError (f"Cannot convert negative redshift to scale factor")
        return 1.0 / (1.0 + z)


    def _get_z_from_a (self, a):
        """ Convert scale factor to redshift

        Parameters
        ----------
        a : array_like
            Scale factor

        Returns
        -------
        z : array_like
            Redshift
        """
        a = np.array (a)
        if np.any (a > 1.0):
            raise ValueError (f"Cannot convert invalid scale factor a > 1 to redshift")
        return (1.0 / a) - 1.0


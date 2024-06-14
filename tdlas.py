import numpy as np
import matplotlib.pyplot as plt
import scipy
from hapi import *

A = 6.022 * 10**23

"""
https://hitran.org/docs/iso-meta/
https://hitran.org/docs/cross-sections-definitions/
"""

compound = "O2"
id = 7
isotopologue = 1

# Wavelength in nanometers
range_l_min = 500
range_l_max = 2000

db_begin('data')
fetch(compound,id,isotopologue,int(10**7/range_l_max),int(10**7/range_l_min))
"""
nu, coef = absorptionCoefficient_Lorentz(SourceTables='O2', Diluent={'air':1.0})
nu = np.array(nu)
l = 10 ** 7 / nu 
plt.plot(l, coef)
plt.show()
"""

path = 1 # in cm
concentration = 0.6 # mols


def wavelength_DFP(current):
    """Returns the wavelength the laser emits given a current"""
    return 759 + 2 * current / 0.005 # nm


def get_absorption_coefficient(l):
    """Returns the absortion coefficient for wavelenght l"""
    nu, coef = absorptionCoefficient_Lorentz(SourceTables=compound, Diluent={'air':1.0})
    nu = np.array(nu)
    ll = 10 ** 7 / nu
    epsilon = scipy.interpolate.interp1d(ll, coef)
    return epsilon(l)


def gas_absorption(wavelength, L, c):
    """Returns the absortion I / I_0."""
    return exp(get_absorption_coefficient(wavelength) * L * c * A)
    

def get_detection(current):
    k = 1 # Constant voltage is proportional to measured intensity
    return k * gas_absorption(wavelength_DFP(current), path, concentration)

t = np.linspace(0,1,1000)
driving_current = 0.005 * scipy.signal.sawtooth(2 * np.pi * 5 * t)
v = get_detection(driving_current)

plt.plot(t, driving_current)
plt.plot(t, v)
plt.show()



def plot_absortion(l_min, l_max):
    """
        l_min, l_max: wavelenght interval given in nm
        nu_min, nu_max: wavenumber given in cm
    """
    nu_min = int(10**8 / l_max)
    nu_max = int(10**8 / l_min)
    print(nu_min, nu_max)
    db_begin('data')
    fetch('O2',7,1,nu_min,nu_max)
    nu, coef = absorptionCoefficient_Lorentz(SourceTables='O2', Diluent={'air':1.0})

    nu = np.array(nu)
    l = 10 ** 8 / nu
    plt.plot(nu, coef)
    plt.show()



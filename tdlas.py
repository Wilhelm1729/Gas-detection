import numpy as np
import matplotlib.pyplot as plt
import scipy
from hapi import *

"""
https://hitran.org/docs/iso-meta/
https://hitran.org/docs/cross-sections-definitions/
"""

# Avogadros constant
A = 6.022 * 10**23

# Compound
compound = "O2"
id = 7
isotopologue = 1

# Wavelength in nanometers
range_l_min = 500
range_l_max = 2000

# Wavenumber in cm^-1
range_nu_min = int(10**7/range_l_max) 
range_nu_max = int(10**7/range_l_min)

# Load data
db_begin('data')
fetch(compound,id,isotopologue,range_nu_min,range_nu_max)

# Experiment parameters
path_length = 100 # in cm
concentration = 10**(-5) # mols per cm^3


def wavelength_DFP(current):
    """Returns the wavelength distribution the laser emits given a current"""

    center = 759 + 2 * current / 0.005
    variance = 0.01 #"Linewidth of the laser"

    wavelength = np.linspace(center-0.05, center+0.05, 50)
    intensity = 1/sqrt(2*np.pi)/variance * np.exp(-(wavelength-center)**2/variance**2/2)

    return (intensity, wavelength)

# Absorption coefficient, make function from absorption
nu, coef = absorptionCoefficient_Lorentz(SourceTables=compound, Diluent={'air':1.0})
nu = np.array(nu)
ll = 10 ** 7 / nu
get_absorption_coefficient = scipy.interpolate.interp1d(ll, coef)


def gas_absorption(wavelength_distibution, L, c):
    """Returns how much light is transmitted I / I_0."""
    (intensity, wavelength) = wavelength_distibution
    absorbed_intensity = intensity * exp(-get_absorption_coefficient(wavelength) * L * c * A)
    total_intensity = scipy.integrate.simpson(absorbed_intensity, x=wavelength)
    
    return total_intensity
    

def get_detection(current):
    k = 1 # Constant, voltage is proportional to measured intensity
    return k * gas_absorption(wavelength_DFP(current), path_length, concentration)


# Driving current
threshold_current = 0.05

# Sawtooth wave
t = np.linspace(0,1,500)
driving_current = threshold_current / 2 * (1 + scipy.signal.sawtooth(2 * np.pi * 3 * t))

# Measured voltage
v = np.array([get_detection(current) for current in driving_current])


#plt.plot(t, driving_current)
plt.plot(t, v)
plt.show()



"""
l = np.linspace(750,770)
i = gas_absorption(l, path_length, concentration)
plt.plot(l,i)
plt.show()
"""


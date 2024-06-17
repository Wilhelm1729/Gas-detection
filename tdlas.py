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

def wavelength_DFP(current):
    """Returns the wavelength the laser emits given a current"""
    return 763.7 + 0.4 * current / 0.03


# Absorption coefficient
nu, coef = absorptionCoefficient_Lorentz(SourceTables=compound, Diluent={'air':1.0})
nu = np.array(nu)
ll = 10 ** 7 / nu
get_absorption_coefficient = scipy.interpolate.interp1d(ll, coef)


def gas_absorption(wavelength, L, c):
    """Returns how much light is transmitted I / I_0."""
    return exp(-get_absorption_coefficient(wavelength) * L * c * A)
    

def get_detection(current, path_length, concentration):
    k = 1 # Constant, voltage is proportional to measured intensity

    k = 0 if current < 0.01 else current-0.01

    return k * gas_absorption(wavelength_DFP(current), path_length, concentration)


def direct_absorption():
    """DIRECT ABSORPTION SPECTROSCOPY"""
    # Driving current
    threshold_current = 0.03

    # Sawtooth wave
    t = np.linspace(0,1,500)
    driving_current = 0.02 + threshold_current / 2 * (1 + scipy.signal.sawtooth(2 * np.pi * 3 * t))
    
    # Experiment parameters
    path_length = 44 # in cm
    concentration = 0.72*10**(-5) # mols per cm^3

    # Measured voltage
    v = np.array([get_detection(current, path_length, concentration) for current in driving_current])

    #plt.plot(t, driving_current)
    plt.plot(t, v)
    #plt.plot(t, driving_current)

    
    
    plt.show()

def wavelength_modulation():
    """WAVELENGTH MODULATION SPECTROSCOPY"""

    # Driving current
    threshold_current = 0.05

    modulation_frequency = 100
    modulation_amplitude = 0.005

    # Modulated wave
    t = np.linspace(0,1,500)
    driving_current = threshold_current / 2 * (1 + scipy.signal.sawtooth(2 * np.pi * 2 * t))
    modulated_current = modulation_amplitude * np.sin(2 * np.pi * modulation_frequency * t)
    total_current = driving_current+modulated_current

    # Measured voltage
    v = np.array([get_detection(current) for current in driving_current])

    # Lock-in amplifier

    reference_frequency = 100

    #UNFINISHED


def lock_in_amp(signal, frequency):
    pass



def main():
    direct_absorption()

if __name__ == "__main__":
    main()

"""
l = np.linspace(750,770)
i = gas_absorption(l, path_length, concentration)
plt.plot(l,i)
plt.show()
"""


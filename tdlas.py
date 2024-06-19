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
    threshold_current = 0.03

    modulation_frequency = 5000
    modulation_amplitude = 0.002

    # Modulated wave
    t = np.linspace(0,1,50000)

    driving_current = 0.02 + threshold_current / 2 * (1 + scipy.signal.sawtooth(2 * np.pi * t))

    modulated_current = modulation_amplitude * np.sin(2 * np.pi * modulation_frequency * t)
    total_current = driving_current+modulated_current

    # Experiment parameters
    path_length = 300 # in cm
    concentration = 0.72*10**(-5) # mols per cm^3


    # Measured voltage
    v1 = np.array([get_detection(current, path_length, concentration) for current in total_current])
    v2 = np.array([get_detection(current, path_length, 2*concentration) for current in total_current])

    # Lock-in amplifier
    reference_frequency = 10000

    # Multiply by cosine
    signal1 = v1 * np.cos(2 * np.pi * reference_frequency * t)
    signal2 = v2 * np.cos(2 * np.pi * reference_frequency * t)
    #signal1_sin = v1 * np.sin(2 * np.pi * reference_frequency * t)
    
    filtered_signal1 = lowpass_filter(signal1)
    #filtered_signal1 = lowpass_filter(np.sqrt(signal1**2+signal1_sin**2))
    filtered_signal2 = lowpass_filter(signal2)
    
    fig, axs = plt.subplots(2,2, figsize=(10, 10))

    axs[0,0].plot(t, v1)

    axs[0,1].plot(t, signal1)

    axs[1,0].plot(t, filtered_signal1)
    axs[1,1].plot(t, filtered_signal2)

    plt.tight_layout()
    plt.show()



def lowpass_filter(signal):
    """A lowpass filter"""
    freq_cutoff_p = 30
    freq_cutoff_s = 100
    sampling_rate = 50000

    rp = 1
    rs = 40

    wp = freq_cutoff_p / (sampling_rate / 2)
    ws = freq_cutoff_s / (sampling_rate / 2)

    N, Wn = scipy.signal.cheb1ord(wp, ws, rp, rs)
    b, a = scipy.signal.cheby1(N, rp, Wn, btype = 'lowpass', analog = False)
    filtered_signal = scipy.signal.lfilter(b, a, signal)


    return filtered_signal



def main():
    wavelength_modulation()

if __name__ == "__main__":
    main()

"""
l = np.linspace(750,770)
i = gas_absorption(l, path_length, concentration)
plt.plot(l,i)
plt.show()
"""


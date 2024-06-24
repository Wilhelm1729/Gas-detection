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



def output_laser761(current, temp):
    """
    Units: mW, nm, mA
    """
    power = 0 if current < 10 else 0.25 * (current-10) #at temp 25 c, approximate
    wavelength = 760.95 + 0.015 * (current - 15) + (761.15-760.4) / 15 * (temp-35)
    return (power,wavelength)

# Absorption coefficient
nu, coef = absorptionCoefficient_Lorentz(SourceTables=compound, Diluent={'air':1.0})
nu = np.array(nu)
ll = 10 ** 7 / nu
get_absorption_coefficient = scipy.interpolate.interp1d(ll, coef)


def gas_absorption(wavelength, L, c):
    """Returns how much light is transmitted I / I_0."""
    return exp(-get_absorption_coefficient(wavelength) * L * c * A)


def get_detection(current, temperature, path_length, concentration):
    """Calculates what is detected"""
    (power, wavelength) = output_laser761(current, temperature)

    return power * gas_absorption(wavelength, path_length, concentration)


def direct_absorption():
    """DIRECT ABSORPTION SPECTROSCOPY"""
    # Driving current
    sawtooth_amp = 0.05
    sawtooth_freq = 1

    base_current = 40.5 + 1.8 #mA
    temperature = 30.13 #from omega = 8008

    # Sawtooth wave
    t = np.linspace(0,1,500)

    voltage_signal = sawtooth_amp / 2 * (1 + scipy.signal.sawtooth(2 * np.pi * t * sawtooth_freq))
    driving_current = base_current + 50 * voltage_signal

    # Experiment parameters
    path_length = 44 # in cm
    concentration = 0.72*10**(-5) # mols per cm^3

    # Measured voltage
    v = np.array([get_detection(current, temperature, path_length, concentration) for current in driving_current])
    """
    plt.plot(t, v)
    plt.title("Detector")
    plt.show()
    """
    
    fig, axs = plt.subplots(2,2, figsize=(10, 10))

    axs[0,0].plot(t, v)
    axs[0,0].set_title("Detector")
    axs[1,0].plot(t, driving_current)
    axs[1,0].set_title("Driving current")

    power = []
    wavelength = []
    for current in driving_current:
        (p, w) = output_laser761(current, temperature)
        power.append(p)
        wavelength.append(w)
    
    axs[0,1].plot(t, wavelength)
    axs[0,1].set_title("Wavelength variation")

    plt.tight_layout()
    plt.show()
    

def wavelength_modulation():
    """WAVELENGTH MODULATION SPECTROSCOPY"""

    # Driving current
    threshold_current = 30

    modulation_frequency = 5000
    modulation_amplitude = 0.002

    # Modulated wave
    t = np.linspace(0,1,50000)

    driving_current = 20 + threshold_current / 2 * (1 + scipy.signal.sawtooth(2 * np.pi * t))

    modulated_current = modulation_amplitude * np.sin(2 * np.pi * modulation_frequency * t)
    total_current = driving_current + modulated_current

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


def plot_absortion_coefficient(l_min, l_max):
    #l = np.linspace(750,770)
    #i = gas_absorption(l, path_length, concentration)
    l = np.linspace(l_min, l_max, 1000)

    e = get_absorption_coefficient(l)

    plt.plot(l,e)
    plt.show()



def main():
    #plot_absortion_coefficient(760,762)
    direct_absorption()

if __name__ == "__main__":
    main()




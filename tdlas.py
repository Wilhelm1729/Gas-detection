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
#fetch(compound,id,isotopologue,range_nu_min,range_nu_max)



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

    base_current = 40 - 7 #mA
    temperature = 30.13 #from omega = 8008

    # Sawtooth wave
    t = np.linspace(0,1,500)

    voltage_signal = sawtooth_amp / 2 * (1 + scipy.signal.sawtooth(2 * np.pi * t * sawtooth_freq))
    driving_current = base_current + 50 * voltage_signal

    # Experiment parameters
    path_length = 300 # in cm
    concentration = 0.72*10**(-5) # mols per cm^3

    # Measured voltage
    v = np.array([get_detection(current, temperature, path_length, concentration) for current in driving_current])

    #plt.plot(t, v)
    #plt.title("Detector")
    #plt.show()
    
    
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
    sawtooth_amp = 0.05
    sawtooth_freq = 1

    f = 4900

    modulation_frequency = f
    modulation_amplitude = 0.022

    base_current = 32.2 #mA
    temperature = 30.13 #from omega = 8008

    # Sawtooth wave
    t = np.linspace(0,1,50000)

    voltage_signal = sawtooth_amp * (1 + scipy.signal.sawtooth(2 * np.pi * t * sawtooth_freq))
    modulating_voltage = modulation_amplitude * np.sin(2 * np.pi * modulation_frequency * t)

    driving_current = base_current + 50 * (voltage_signal + modulating_voltage)
    dc = base_current + 50 * voltage_signal

    #w = np.array([output_laser761(current, temperature)[1] for current in driving_current])

    # Experiment parameters
    path_length = 44 # in cm
    concentration = 0.94*10**(-5) # mols per cm^3

    # Measured voltage
    v0 = np.array([get_detection(current, temperature, path_length, concentration) for current in dc])
    v1 = np.array([get_detection(current, temperature, path_length, concentration) for current in driving_current])
    

    #(t, v1) = get_xy("O2_DAS/O2-40mA-8008omega-23.1deg-49%RH-5000Hz-0.022A/0.txt",0)
    # t = np.array(t)
    # v1 = np.array(v1)
    # Lock-in amplifier
    reference_frequency = 2 * f

    # Multiply by cosine
    signal_cos = v1 * np.cos(2 * np.pi * reference_frequency * t)
    signal_sin = v1 * np.sin(2 * np.pi * reference_frequency * t)

    #signal1_sin = v1 * np.sin(2 * np.pi * reference_frequency * t)
    
    filtered_signal_cos = lowpass_filter(signal_cos)
    filtered_signal_sin = lowpass_filter(signal_sin)

    filtered_signal = np.sqrt(filtered_signal_cos**2+filtered_signal_sin**2)
    #filtered_signal1 = lowpass_filter(np.sqrt(signal1**2+signal1_sin**2))

    fig, axs = plt.subplots(1,3, figsize=(15, 5))

    #axs[0].plot(t, w)
    axs[0].plot(t, v0)
    axs[0].set_title("Sawtooth")
    axs[0].set_ylabel("Voltage from detector")
    axs[0].set_xlabel("Time")

    axs[1].plot(t, v1)
    axs[1].set_title("With modulation")
    axs[1].set_ylabel("Voltage from detector")
    axs[1].set_xlabel("Time")
    #axs[0,0].set_ylim(6,10)

    axs[2].plot(t, filtered_signal)
    axs[2].set_title("Lock-in amplifier")
    axs[2].set_xlabel("Time")

    plt.tight_layout()
    plt.show()
    

def lowpass_filter(signal):
    """A lowpass filter"""
    freq_cutoff_p = 30
    freq_cutoff_s = 100
    sampling_rate = 50000

    rp = 3
    rs = 64

    wp = freq_cutoff_p / (sampling_rate / 2)
    ws = freq_cutoff_s / (sampling_rate / 2)

    N, Wn = scipy.signal.cheb1ord(wp, ws, rp, rs)
    b, a = scipy.signal.cheby1(N, rp, Wn, btype = 'lowpass', analog = False)
    filtered_signal = scipy.signal.lfilter(b, a, signal)

    return filtered_signal



def plot_absortion_coefficient(l_min, l_max):
    """
    Plots the absorption coefficient and finds the peaks.
    """
    #l = np.linspace(750,770)
    #i = gas_absorption(l, path_length, concentration)
    l = np.linspace(l_min, l_max, 1000)

    e = get_absorption_coefficient(l)
    
    plt.plot(l,e)
    plt.show()

    centers = [760.45, 760.58, 760.65, 760.75, 760.9, 761.0, 761.12, 761.25, 761.4, 761.55]

    abs_coeff = []

    for c in centers:
        r = np.linspace(c - 0.05, c + 0.05 ,100)
        values = get_absorption_coefficient(r)
        m = max(values)
        abs_coeff.append(m)


    print(abs_coeff)

    """
    4.9082 * 10^-23 at 761.12
    4.6301 * 10^-23 at 761.0
    
    """


    """
    Look at:

    nm           absorption coeff (10^-23)
    760.65          5.616
    760.75          4.853

    760.9           5.456
    761.0           4.625

    761.12          4.893
    761.25          3.791

    761.4           3.621
    761.55          2.419
    
    r=0.05
    """


def main():
    #plot_absortion_coefficient(760,762)
    #direct_absorption()
    wavelength_modulation()

if __name__ == "__main__":
    main()



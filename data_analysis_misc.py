import numpy as np 
import matplotlib.pyplot as plt


from matplotlib.ticker import FormatStrFormatter


def open_and_plot(filename, column_index):
    (x_values, y_values) = get_xy(filename, column_index)

    #plot data points
    plt.plot(x_values, y_values, linestyle='solid') 
    plt.xlabel('time samples')  
    plt.ylabel('value') 
    plt.show()


def get_value(filename, column_index):
    (x_values, y_values) = get_xy(filename, column_index)

    #Check these parameters
    r = 5000
    center = 30000                          
    interval = y_values[center-r:center+r]

    y_max = max(interval)

    return y_max

def get_value_with_error(filename, column_index):
    (x_values, y_values) = get_xy(filename, column_index)

    #Check these parameters
    r = 5000
    center = 30000                          
    interval = y_values[center-r:center+r]


    y_max = max(interval)
    y_max_index = np.argmax(interval)

    std_r = 100
    std = np.std(y_values[y_max_index-std_r:y_max_index+std_r])


    return (y_max, std)

def get_standard_error(filename, column_index, start, stop):
    (x_values, y_values) = get_xy(filename, column_index)

    N = stop - start

    values = np.array(y_values[start:stop])

    std = np.std(values)
    mean = np.mean(values)

    return (mean, std)

def get_xy(filename, column_index):
    f = open(filename, "r")
    filedata = f.readlines()
    size = len(filedata)

    x_values = list()
    y_values = list()

    index = 0
    for line in filedata:
        columns = line.split()
        y_values.append(float(columns[column_index]))
        x_values.append(index)
        index += 1

    return (x_values, y_values)




def get_exhaled_and_error(amp, cal_amp, cal_conc, delta_amp, delta_cal_amp, delta_cal_conc):
    """
        Return concetration and error in concentration
    """

    conc = cal_conc * amp / cal_amp

    delta_conc = ((amp/cal_amp)**2*delta_cal_conc**2 + (cal_conc / cal_amp)**2*delta_amp**2 + (cal_conc * amp / cal_amp**2)**2*delta_cal_amp**2 )**(1/2)

    return (conc, delta_conc)


### OXYGEN ################################################################################################
def O2_exhaled():

    (calibration, cal_error) = get_value_with_error("O2_exhaled/O2-40mA-8008omega-23.1deg-49%RH-air-WMS/0.txt", 3)

    (m1, me1) = get_value_with_error("O2_exhaled/O2-40mA-8008omega-23.1deg-49%RH-air-WMS-martin/0.txt", 3)
    (m2, me2) = get_value_with_error("O2_exhaled/O2-40mA-8008omega-23.1deg-49%RH-air-WMS-martin1/0.txt", 3)
    (m3, me3) = get_value_with_error("O2_exhaled/O2-40mA-8008omega-23.1deg-49%RH-air-WMS-martin2/0.txt", 3)

    (w1, we1) = get_value_with_error("O2_exhaled/O2-40mA-8008omega-23.1deg-49%RH-air-WMS-wilhelm/0.txt", 3)
    (w2, we2) = get_value_with_error("O2_exhaled/O2-40mA-8008omega-23.1deg-49%RH-air-WMS-wilhelm1/0.txt", 3)

    air_conc = 19.47 #before 0.193
    air_conc_delta = 0.87

    """
    martin = air_conc * m / calibration
    martin1 = air_conc * m1 / calibration
    martin2 = air_conc * m2 / calibration

    wilhelm = air_conc * w / calibration
    wilhelm1 = air_conc * w1 / calibration
    """

    (cm1, cme1) = get_exhaled_and_error(m1, calibration, air_conc, me1, cal_error, air_conc_delta)
    (cm2, cme2) = get_exhaled_and_error(m2, calibration, air_conc, me2, cal_error, air_conc_delta)
    (cm3, cme3) = get_exhaled_and_error(m3, calibration, air_conc, me3, cal_error, air_conc_delta)

    martin_conc = (cm1 + cm2 + cm3) / 3
    martin_conc_error = (cme1**2 + cme2**2 + cme3**2)**(1/2)/3


    (cw1, cwe1) = get_exhaled_and_error(w1, calibration, air_conc, we1, cal_error, air_conc_delta)
    (cw2, cwe2) = get_exhaled_and_error(w2, calibration, air_conc, we2, cal_error, air_conc_delta)

    wilhelm_conc = (cw1 + cw2) /2
    wilhelm_conc_error = (cwe1**2 + cwe2**2)**(1/2)/2

    print("O2 Martin: (%)", martin_conc, martin_conc_error)

    print("O2 Wilhelm: (%)", wilhelm_conc, wilhelm_conc_error)



### CARBON DIOXIDE ################################################################################################
def CO2_gasmix():
    """
    CO2 tank with 3000ppm
    N2 tank with pure nitrogen gas

    N         CO2         Concentration
    600       0           0
    500       100         500
    400       200         1000
    300       300         1500
    200       400         2000
    100       500         2500
    0         600         3000
    """

    Concentration = [0, 500, 1000, 1500, 2000, 2500, 3000]

    Amplitude = []

    #Amplitude.append(get_value("CO2_gasmix/CO2-120mA-10000omega-23.1deg-49%RH-N600/0.txt", 0))
    #Detection limit. Need to take average

    center = 30000
    r = 1000
    (mean, std) = get_standard_error("CO2_gasmix/CO2-120mA-10000omega-23.1deg-49%RH-N600/0.txt",0,center-r, center+r)

    Amplitude.append(mean)

    Amplitude.append(get_value("CO2_gasmix/CO2-120mA-10000omega-23.1deg-49%RH-N500-O100/0.txt", 0))
    Amplitude.append(get_value("CO2_gasmix/CO2-120mA-10000omega-23.1deg-49%RH-N400-O200/0.txt", 0))
    Amplitude.append(get_value("CO2_gasmix/CO2-120mA-10000omega-23.1deg-49%RH-N300-O300/0.txt", 0))
    Amplitude.append(get_value("CO2_gasmix/CO2-120mA-10000omega-23.1deg-49%RH-N200-O400/0.txt", 0))
    Amplitude.append(get_value("CO2_gasmix/CO2-120mA-10000omega-23.1deg-49%RH-N100-O500/0.txt", 0))
    Amplitude.append(get_value("CO2_gasmix/CO2-120mA-10000omega-23.1deg-49%RH-N000-O600/0.txt", 0))

    plt.plot(Concentration, Amplitude, marker="*")

    plt.xlabel("Concentration [ppm]")
    plt.ylabel("Amplitude [V]")
    plt.title("Amplitude of lock-in ampl. vs vs concentration of CO2")

    plt.show()


def CO2_conc_in_air():
    """Concentration in air in ppm"""
    (calibration, cal_err) = get_value_with_error("CO2_gasmix/CO2-120mA-10000omega-23.1deg-49%RH-N000-O600/0.txt", 0)

    (air, air_err) = get_value_with_error("CO2_exhaled/CO2-120mA-10000omega-23.1deg-49%RH-AIR-LOCKIN/0.txt", 0)

    cal_conc = 3000
    cal_conc_error = 1

    (conc_in_air, delta_conc_in_air) = get_exhaled_and_error(air, calibration, cal_conc, air_err, cal_err, cal_conc_error)


    #conc_in_air = 3000 * air / calibration

    print("CO2 concentration in air: (ppm)", conc_in_air, delta_conc_in_air)


def CO2_exhale():

    #calibration = get_value("CO2_gasmix/CO2-120mA-10000omega-23.1deg-49%RH-N000-O600/0.txt", 0)
    (calibration, cal_err) = get_value_with_error("CO2_gasmix/CO2-120mA-10000omega-23.1deg-49%RH-N000-O600/0.txt", 0)

    (m, me) = get_value_with_error("CO2_exhaled/CO2-120mA-10000omega-23.1deg-49%RH-MARTIN-LOCKIN/0.txt", 0)
    (w, we) = get_value_with_error("CO2_exhaled/CO2-120mA-10000omega-23.1deg-49%RH-WILHELM-LOCKIN/0.txt", 0)
    (a, ae) = get_value_with_error("CO2_exhaled/CO2-120mA-10000omega-23.1deg-49%RH-ARON-LOCKIN/0.txt", 0)

    cal_conc = 3000
    cal_conc_error = 1

    (cm, cme) = get_exhaled_and_error(m, calibration, cal_conc, me, cal_err, cal_conc_error)
    (cw, cwe) = get_exhaled_and_error(w, calibration, cal_conc, we, cal_err, cal_conc_error)
    (ca, cae) = get_exhaled_and_error(a, calibration, cal_conc, ae, cal_err, cal_conc_error)


    #martin = 3000 * m / calibration
    #wilhelm = 3000 * w / calibration
    #aron = 3000 * a / calibration

    print("CO2 Aron (ppm)", ca, cae)
    print("CO2 Martin (ppm)", cm, cme)
    print("CO2 Wilhelm (ppm)", cw, cwe)


def CO2_detection_limit():
    """
    Detection limit for digital and analog lock-in amplifier in ppm
    """

    calibration_digital = get_value("CO2_detection_limit/CO2-120mA-10000omega-23.1deg-49%RH-3000ppm/0.txt", 3)
    calibration_analog = get_value("CO2_detection_limit/CO2-120mA-10000omega-23.1deg-49%RH-3000ppm-LOCKIN/0.txt", 0)
    
    c_d = 30000
    r_d = 1000
    (limit_digital, std) = get_standard_error("CO2_detection_limit/N2-120mA-10000omega-23.1deg-49%RH-3000ppm-noise/0.txt",3,c_d-r_d, c_d+r_d)

    c_a = 29000
    r_a = 1000
    (limit_analog, std) = get_standard_error("CO2_detection_limit/N2-120mA-10000omega-23.1deg-49%RH-3000ppm-LOCKIN-noise/0.txt",0,c_a-r_a, c_a+r_a)

    dl_digital = 3000 * limit_digital / calibration_digital
    dl_analog = 3000 * limit_analog / calibration_analog

    print("Detection limit digital lock in amplifier", dl_digital, "ppm")
    print("Detection limit analog lock in amplifier", dl_analog, "ppm")
    # Weird values, recheck later

### METHANE ################################################################################################

def CH4_gasmix():
    """
    CH4 tank with 100ppm
    N2 tank with pure nitrogen gas

    N         CH4         Concentration
    500       000         0
    400       100         20
    300       200         40
    200       300         60
    100       400         80
    0         500         100
    """

    Concentration = [0, 20, 40, 60, 80, 100]

    Amplitude = []

    #Amplitude.append(get_value("CO2_gasmix/CO2-120mA-10000omega-23.1deg-49%RH-N600/0.txt", 0))
    #Detection limit. Need to take average

    center = 30000
    r = 1000
    (mean, std) = get_standard_error("CH4_gasmix_and_detection_limit/CH4-130mA-11000omega-22.4deg-77%RH-0PPM/0.txt",3,center-r, center+r)

    Amplitude.append(mean)

    Amplitude.append(get_value("CH4_gasmix_and_detection_limit/CH4-130mA-11000omega-22.4deg-77%RH-20PPM/0.txt", 3))
    Amplitude.append(get_value("CH4_gasmix_and_detection_limit/CH4-130mA-11000omega-22.4deg-77%RH-40PPM/0.txt", 3))
    Amplitude.append(get_value("CH4_gasmix_and_detection_limit/CH4-130mA-11000omega-22.4deg-77%RH-60PPM/0.txt", 3))
    Amplitude.append(get_value("CH4_gasmix_and_detection_limit/CH4-130mA-11000omega-22.4deg-77%RH-80PPM/0.txt", 3))
    Amplitude.append(get_value("CH4_gasmix_and_detection_limit/CH4-130mA-11000omega-22.4deg-77%RH-100PPM-A0.1/0.txt", 3))
    #Wrong name in data, last one different

    plt.plot(Concentration, Amplitude, marker="*")

    plt.xlabel("Concentration [ppm]")
    plt.ylabel("Amplitude [V]")
    plt.title("Amplitude of lock-in ampl. vs concentration of CH4")

    plt.show()

def CH4_detection_limit():
    
    calibration = get_value("CH4_gasmix_and_detection_limit/CH4-130mA-11000omega-22.4deg-77%RH-100PPM-A0.1/0.txt", 3)

    center = 30000
    r = 1000
    (mean, std) = get_standard_error("CH4_gasmix_and_detection_limit/CH4-130mA-11000omega-22.4deg-77%RH-0PPM/0.txt",3,center-r, center+r)

    detection_limit = 100 * mean / calibration

    print("Detection limit of CH4 measurements", detection_limit, "ppm")


def CH4_exhaled():
    
    (calibration, cal_err) = get_value_with_error("CH4_exhaled/CH4-130mA-11000omega-22.4deg-77%RH-100PPM-A0.1/0.txt", 3)

    (air, aire) = get_value_with_error("CH4_exhaled/CH4-130mA-11000omega-22.4deg-77%RH-AIR/0.txt", 3)
    (m, me) = get_value_with_error("CH4_exhaled/CH4-130mA-11000omega-22.4deg-77%RH-MARTIN/0.txt", 3)
    
    cal_conc = 100
    cal_conc_error = 1

    (cm, cme) = get_exhaled_and_error(m, calibration, cal_conc, me, cal_err, cal_conc_error)
    (cair, caire) = get_exhaled_and_error(air, calibration, cal_conc, aire, cal_err, cal_conc_error)

    """
    calibration = get_value("CH4_exhaled/CH4-130mA-11000omega-22.4deg-77%RH-100PPM-A0.1/0.txt", 3)

    air = get_value("CH4_exhaled/CH4-130mA-11000omega-22.4deg-77%RH-AIR/0.txt", 3)
    martin = get_value("CH4_exhaled/CH4-130mA-11000omega-22.4deg-77%RH-MARTIN/0.txt", 3)

    cal_conc = 100

    air_conc = 100 * air / calibration
    martin_conc = 100 * martin / calibration
    """

    print("CH4 concentration in air (ppm)", cair, caire)
    print("CH4 Exhaled by martin (ppm)", cm, cme)



### VAPOR ################################################################################################

def VAPOR_exhaled():
    
    (calibration, cal_err) = get_value_with_error("VAPOR_exhaled/VAPOR-70mA-8008omega-22.4deg-77%RH/0.txt", 0)

    (m, me) = get_value_with_error("VAPOR_exhaled/VAPOR-70mA-8008omega-22.4deg-77%RH-MARTIN/0.txt", 0)
    (w, we) = get_value_with_error("VAPOR_exhaled/VAPOR-70mA-8008omega-22.4deg-77%RH-WILHELM/0.txt", 0)
    (a, ae) = get_value_with_error("VAPOR_exhaled/VAPOR-70mA-8008omega-22.4deg-77%RH-ARON/0.txt", 0)


    RH = 0.77
    dRH = 0.05
    temp = 22.4
    dtemp = 0.1

    swp = 2.6447 + (2.8104-2.6447) * 0.4 # 0.4 = 22.4 -22
    swp_e = (2.8104-2.6447) * dtemp
    
    cal_conc = swp * RH
    cal_conc_error = ((swp * dRH)**2 + (swp_e * RH)**2)**(1/2)

    print("TEST",cal_conc, cal_conc_error)

    """
    RH 77%
    Temp 22.4 deg

    22 -> 2.6447
    23 -> 2.8104

    2.6447 + (2.8104-2.6447) * 0.4 = 2.711
    2.711 * 0.77 = 2.08747
    """

    (cm, cme) = get_exhaled_and_error(m, calibration, cal_conc, me, cal_err, cal_conc_error)
    (cw, cwe) = get_exhaled_and_error(w, calibration, cal_conc, we, cal_err, cal_conc_error)
    (ca, cae) = get_exhaled_and_error(a, calibration, cal_conc, ae, cal_err, cal_conc_error)

    """
    calibration = get_value("VAPOR_exhaled/VAPOR-70mA-8008omega-22.4deg-77%RH/0.txt", 0)

    aron = get_value("VAPOR_exhaled/VAPOR-70mA-8008omega-22.4deg-77%RH-ARON/0.txt", 0)
    martin = get_value("VAPOR_exhaled/VAPOR-70mA-8008omega-22.4deg-77%RH-MARTIN/0.txt", 0)
    wilhelm = get_value("VAPOR_exhaled/VAPOR-70mA-8008omega-22.4deg-77%RH-WILHELM/0.txt", 0)

    calibration_conc = 2.08747

    aron_conc = calibration_conc * aron / calibration
    martin_conc = calibration_conc * martin / calibration
    wilhelm_conc = calibration_conc * wilhelm / calibration
    """

    print("Vapor exhaled by aron (%)", ca, cae)
    print("Vapor exhaled by martin (%)", cm, cme)
    print("Vapor exhaled by wilhelm (%)", cw, cwe)



def exp_plot():

    #f1 = "Plot/CO2-120mA-10000omega-23.1deg-49%RH-air/0.txt"
    #f2 = "Plot/CO2-120mA-10000omega-23.1deg-49%RH-air-A0.05/0.txt"

    f1 = "O2_DAS/O2-40mA-8008omega-23.1deg-49%RH/4.txt"
    f2 = "O2_DAS/O2-40mA-8008omega-23.1deg-49%RH-5000Hz-0.022A/0.txt"
    
    
    (x1, y1) = get_xy(f1, 0)
    (x2, y2) = get_xy(f2, 0)
    (x3, y3) = get_xy(f2, 3)

    fig, axs = plt.subplots(1,3, figsize=(15, 5))

    

    fs_label = 16
    fs_title = 18

    fs_ticks = 10

    axs[0].plot(x1,y1)
    axs[0].set_title("Sawtooth",fontsize=fs_title)
    axs[0].set_ylabel("Voltage from detector [V]",fontsize=fs_label)
    axs[0].set_xlabel("Sample points",fontsize=fs_label)
    axs[0].set_xticklabels(axs[0].get_xticks(), fontsize=fs_ticks)
    axs[0].set_yticklabels(axs[0].get_yticks(), fontsize=fs_ticks)

    axs[1].plot(x2,y2)
    axs[1].set_title("With modulation",fontsize=fs_title)
    axs[1].set_ylabel("Voltage from detector [V]",fontsize=fs_label)
    axs[1].set_xlabel("Sample points",fontsize=fs_label)
    axs[1].set_xticklabels(axs[1].get_xticks(), fontsize=fs_ticks)
    axs[1].set_yticklabels(axs[1].get_yticks(), fontsize=fs_ticks)

    axs[2].plot(x3,y3)
    axs[2].set_title("Lock-in amplifier",fontsize=fs_title)
    axs[2].set_ylabel("Output amplitude",fontsize=fs_label)
    axs[2].set_xlabel("Sample points",fontsize=fs_label)
    axs[2].set_xticklabels(axs[2].get_xticks(), fontsize=fs_ticks)
    axs[2].set_yticklabels(axs[2].get_yticks(), fontsize=fs_ticks)
    
    plt.tight_layout()
    plt.savefig("sample_experiment.png")
    plt.show()

    """
    (x1, y1) = get_xy(f2, 1)
    (x2, y2) = get_xy(f2, 2)
    (x3, y3) = get_xy(f2, 3)

    fig, axs = plt.subplots(1,3, figsize=(15, 5))
    axs[0].plot(x1,y1)
    axs[1].plot(x2,y2)
    axs[2].plot(x3,y3)

    plt.tight_layout()
    plt.show()
    """

    #plot data points
    #Plt.plot(x_values, y_values, linestyle='solid') 
    #plt.xlabel('time samples')  
    #plt.ylabel('value') 
    #plt.show()



def linear():
    
    Concentration = [0, 500, 1000, 1500, 2000, 2500, 3000]

    Amplitude = []

    #Amplitude.append(get_value("CO2_gasmix/CO2-120mA-10000omega-23.1deg-49%RH-N600/0.txt", 0))
    #Detection limit. Need to take average

    center = 30000
    r = 1000
    (mean, std) = get_standard_error("CO2_gasmix/CO2-120mA-10000omega-23.1deg-49%RH-N600/0.txt",0,center-r, center+r)

    Amplitude.append(mean)

    Amplitude.append(get_value("CO2_gasmix/CO2-120mA-10000omega-23.1deg-49%RH-N500-O100/0.txt", 0))
    Amplitude.append(get_value("CO2_gasmix/CO2-120mA-10000omega-23.1deg-49%RH-N400-O200/0.txt", 0))
    Amplitude.append(get_value("CO2_gasmix/CO2-120mA-10000omega-23.1deg-49%RH-N300-O300/0.txt", 0))
    Amplitude.append(get_value("CO2_gasmix/CO2-120mA-10000omega-23.1deg-49%RH-N200-O400/0.txt", 0))
    Amplitude.append(get_value("CO2_gasmix/CO2-120mA-10000omega-23.1deg-49%RH-N100-O500/0.txt", 0))
    Amplitude.append(get_value("CO2_gasmix/CO2-120mA-10000omega-23.1deg-49%RH-N000-O600/0.txt", 0))

    fig, axs = plt.subplots(1,2, figsize=(10, 4))

    axs[0].plot(Concentration, Amplitude, marker="*")

    axs[0].set_xlabel("Concentration [ppm]")
    axs[0].set_ylabel("Amplitude [V]")
    axs[0].set_title("Amplitude of lock-in ampl. vs vs concentration of CO2")


    
    Concentration = [0, 20, 40, 60, 80, 100]

    Amplitude = []

    #Amplitude.append(get_value("CO2_gasmix/CO2-120mA-10000omega-23.1deg-49%RH-N600/0.txt", 0))
    #Detection limit. Need to take average

    center = 30000
    r = 1000
    (mean, std) = get_standard_error("CH4_gasmix_and_detection_limit/CH4-130mA-11000omega-22.4deg-77%RH-0PPM/0.txt",3,center-r, center+r)

    Amplitude.append(mean)

    Amplitude.append(get_value("CH4_gasmix_and_detection_limit/CH4-130mA-11000omega-22.4deg-77%RH-20PPM/0.txt", 3))
    Amplitude.append(get_value("CH4_gasmix_and_detection_limit/CH4-130mA-11000omega-22.4deg-77%RH-40PPM/0.txt", 3))
    Amplitude.append(get_value("CH4_gasmix_and_detection_limit/CH4-130mA-11000omega-22.4deg-77%RH-60PPM/0.txt", 3))
    Amplitude.append(get_value("CH4_gasmix_and_detection_limit/CH4-130mA-11000omega-22.4deg-77%RH-80PPM/0.txt", 3))
    Amplitude.append(get_value("CH4_gasmix_and_detection_limit/CH4-130mA-11000omega-22.4deg-77%RH-100PPM-A0.1/0.txt", 3))
    #Wrong name in data, last one different

    axs[1].plot(Concentration, Amplitude, marker="*")

    axs[1].set_xlabel("Concentration [ppm]")
    axs[1].set_ylabel("Amplitude [V]")
    axs[1].set_title("Amplitude of lock-in ampl. vs concentration of CH4")

    plt.tight_layout()
    plt.show()
    

if __name__ == "__main__":
    #open_and_plot("O2-40mA-8008omega-23.1deg-49%RH-air-DAS/0.txt", 0)
    #VAPOR_exhaled()
    #CO2_conc_in_air()
    #CO2_exhale()
    #CH4_exhaled()
    #O2_exhaled()
    #open_and_plot("O2_DAS/O2-31.6mA-8008omega-23.1deg-49%RH/0.txt",0)
    #open_and_plot("O2_DAS/O2-31.6mA-8008omega-23.1deg-49%RH/0.txt",0)
    #open_and_plot("O2_DAS/O2-31.6mA-8008omega-23.1deg-49%RH-air/0.txt",0)
    #open_and_plot("O2_DAS/O2-31.6mA-8008omega-23.1deg-49%RH-air/0.txt",3)
    #open_and_plot("O2_DAS/O2-31.6mA-8008omega-23.1deg-49%RH-air-DAS/0.txt",0)
    exp_plot()
    #linear()



#open_and_plot("CO2_gasmix/CO2-120mA-10000omega-23.1deg-49%RH-N000-O600/0.txt", 0)
#open_and_plot("CO2_exhaled/CO2-120mA-10000omega-23.1deg-49%RH-AIR-LOCKIN/0.txt", 0)
#print(CO2_conc_in_air())    
#open_and_plot("O2_exhaled/O2-40mA-8008omega-23.1deg-49%RH-air-WMS-martin/0.txt", 3)


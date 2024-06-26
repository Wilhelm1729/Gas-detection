import numpy as np 
import matplotlib.pyplot as plt





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


### OXYGEN ################################################################################################
def O2_exhaled():

    calibration = get_value("O2_exhaled/O2-40mA-8008omega-23.1deg-49%RH-air-WMS/0.txt", 3)

    m = get_value("O2_exhaled/O2-40mA-8008omega-23.1deg-49%RH-air-WMS-martin/0.txt", 3)
    m1 = get_value("O2_exhaled/O2-40mA-8008omega-23.1deg-49%RH-air-WMS-martin1/0.txt", 3)
    m2 = get_value("O2_exhaled/O2-40mA-8008omega-23.1deg-49%RH-air-WMS-martin2/0.txt", 3)

    w = get_value("O2_exhaled/O2-40mA-8008omega-23.1deg-49%RH-air-WMS-wilhelm/0.txt", 3)
    w1 = get_value("O2_exhaled/O2-40mA-8008omega-23.1deg-49%RH-air-WMS-wilhelm1/0.txt", 3)

    air_conc = 0.193 #change

    martin = air_conc * m / calibration
    martin1 = air_conc * m1 / calibration
    martin2 = air_conc * m2 / calibration

    wilhelm = air_conc * w / calibration
    wilhelm1 = air_conc * w1 / calibration

    print("martin", martin)
    print("martin1", martin1)
    print("martin2", martin2)

    print("martin mean", (martin+martin1+martin2)/3)

    print("wilhelm1", wilhelm)
    print("wilhelm2", wilhelm1)

    print("wilhelm mean", (wilhelm+wilhelm1)/2)



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
    plt.title("Amplitude of detection vs concentration of CO2")

    plt.show()


def CO2_conc_in_air():
    """Concentration in air in ppm"""
    calibration = get_value("CO2_gasmix/CO2-120mA-10000omega-23.1deg-49%RH-N000-O600/0.txt", 0)

    air = get_value("CO2_exhaled/CO2-120mA-10000omega-23.1deg-49%RH-AIR-LOCKIN/0.txt", 0)

    conc_in_air = 3000 * air / calibration

    print(conc_in_air)


def CO2_exhale():

    calibration = get_value("CO2_gasmix/CO2-120mA-10000omega-23.1deg-49%RH-N000-O600/0.txt", 0)

    m = get_value("CO2_exhaled/CO2-120mA-10000omega-23.1deg-49%RH-MARTIN-LOCKIN/0.txt", 0)
    w = get_value("CO2_exhaled/CO2-120mA-10000omega-23.1deg-49%RH-WILHELM-LOCKIN/0.txt", 0)
    a = get_value("CO2_exhaled/CO2-120mA-10000omega-23.1deg-49%RH-ARON-LOCKIN/0.txt", 0)
    
    martin = 3000 * m / calibration
    wilhelm = 3000 * w / calibration
    aron = 3000 * a / calibration

    print("Aron", aron)
    print("Martin", martin)
    print("Wilhelm", wilhelm)


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
    plt.title("Amplitude of detection vs concentration of CH4")

    plt.show()

def CH4_detection_limit():
    
    calibration = get_value("CH4_gasmix_and_detection_limit/CH4-130mA-11000omega-22.4deg-77%RH-100PPM-A0.1/0.txt", 3)

    center = 30000
    r = 1000
    (mean, std) = get_standard_error("CH4_gasmix_and_detection_limit/CH4-130mA-11000omega-22.4deg-77%RH-0PPM/0.txt",3,center-r, center+r)

    detection_limit = 100 * mean / calibration

    print("Detection limit of CH4 measurements", detection_limit, "ppm")


def CH4_exhaled():
    
    calibration = get_value("CH4_exhaled/CH4-130mA-11000omega-22.4deg-77%RH-100PPM-A0.1/0.txt", 3)

    air = get_value("CH4_exhaled/CH4-130mA-11000omega-22.4deg-77%RH-AIR/0.txt", 3)
    martin = get_value("CH4_exhaled/CH4-130mA-11000omega-22.4deg-77%RH-MARTIN/0.txt", 3)

    air_conc = 100 * air / calibration
    martin_conc = 100 * martin / calibration

    print("Concentration in air", air_conc, "ppm")
    print("Exhaled by martin", martin_conc, "ppm")



### VAPOR ################################################################################################

def VAPOR_exhaled():
    
    calibration = get_value("VAPOR_exhaled/VAPOR-70mA-8008omega-22.4deg-77%RH/0.txt", 0)

    aron = get_value("VAPOR_exhaled/VAPOR-70mA-8008omega-22.4deg-77%RH-ARON/0.txt", 0)
    martin = get_value("VAPOR_exhaled/VAPOR-70mA-8008omega-22.4deg-77%RH-MARTIN/0.txt", 0)
    wilhelm = get_value("VAPOR_exhaled/VAPOR-70mA-8008omega-22.4deg-77%RH-WILHELM/0.txt", 0)

    calibration_conc = 2.08747
    
    """
    RH 77%
    Temp 22.4 deg

    22 -> 2.6447
    23 -> 2.8104

    2.6447 + (2.8104-2.6447) * 0.4 = 2.711
    2.711 * 0.77 = 2.08747
    """



    aron_conc = calibration_conc * aron / calibration
    martin_conc = calibration_conc * martin / calibration
    wilhelm_conc = calibration_conc * wilhelm / calibration

    print("Exhaled by aron", aron_conc, "proc")
    print("Exhaled by martin", martin_conc, "proc")
    print("Exhaled by wilhelm", wilhelm_conc, "proc")



def exp_plot():

    #f1 = "Plot/CO2-120mA-10000omega-23.1deg-49%RH-air/0.txt"
    #f2 = "Plot/CO2-120mA-10000omega-23.1deg-49%RH-air-A0.05/0.txt"
    
    f1 = "O2_DAS/O2-40mA-8008omega-23.1deg-49%RH-air-DAS/4.txt"
    f2 = "O2_DAS/O2-40mA-8008omega-23.1deg-49%RH-5000Hz-0.022A/0.txt"
    
    """
    (x1, y1) = get_xy(f1, 0)
    (x2, y2) = get_xy(f2, 0)
    (x3, y3) = get_xy(f2, 3)

    fig, axs = plt.subplots(1,3, figsize=(15, 5))

    axs[0].plot(x1,y1)
    axs[0].set_title("Sawtooth")
    axs[0].set_ylabel("Voltage from detector [V]")
    axs[0].set_xlabel("Sample points")

    axs[1].plot(x2,y2)
    axs[1].set_title("With modulation")
    axs[1].set_ylabel("Voltage from detector [V]")
    axs[1].set_xlabel("Sample points")

    axs[2].plot(x3,y3)
    axs[2].set_title("Lock-in amplifier")
    axs[2].set_xlabel("Sample points")
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

    #plot data points
    #plt.plot(x_values, y_values, linestyle='solid') 
    #plt.xlabel('time samples')  
    #plt.ylabel('value') 
    #plt.show()


if __name__ == "__main__":
    #open_and_plot("O2-40mA-8008omega-23.1deg-49%RH-air-DAS/0.txt", 0)
    #VAPOR_exhaled()
    #O2_exhaled()
    #open_and_plot("O2_DAS/O2-31.6mA-8008omega-23.1deg-49%RH/0.txt",0)
    #open_and_plot("O2_DAS/O2-31.6mA-8008omega-23.1deg-49%RH/0.txt",0)
    #open_and_plot("O2_DAS/O2-31.6mA-8008omega-23.1deg-49%RH-air/0.txt",0)
    #open_and_plot("O2_DAS/O2-31.6mA-8008omega-23.1deg-49%RH-air/0.txt",3)
    #open_and_plot("O2_DAS/O2-31.6mA-8008omega-23.1deg-49%RH-air-DAS/0.txt",0)
    exp_plot()
    



#open_and_plot("CO2_gasmix/CO2-120mA-10000omega-23.1deg-49%RH-N000-O600/0.txt", 0)
#open_and_plot("CO2_exhaled/CO2-120mA-10000omega-23.1deg-49%RH-AIR-LOCKIN/0.txt", 0)
#print(CO2_conc_in_air())    
#open_and_plot("O2_exhaled/O2-40mA-8008omega-23.1deg-49%RH-air-WMS-martin/0.txt", 3)


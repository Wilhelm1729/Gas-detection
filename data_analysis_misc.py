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

    r = 5000
    center = 30000
    interval = y_values[center-r:center+r]

    y_max = max(interval)

    return y_max


def get_standard_error(filename, column_index, start, stop):
    (x_values, y_values) = get_xy(filename, column_index)

    N = stop - start

    values = np.array(y_values[start.stop])

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


def O2_exhaled():

    calibration = get_value("O2_exhaled/O2-40mA-8008omega-23.1deg-49%RH-air-WMS/0.txt", 3)



print(get_value("O2_exhaled/O2-40mA-8008omega-23.1deg-49%RH-air-WMS-martin/0.txt", 3))

open_and_plot("O2_exhaled/O2-40mA-8008omega-23.1deg-49%RH-air-WMS-martin/0.txt", 3)
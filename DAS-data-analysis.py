import numpy as np 
import matplotlib.pyplot as plt

def plot_absorbtion(filename, ymaxrange, yminrange): #Hard coded for 50 000 data points
    f = open(filename, "r")
    y_values = f.readlines()
    ymin = 1000
    ymin_xvalue = 0
    for i in range(len(y_values)):
        y_values[i] = float(y_values[i][:8])
        if y_values[i] < ymin and i < ymaxrange and i > yminrange: 
            ymin = y_values[i]
            ymin_xvalue = i
    print("min y value:", ymin, "x value:", ymin_xvalue)
    
    regression_data_y = []
    regression_data_x = []
    for i in range(1000, 11000, 1000):
        regression_data_y.append(y_values[i])
        regression_data_x.append(i)
    
    regression_data_x_array = np.array(regression_data_x)
    regression_data_x_array = np.append(regression_data_x_array, ymaxrange)
    regression_data_y_array = np.array(regression_data_y)
    regression_data_y_array = np.append(regression_data_y_array, y_values[ymaxrange])

    # Calculate the regression line (slope and intercept)
    slope, intercept = np.polyfit(regression_data_x_array, regression_data_y_array, 1)
    
    #y above value
    y_above_absorption = slope * ymin_xvalue + intercept # To do

    print(y_above_absorption)
    # Generate the y values of the regression line
    regression_line = slope * regression_data_x_array + intercept
    plt.plot(regression_data_x_array, regression_line, 'r-', label=f'Regression Line: y = {slope:.2f}x + {intercept:.2f}')
 
 
    x_values = list(range(1, 50001))

    #plot data points
    plt.plot(x_values, y_values, linestyle='solid') 
    plt.xlabel('x - axis, time')  
    plt.ylabel('y - axis, absorption') 

    plt.plot(ymin_xvalue, y_above_absorption, "g*")

    plt.show()
    #return x_values, y_values, 
    return y_above_absorption, ymin

def calculate_oxygen_concentration(V0, V, L, epsilon):
    # Calculate absorbance
    A = np.log(V0 / V)
    
    # Calculate concentration
    C = A / (epsilon * L)

    #Returns concentration (molecules per cubic centimeter)
    return C

intensity_sent, intensity_recieved = plot_absorbtion("0.txt", 45000, 15000)

oxygen_concentration = calculate_oxygen_concentration(intensity_sent, intensity_recieved, 44.2, 1.3e3)


"""
#Examples:
plot_absorbtion("0")
...
plot_absorbtion("4")
"""

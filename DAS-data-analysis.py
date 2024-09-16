import numpy as np 
import matplotlib.pyplot as plt
import math


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

def plot_absorbtion(filename, ymaxrange, cutoff): #Hard coded for 50 000 data points
    
    (x_values, y_values) = get_xy(filename, 0)
    
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
    # Generate the y values of the regression line
    regression_line = slope * regression_data_x_array + intercept


    quotient = []
    min = 2
    min_index = 0

    for i in range(50000):
        initial = slope * i + intercept
        absorbed = y_values[i]
        q = absorbed / initial
        quotient.append(q)
        if q < min and i < cutoff:
            min = q
            min_index = i
    
    r = 100 # Radien för värdena där standardavvikelsen räknas ut, 100 från inspektion av grafen

    std = np.std(quotient[min_index-r:min_index+r])
    mean = np.mean(quotient[min_index-r:min_index+r]) 

    #Förut returnerades min instället för mean


    #print(min)

    #plot data points
    """
    fig, axs = plt.subplots(2,1, figsize=(10, 10))

    axs[0].plot(x_values, y_values, linestyle='solid') 
    axs[0].plot(regression_data_x_array, regression_line, 'r-', label=f'Regression Line: y = {slope:.2f}x + {intercept:.2f}')

    axs[1].plot(x_values, quotient)

    plt.tight_layout()
    plt.show()
    """
    return (mean, std)


def calculate_oxygen_concentration(V0, V, L, epsilon):
    # Calculate absorbance
    A = np.log(V0 / V)
    
    # Calculate concentration
    C = A / (epsilon * L)

    #Returns concentration (molecules per cubic centimeter)
    return C


def calculate_oxygen_concentration_with_error(V, delta_V, L, delta_L, epsilon):
    #delta_epsilon is assumed to be small

    # Calculate concentration
    C = -np.log(V) / (epsilon * L)

    # Error
    delta_C = ((1/(epsilon * L * V))**2*delta_V**2 + (np.log(V) / (epsilon * L**2))**2 * delta_L**2)**(1/2)

    #Returns concentration (molecules per cubic centimeter)
    return (C, delta_C)

#V0_1, V_1 = plot_absorbtion("O2_DAS/O2-40mA-8008omega-23.1deg-49%RH-air-DAS/1.txt", 45000, 15000)
#V0_2, V_2 = plot_absorbtion("O2_DAS/O2-31.6mA-8008omega-23.1deg-49%RH-air-DAS/1.txt", 45000, 15000)


#A_1 = plot_absorbtion("O2_DAS/O2-40mA-8008omega-23.1deg-49%RH/2.txt", 45000, 45000)
#A_2 = plot_absorbtion("O2_DAS/O2-31.6mA-8008omega-23.1deg-49%RH/4.txt", 45000, 45000)


"""
sum_1 = 0
sum_2 = 0
for i in range(5):
    #sum_1  += plot_absorbtion("O2_DAS/O2-40mA-8008omega-23.1deg-49%RH-air-DAS/"+str(i)+".txt", 45000, 45000)
    #sum_2  += plot_absorbtion("O2_DAS/O2-31.6mA-8008omega-23.1deg-49%RH-air-DAS/"+str(i)+".txt", 45000, 45000)
    sum_1  += plot_absorbtion("O2_DAS/O2-40mA-8008omega-23.1deg-49%RH/"+str(i)+".txt", 45000, 45000)
    sum_2  += plot_absorbtion("O2_DAS/O2-31.6mA-8008omega-23.1deg-49%RH/"+str(i)+".txt", 45000, 45000)
"""
    

#A_1 = sum_1 / 5
#A_2 = sum_2 / 5

#print(A_1, A_2)

#L = 44 #L = 400 #44.2 # cm
#A = 6.022 * 10**23
#e = 4.9082 * 10**-23 #absorption coefficient for w=761.12
#e = 4.6301 * 10**-23 #absorption coefficient for w = 761.0

#oxygen_concentration = calculate_oxygen_concentration(intensity_sent, intensity_recieved, L, e*A)

#print("Oxygen concentration", oxygen_concentration)

# Search for the right absorption peak

abs_coeff = [5.1248646136058054e-23, 4.4441924337452004e-23, 5.616444626627102e-23, 4.8526588398367214e-23, 5.455597787505272e-23, 4.6254426833187146e-23, 4.893293460994988e-23, 3.7909009909837687e-23, 3.621014010915559e-23, 2.4196619420450937e-23]

#index 4 5 are the right abs coeff

#print(abs_coeff[4],abs_coeff[5])

"""
for i in range(len(abs_coeff)-1):
    if i % 2 == 1:
        continue

    e_1 = abs_coeff[i]
    e_2 = abs_coeff[i+1]

    c_1 = calculate_oxygen_concentration(1, A_2, L, e_1*A)
    c_2 = calculate_oxygen_concentration(1, A_1, L, e_2*A)

    print(i, i+1)
    print(c_1, c_2, c_1/c_2)


"""

def calculate_oxygen_level():
    """
        Calculates the oxygen concentration and error using the "error" (noise) on
        the graph and the error in the path length
    """
    mean_sum_1 = 0
    mean_sum_2 = 0
    std_sum_1 = 0
    std_sum_2 = 0
    for i in range(5):
        #sum_1  += plot_absorbtion("O2_DAS/O2-40mA-8008omega-23.1deg-49%RH-air-DAS/"+str(i)+".txt", 45000, 45000)
        #sum_2  += plot_absorbtion("O2_DAS/O2-31.6mA-8008omega-23.1deg-49%RH-air-DAS/"+str(i)+".txt", 45000, 45000)

        # ta bort -air-DAS, och ändra L till 44 cm för att få de första mätningarna
        (val_1, std_1) = plot_absorbtion("O2_DAS/O2-40mA-8008omega-23.1deg-49%RH-air-DAS/"+str(i)+".txt", 45000, 45000)
        (val_2, std_2) = plot_absorbtion("O2_DAS/O2-31.6mA-8008omega-23.1deg-49%RH-air-DAS/"+str(i)+".txt", 45000, 45000)

        mean_sum_1  += val_1
        mean_sum_2  += val_2
        std_sum_1  += std_1**2
        std_sum_2  += std_2**2

    A_1 = mean_sum_1 / 5
    A_2 = mean_sum_2 / 5
    S_1 = std_sum_1**(1/2) / 5
    S_2 = std_sum_1**(1/2) / 5

    print(A_1, A_2, S_1, S_2)

    L = 450 #L = 400 #44.2 # cm
    delta_L = 20
    A = 6.022 * 10**23

    (c_1, e_1) = calculate_oxygen_concentration_with_error(A_2, S_2, L, delta_L, abs_coeff[4]*A)
    (c_2, e_2) = calculate_oxygen_concentration_with_error(A_1, S_1, L, delta_L, abs_coeff[5]*A)


    c_pure = 101000 * 0.01**3 / 8.314 / 300

    #print(c_1, c_2, c_1/c_2)

    c = (c_1 + c_2) / 2
    e = (e_1**2 + e_2**2)**(1/2)/2

    print(c, e)

    print(c_2/c_pure*100,e_2/c_pure*100)




calculate_oxygen_level()

"""

Using the data for the path length 44 cm:

At 760.9:
Conc = 7.96*10^-6 mol / cm^3

At 761.0:
Conc = 7.75*10^-6 mol / cm^3

Using the data for the path length 300



760.9 and 761.0 yields precisely 1.052 * 10^-5 mol / cm^3 (344 cm)










Outdated:

New hypothesis:

At 760.9:
Conc = 8.29*10^-5 mol / cm^3

At 761.0:
Conc = 8.23*10^-5 mol / cm^3



PV = NRT
V = 1 cm^3 = 0.01^3 m^3
N = PV / RT = 101000 * 0.01^3 / 8.314 / 300 = 4 * 10^-5 (pure 100% oxygen)





At 761:
Conc = 9.6499 * 10^-5

At 761.12
Conc = 7.5636 * 10^-5

mol/cm^3

SO this is wrong.


Table of absorption coefficients.

The peak at 31.6 mA is slightly (0.8877) stronger than the one at 40 mA (0.905)

    nm           absorption coeff (10^-23)
    760
    760
    
    760.65          5.616
    760.75          4.853

    760.9           5.456
    761.0           4.625

    761.12          4.893
    761.25          3.791

    761.4           3.621
    761.55          2.419



"""

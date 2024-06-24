#Plotta sinus amplituderna
#plotta sinus amplituden mot lock in amplifier

#y axel sinus max amplitud, x axel amplituden som står i slutet av filen
import numpy as np 
import matplotlib.pyplot as plt
import re
from pathlib import Path

def plot_absorbtion(filename, ymaxrange, yminrange): #Hard coded for 50 000 data points
    """
    Plots absoprtion graph and returns I_0 and I, input with a range for the absoprtion spectrum
    """
    f = open(filename, "r")
    y_values = f.readlines()
    ymax_amplitud = 0
    ymin_xvalue = 0
    for i in range(len(y_values)):
        y_values[i] = float(y_values[i][28:36])
        if y_values[i] > ymax_amplitud: 
            ymax_amplitud = y_values[i]
            ymin_xvalue = i


    #C:\\Users\\marti\\Documents\\lockin_amplituderna
    #return x_values, y_values, 
    #print("max y amplitud:", ymax_amplitud, "measurements frequency in Hz:", frequency)
    return ymax_amplitud

#plot_absorbtion("C:\\Users\\marti\\Documents\\0.txt", 0, 50000)

def get_folder_names(directory):
    path = Path(directory)
    folder_names = [f.name for f in path.iterdir() if f.is_dir()]
    return folder_names


def extract_amp(filename):
    # Define a regular expression pattern to match the frequency string
    pattern = r'\d+\.\d+A'
    
    # Search for the pattern in the filename
    match = re.search(pattern, filename)
    
    # If a match is found, return the matched string, otherwise return None
    if match:
        return match.group(0)
    else:
        return None

def loop_folders(fld, unit_name):
    # Remove "A" and convert each element to a float, for each folder name
    folder_amps = []
    for i in fld:
        foldername = i
        amp = extract_amp(foldername)
        folder_amps.append(amp)
    return [float(amp.replace(unit_name, '')) for amp in folder_amps]


def max_amplitude_list(folder_name, folders, txt_file_type):
    max_amplitudes_list = []
    for i in range(len(folders)):
        temp = folders[i].replace('\\', '\\\\')
        print(folder_name +  str(temp) + "\\" + txt_file_type)
        max_amplitudes_list.append(plot_absorbtion(folder_name + "\\" + str(temp) + "\\" + txt_file_type, 0, 50000))
    return max_amplitudes_list

def plot_sinus_lockinamplifier(x_lst, y_lst):
    plt.autoscale()
    plt.plot(x_lst, y_lst, 'o') 
    plt.xlabel('x - Sinus Amp')   # Sinus Amplituden
    plt.ylabel('y - Max Amp')     # Mätningen av lock in amplifier
    plt.title("Sinus Amplitude vs Measurement of Lock in amplifier")
    plt.show()

#EXAMPLE:

def main():

    #Oxygen
    """
    data_folder, data_txt_file = "C:\\Users\\marti\\Documents\\amplituderna_graf_2", "0.txt"
    plot_sinus_lockinamplifier(loop_folders(get_folder_names(data_folder), "A"), max_amplitude_list(data_folder, get_folder_names(data_folder), data_txt_file))
    """

    #Carbon Dioxide
    """
    data_folder, data_txt_file = "C:\\Users\\marti\\Documents\\koldioxid_sinus_amp", "0.txt"
    plot_sinus_lockinamplifier(loop_folders(get_folder_names(data_folder), "A"), max_amplitude_list(data_folder, get_folder_names(data_folder), data_txt_file))
    """
    
    #Methane
    """
    data_folder, data_txt_file = "C:\\Users\\marti\\Documents\\metan_sinus_amp", "0.txt"
    plot_sinus_lockinamplifier(loop_folders(get_folder_names(data_folder), "A"), max_amplitude_list(data_folder, get_folder_names(data_folder), data_txt_file))
    """

    #Water Vapour
    """
    data_folder, data_txt_file = "C:\\Users\\marti\\Documents\\water_vapour_sinus_amp", "0.txt"
    plot_sinus_lockinamplifier(loop_folders(get_folder_names(data_folder), "A"), max_amplitude_list(data_folder, get_folder_names(data_folder), data_txt_file))
    """

main()


#IGNORE:

"""
def extract_frequency(filename):
    # Define a regular expression pattern to match the frequency string
    pattern = r'\d+Hz'
    
    # Search for the pattern in the filename
    match = re.search(pattern, filename)
    
    # If a match is found, return the matched string, otherwise return None
    if match:
        return match.group(0)
    else:
        return None

# Example usage


folder_frequencies = []
for i in folders:
    foldername = i
    frequency = extract_frequency(foldername)
    folder_frequencies.append(frequency)

#print(folder_frequencies)


max_amplitudes_list = []

for i in range(len(folders)):
    temp = folders[i].replace('\\', '\\\\')
    print("C:\\Users\\marti\\Documents\\lockin_amplituderna\\" + str(temp) + "\\0.txt")
    max_amplitudes_list.append(plot_absorbtion("C:\\Users\\marti\\Documents\\lockin_amplituderna\\" + str(temp) + "\\0.txt", 0, 50000))
print(max_amplitudes_list)

def remove_hz_and_convert_to_int(frequency_list):
    # Remove "Hz" and convert each element to an integer
    return [int(freq.replace('Hz', '')) for freq in frequency_list]

Lock in amplituderna
x_val = remove_hz_and_convert_to_int(folder_frequencies)
plt.autoscale()
plt.plot(x_val, max_amplitudes_list) 
plt.xlabel('x - Frequencies')  
plt.ylabel('y - Amplitudes')
plt.title("0.022A")
plt.show()
"""
import numpy as np 
import matplotlib.pyplot as plt

#Oxygen
"""
data = [19.2, 18.8, 18.9, 19.1, 19.0]
names = [ "Wilhelm1", "Wilhelm2", "Martin1", "Martin2", "Martin3"]
plt.figure(figsize=(10, 6))
bars = plt.bar(names, data, color='skyblue', edgecolor='black')
plt.axhline(y=19.3, color='red', linestyle='--', label='Oxygen Concentration in Air')
plt.ylim(18.50, 19.5)
plt.ylabel('Concentration (%)')
plt.xlabel('Attempts')
plt.title('Oxygen concentration vs humans breathing out')
plt.legend()
for bar, concentration in zip(bars, data):
    plt.text(bar.get_x() + bar.get_width()/2, bar.get_height(), f'{concentration:.2f}%', 
             ha='center', va='bottom', color='black', fontsize=20)
plt.show()

"""
#Carbon dioxide
"""
# Given data
x = [34438, 28025, 37999]
y = ["Aron", "Wilhelm", "Martin"]

# Create a bar plot
plt.figure(figsize=(8, 6))
bars = plt.bar(y, x, color='skyblue', edgecolor='black')

# Draw a horizontal line at y = 495
plt.axhline(y=495, color='red', linestyle='--', label='CO2 concentration in air 495 ppm')

# Set y-axis to logarithmic scale
plt.yscale('log')

# Add values on top of the bars
for bar, value in zip(bars, x):
    plt.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 100, str(value) + " ppm", 
             ha='center', va='bottom', color='black', fontsize=12)

# Add titles and labels
plt.title('Logarithmic histogram CO2 concentration vs human breathing')
plt.xlabel('Attempts')
plt.ylabel('Concentration (ppm)')
plt.legend(loc='center right')

# Show the plot
plt.tight_layout()
plt.show()
"""

#Methane
"""
data = [1.7]
names = ["Martin"]
plt.figure(figsize=(10, 6))
bars = plt.bar(names, data, color='skyblue', edgecolor='black')
plt.axhline(y=2.0, color='red', linestyle='--', label='Methane Concentration in air 2.0 ppm')
plt.ylim(1.5, 2.1)
plt.ylabel('Concentration (ppm)')
plt.xlabel('Attempts')
plt.title('Methane concentration vs humans breathing out')
plt.legend()
for bar, concentration in zip(bars, data):
    plt.text(bar.get_x() + bar.get_width()/2, bar.get_height(), f'{concentration:.2f}%', 
             ha='center', va='bottom', color='black', fontsize=20)
plt.show()
"""

#Water vapour
"""
data = [2.219, 2.224, 2.233]
names = ["Aron", "Wilhelm", "Martin"]
plt.figure(figsize=(5, 5))
bars = plt.bar(names, data, color='skyblue', edgecolor='black')
plt.axhline(y=2.09, color='red', linestyle='--', label='Water Vapour Concentration in air 2.09%')
plt.ylim(2.0, 2.4)
plt.ylabel('Concentration (%)')
plt.xlabel('Attempts')
plt.title('Methane concentration vs humans breathing out')
plt.legend()
for bar, concentration in zip(bars, data):
    plt.text(bar.get_x() + bar.get_width()/2, bar.get_height(), f'{concentration:.3f}%', 
             ha='center', va='bottom', color='black', fontsize=20)
plt.show()
"""

import numpy as np 
import matplotlib.pyplot as plt

# Create a figure with 2x2 subplots
fig, axs = plt.subplots(1, 4, figsize=(16, 4))

# Oxygen concentration plot
data_oxygen = [18.98, 19.01]
names_oxygen = ["Wilhelm", "Martin"]
axs[0].bar(names_oxygen, data_oxygen, color='skyblue', edgecolor='black')
axs[0].axhline(y=19.3, color='red', linestyle='--', label='Oxygen conc. in air 19.3%')
axs[0].set_ylim(18.50, 19.5)
axs[0].set_ylabel('Concentration (%)')
axs[0].set_title('Oxygen exhaled vs oxygen in air', fontsize=10)
axs[0].legend()
for bar, concentration in zip(axs[0].patches, data_oxygen):
    axs[0].text(bar.get_x() + bar.get_width()/2, bar.get_height(), f'{concentration:.2f}%', 
                   ha='center', va='bottom', color='black', fontsize=12)

# Carbon dioxide concentration plot
data_co2 = [34438, 28025, 37999]
names_co2 = ["Aron", "Wilhelm", "Martin"]
bars = axs[1].bar(names_co2, data_co2, color='skyblue', edgecolor='black')
axs[1].axhline(y=495, color='red', linestyle='--', label='CO2 conc. in air 495 ppm')
axs[1].set_yscale('log')
axs[1].set_ylim(0, 10**5)
for bar, value in zip(bars, data_co2):
    axs[1].text(bar.get_x() + bar.get_width()/2, bar.get_height() + 100, str(value) + " ppm", 
                   ha='center', va='bottom', color='black', fontsize=12)
axs[1].set_title('Logarithmic scale, CO2 exhaled vs CO2 in air', fontsize=10)
axs[1].set_ylabel('Concentration (ppm)')
axs[1].legend(loc='upper right')

# Methane concentration plot
data_methane = [1.7]
names_methane = ["Martin"]
axs[2].bar(names_methane, data_methane, color='skyblue', edgecolor='black', width = 0.5)
axs[2].axhline(y=2.0, color='red', linestyle='--', label='Methane conc. in air 2.0 ppm')
axs[2].set_ylim(1.5, 2.1)
axs[2].set_ylabel('Concentration (ppm)')
axs[2].set_title('Methane exhaled vs methane in air', fontsize=10)
axs[2].legend()
for bar, concentration in zip(axs[2].patches, data_methane):
    axs[2].text(bar.get_x() + bar.get_width()/2, bar.get_height(), f'{concentration:.2f}%', 
                   ha='center', va='bottom', color='black', fontsize=12)

# Water vapour concentration plot
data_water = [2.219, 2.224, 2.233]
names_water = ["Aron", "Wilhelm", "Martin"]
bars = axs[3].bar(names_water, data_water, color='skyblue', edgecolor='black')
axs[3].axhline(y=2.09, color='red', linestyle='--', label='Water vapour conc. in air 2.09%')
axs[3].set_ylim(2.0, 2.4)
axs[3].set_ylabel('Concentration (%)')
axs[3].set_title('Water vapour exhaled vs water vapour in air', fontsize=10)
axs[3].legend()
for bar, concentration in zip(bars, data_water):
    axs[3].text(bar.get_x() + bar.get_width()/2, bar.get_height(), f'{concentration:.3f}%', 
                   ha='center', va='bottom', color='black', fontsize=12)

# Adjust layout
plt.tight_layout()
plt.savefig("pp_fig")
plt.show()

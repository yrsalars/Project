#%%
import pandas as pd
import numpy as np
from itertools import combinations

# Load data
measured_mass = pd.read_excel(r'C:\Users\au708090\OneDrive\Dokument\PhD\Courses\Python\BAC_compounds.xlsx', sheet_name='Sheet1',)
chemical_elements = pd.read_excel(r'C:\Users\au708090\OneDrive\Dokument\PhD\Courses\Python\Monoisotopic_masses.xlsx', sheet_name='Most occuring')
mm = measured_mass['m/z'].astype(float).tolist()
print(measured_mass)
#%%
def calculate_mass(formula):
    elements = {}
    for i, row in chemical_elements.iterrows():
        elements[row['Symbol']] = row['Mass']
    
    mass = 0
    current_element = ''
    current_count = ''
    for char in formula:
        if char.isupper():
            if current_element != '':
                if current_count == '':
                    current_count = '1'
                mass += elements[current_element] * int(current_count)
            current_element = char
            current_count = ''
        elif char.islower():
            current_element += char
        elif char.isdigit():
            current_count += char
    
    if current_element != '':
        if current_count == '':
            current_count = '1'
        mass += elements[current_element] * int(current_count)
    
    return mass
measured_mass='C17H28NO3'
print(calculate_mass(measured_mass))

def ppm_error(measured_mass, calculated_mass):
    if measured_mass == 0:
        return None
    return abs((measured_mass - calculated_mass) / measured_mass) * 1e6
print(ppm_error)
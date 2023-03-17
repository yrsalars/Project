#%%
# Import the necessary modules
import pandas as pd
import numpy as np
import itertools
from itertools import combinations
from itertools import combinations_with_replacement
from collections import Counter

# Load data
measured_mass = pd.read_excel(r'C:\Users\au708090\OneDrive\Dokument\PhD\Courses\Python\BAC_compounds.xlsx', sheet_name='Sheet1',)
#chemical_elements = pd.read_excel(r'C:\Users\au708090\OneDrive\Dokument\PhD\Courses\Python\Monoisotopic_masses.xlsx', sheet_name='Most occuring')
# Define the dictionary of elements and their atomic masses
measured_mass = pd.read_excel(r'C:\Users\au708090\OneDrive\Dokument\PhD\Courses\Python\BAC_compounds.xlsx', sheet_name='Sheet1',)
print(measures_mass)
#%%
chemical_elements = {
    "H": {"Symbol": "H", "Mass": 1.007825},
    "C": {"Symbol": "C", "Mass": 12.0},
    "N": {"Symbol": "N", "Mass": 14.003074},
    "O": {"Symbol": "O", "Mass": 15.994915}
}

#mm = measured_mass['m/z'].astype(float).tolist()
mm=[304.29]

# Define the function to calculate the ppm error
def ppm_error(mm, calculated_mass):
    if mm == 0:
        return None
    return abs((mm - calculated_mass) / mm) * 1e6

# Define the function to calculate the possible chemical formulas
def calc_formulas(mz):
    # Define the list of elements and their atomic masses
    elements = []
    for symbol, data in chemical_elements.items():
        elements.append((data['Symbol'], data['Mass']))
    
    # Define the minimum and maximum counts for each element
    min_counts = {'H': 0, 'C': 10, 'N': 0, 'O': 0}
    max_counts = {'H': 40, 'C': 25, 'N': 2, 'O': 5}

    # Calculate the possible formulas
    
    # Calculate the possible formulas
    possible_formulas = []
    for i in range(1, len(elements) + 1):
        for combination in itertools.chain.from_iterable(
            [combinations(elements, r) for r in range(1, i + 1)]):
            counts = Counter(combination)
            # Check if the counts of each element are within the limits
            if all(
                counts.get(elem, 0) >= min_counts.get(elem, 0)
                and counts.get(elem, 0) <= max_counts.get(elem, float("inf"))
                for elem in counts.keys()):
                formula = "".join([elem[0] for elem in combination])
                mass = sum([elem[1] for elem in combination])
                if abs(mass - mz) < 0.1:
                    possible_formulas.append((formula, mass))



    
    # Return the list of possible formulas, sorted by mass
    if possible_formulas:
        return sorted(possible_formulas, key=lambda x: x[1])
   
    # Filter the possible formulas based on the ppm error
    ppm_tolerance = 50 # set the ppm tolerance here
    filtered_formulas = []
    for formula, mass in possible_formulas:
        error = ppm_error(mz, mass)
        if error is not None and error <= ppm_tolerance:
            filtered_formulas.append((formula, mass, error))
            print(f"Formula {formula} has ppm error {error}")
            
   # Convert the list of tuples to a DataFrame
    columns = ['Formula', 'Mass', 'PPM Error']
    df = pd.DataFrame(filtered_formulas, columns=columns)
    
    # Sort the filtered formulas by increasing ppm error
    df = df.sort_values(by='PPM Error')
    
    return df
 
for mass in mm:
    formulas = calc_formulas(mass)
    if formulas is not None:
        print('Measured Mass:', mass)
        print(formulas.to_string(index=False, columns=['Formula', 'Mass', 'PPM Error']))
        print()
    else:
        print('Error: could not calculate formulas for measured mass', mass)



       


# %%

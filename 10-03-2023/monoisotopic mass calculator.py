#%%
import pandas as pd
Mono_masses=pd.read_excel(r'C:\Users\au708090\OneDrive\Dokument\PhD\Courses\Python\Monoisotopic_masses.xlsx', sheet_name='Most occuring')
print(Mono_masses)

# %%
# Import the necessary modules
import pandas as pd
import numpy as np
from itertools import combinations
from scipy.optimize import minimize_scalar

measured_mass=pd.read_excel(r'C:\Users\au708090\OneDrive\Dokument\PhD\Courses\Python\BAC_compounds.xlsx', sheet_name='Sheet1',)
chemical_elements=pd.read_excel(r'C:\Users\au708090\OneDrive\Dokument\PhD\Courses\Python\Monoisotopic_masses.xlsx', sheet_name='Most occuring')
mm=measured_mass['m/z'].tolist()

    # Define the function to calculate the ppm error
def ppm_error(mm, calculated_mass):
    return abs((mm- calculated_mass) / mm) * 1e6

# # Define the function to calculate the possible chemical formulas
def calc_formulas(mm):
    # Define the list of elements and their atomic masses
    elements = {'H': 1.007825, 'C': 12.0, 'N': 14.003074, 'O': 15.994915}
  
    # Define the mass tolerance (in Da) for each element
    tol = {element: 50 / 1e6 * mass for element, mass in elements.items()}

    # Define the function to calculate the mass of a formula
    def calc_mass(formula):
        mass = 0
        for element, count in formula.items():
            mass += count * elements[element]
        return mass

    # Create a list of all possible combinations of elements and their counts
    elements_list = []
    for i in range(1, len(elements) + 1):
        for combination in combinations(elements.keys(), i):
            elements_list.append(dict.fromkeys(combination, 0))

    # Create a DataFrame to store the possible formulas and their masses
    formulas_df = pd.DataFrame(columns=['Formula', 'Mass'])

    # Iterate through each possible formula and calculate its mass
    for formula in elements_list:
        for element, mass in tol.items():
            formula[element] = int(np.ceil(mm / elements[element] - mass))
        if all(count >= 0 for count in formula.values()):
            mass = calc_mass(formula)
            formulas_df = formulas_df.append({'Formula': formula, 'Mass': mass}, ignore_index=True)

    # Sort the formulas by their mass and keep only the top three
    formulas_df = formulas_df.sort_values('Mass').head(3)

    # Calculate the ppm error for each formula and add it to the DataFrame
    for i in range(len(formulas_df)):
        ppm = ppm_error(mm, formulas_df.iloc[i]['Mass'])
        formulas_df.at[i, 'PPM Error'] = ppm

    return formulas_df
 

for masses in measured_mass:
    formulas = calc_formulas([mm])
    print(masses, 'Measured Mass', formulas.to_string(index=False))


#%% Example usage
measured_masses = [119.0351, 101.0438, 145.0602]
for measured_mass in measured_masses:
    formulas = calc_formulas([measured_mass])
    print('Measured Mass:', measured_mass)
    print(formulas)
    print()

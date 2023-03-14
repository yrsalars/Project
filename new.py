#%%
import pandas as pd
import numpy as np
from itertools import combinations

# Load data
measured_mass = pd.read_excel(r'C:\Users\au708090\OneDrive\Dokument\PhD\Courses\Python\BAC_compounds.xlsx', sheet_name='Sheet1',)
chemical_elements = pd.read_excel(r'C:\Users\au708090\OneDrive\Dokument\PhD\Courses\Python\Monoisotopic_masses.xlsx', sheet_name='Most occuring')
mm = measured_mass['m/z'].astype(float).tolist()

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
#%%
# Import the necessary modules
import pandas as pd
import numpy as np
from itertools import combinations

# Load data
measured_mass = pd.read_excel(r'C:\Users\au708090\OneDrive\Dokument\PhD\Courses\Python\BAC_compounds.xlsx', sheet_name='Sheet1',)
chemical_elements = pd.read_excel(r'C:\Users\au708090\OneDrive\Dokument\PhD\Courses\Python\Monoisotopic_masses.xlsx', sheet_name='Most occuring')
mm = measured_mass['m/z'].astype(float).tolist()

# Define the function to calculate the ppm error
def ppm_error(mm, calculated_mass):
    if mm == 0:
        return None
    return abs((mm - calculated_mass) / mm) * 1e6

# Define the function to calculate the possible chemical formulas
def calc_formulas(mz):
    # Define the list of elements and their atomic masses
    elements = {}
    for i, row in chemical_elements.iterrows():
        elements [row['Symbol']] = row['Mass']
  
    mass = 0
    current_element = ''
    current_count = ''
    for char in mz:
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
  
    # Define the function to calculate the mass of a formula
    def calc_mass(formula):
        mass_dict = {}
        for element, count in formula.items():
            mass_dict[element]= count * elements[element]
        return sum(mass_dict.values())

    # Create a list of all possible combinations of elements and their counts
    elements_list = [dict.fromkeys(elements.keys(), 0) for i in range(2, len(elements) + 1)]
    for i in range(1, len(elements) + 1):
        for combination in combinations(elements.keys(), i):
            elements_list.append(dict.fromkeys(combination, 0))
        for i in range(1, 10):
            for combination in combinations(elements.keys(), i):
                elements_list.append(dict.fromkeys(combination, 0))

    # Create a DataFrame to store the possible formulas and their masses
    formulas_df = pd.DataFrame(columns=['Formula', 'Mass', 'PPM Error'])

    # Define the mass tolerance (in Da) for each element
    tol = {element: 100 / 1e6 * mass for element, mass in elements.items()}

    #Range for monoisotopic mass calculation and difference in Dalton
    min_mass = mz - 5 
    max_mass = mz + 5

    # Iterate through each possible formula and calculate its mass
    for formula in elements_list:
        mass = calc_mass(formula)
        if mass >= min_mass and mass <= max_mass:
            for element, mass in elements.items():
                formula[element] = int(np.ceil(mz / mass - tol[element]))
            if all(count >= 0 for count in formula.values()):
                mass = calc_mass(formula)
                formulas_df = formulas_df.append({'Formula': formula, 'Mass': mass}, ignore_index=True)

    # Sort the formulas by their mass and keep only the top three
    formulas_df = formulas_df.sort_values('Mass').head(3)

    # Convert the formula dictionary to a string representation
    formulas_df['Formula Str'] = formulas_df['Formula'].apply(lambda x: ''.join([f'{k}{v}' for k,v in x.items() if v > 0]))
    formulas_df = formulas_df.drop(columns='Formula')

    # Calculate the ppm error for each formula and add it to the DataFrame
    for i in range(len(formulas_df)):
        ppm = ppm_error(mz, formulas_df.iloc[i]['Mass'])
        if ppm is not None:
            formulas_df.at[i, 'PPM Error'] = ppm
        else:
            print('Error: could not calculate ppm error')

    # Return the formulas_df DataFrame
    return formulas_df


for mass in mm:
    formulas = calc_formulas(mass)
    if formulas is not None:
        print('Measured Mass:', mass)
        print(formulas[['Formula Str', 'Mass', 'PPM Error']].to_string(index=False))
        print()
    else:
        print('Error: could not calculate formulas for measured mass', mass)


       


# %%

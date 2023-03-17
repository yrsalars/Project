#%%
import pandas as pd
from itertools import product
from prettytable import PrettyTable

# Atomic masses of each element
atom_mass = {'H': 1.007825, 'C': 12.0, 'N': 14.003074, 'O': 15.994915}

# Calculate the possible molecular formulas that give the monoisotopic mass within 50 ppm
def calc_formulas(mz, min_counts):
    formulas = []
    # Loop over all possible combinations of elements up to a maximum count
    max_counts = {'C': 40, 'H': 50, 'N': 2, 'O': 3}
    for counts in product(*(range(min_count, max_count+1) for min_count, max_count in zip(min_counts.values(), max_counts.values()))):
        # Calculate the mass of this combination of elements
        mass = sum(count * atom_mass[elem] for elem, count in zip(max_counts.keys(), counts))
        # Check if the mass is within 50 ppm of the measured mass
        ppm_error = abs(mass - mz) / mz * 1e6
        if ppm_error <= 50:
            formula = ''.join(elem if count == 1 else f"{elem}{count}" for elem, count in zip(max_counts.keys(), counts) if count > 0)
            formulas.append((formula, mass, ppm_error))
    return formulas
print('loading...')
# Read the data from the Excel file
df = pd.read_excel(r'C:\Users\au708090\OneDrive\Dokument\PhD\Courses\Python\BAC_compounds.xlsx', sheet_name='Sheet1',)

# Loop over the m/z values and calculate the possible formulas
for mz in df['m/z']:
    formulas = calc_formulas(mz, {'C': 10, 'H': 10, 'N': 0, 'O': 0}) #lower limit of chemicals
    if formulas is not None:
        print('Measured Mass:', mz)
        sorted_formulas = sorted(formulas, key=lambda x: x[2])#sorted by ppm error values
        table = PrettyTable()
        table.field_names = ["m/z", "Ret.Time", "Theoretical Formula", "Mass", "ppm error"]
        for formula, mass, ppm_error in sorted_formulas:
            table.add_row([mz, df.loc[df['m/z'] == mz, 'Ret.Time'].iloc[0], formula, f"{mass:.4f}", f"{ppm_error:.3f}"])
        print(table)




       
# %%

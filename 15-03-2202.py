#%%
# # Define a dictionary of atomic masses 
atomic_masses = {
    "H": 1.007825,
    "C": 12.0,
    "N": 14.003074,
    "O": 15.994915,
    "F": 18.998403,
    "P": 30.973763,
    "S": 31.972072,
    "Cl": 34.968853,
}

def find_molecular_formula(monoisotopic_mass, tolerance=0.1):
def find_molecular_formula(monoisotopic_mass):
def find_molecular_formula(monoisotopic_mass, tolerance=0.1):
    """
    Given a monoisotopic mass, returns the molecular formula
    that has the closest possible mass to the given value.
    """
    # Initialize variables
    formula = {}
    mass_error = float("inf")
    mass_error = monoisotopic_mass
    mass_error = float("inf")
    max_atoms = 70
    max_H_atoms = 50
    max_C_atoms = 21
    max_N_atoms = 1
    max_O_atoms = 4
    max_F_atoms = 0
    max_P_atoms = 0
    max_S_atoms = 0
    max_Cl_atoms = 0
    mass_out = None
    # Loop through all possible combinations of atoms up to max_atoms
    for num_c in range(max_atoms + 1):
        for num_h in range(max_H_atoms - num_c + 1):
            for num_n in range(max_N_atoms - num_c - num_h + 1):
                for num_o in range(max_O_atoms - num_c - num_h - num_n + 1):
                    for num_f in range(max_F_atoms - num_c - num_h - num_n - num_o + 1):
                        for num_p in range(max_P_atoms - num_c - num_h - num_n - num_o - num_f + 1):
                            for num_s in range(max_S_atoms - num_c - num_h - num_n - num_o - num_f - num_p + 1):
                                for num_cl in range(max_Cl_atoms - num_c - num_h - num_n - num_o - num_f - num_p - num_s + 1):
                                    # Calculate the mass of this formula
                                    mass = num_c*atomic_masses["C"] + num_h*atomic_masses["H"] + num_n*atomic_masses["N"] + num_o*atomic_masses["O"] + num_f*atomic_masses["F"] + num_p*atomic_masses["P"] + num_s*atomic_masses["S"] + num_cl*atomic_masses["Cl"] 
                                    # Check if the mass is closer to the target than the current closest formula
                                    if abs(mass - monoisotopic_mass) < abs(mass_error):
                                        # Update the closest formula and mass error
                                        formula = {"C": num_c, "H": num_h, "N": num_n, "O": num_o, "F": num_f, "P": num_p, "S": num_s, "Cl": num_cl}
                                        mass_error = abs(mass - monoisotopic_mass)
                                        mass_out = mass
                                    

    # Return the closest molecular formula
    return formula, mass_out

# Test the function
mono_mass = 304.29
tolerance = 0.1
formula, mass = find_molecular_formula(mono_mass, tolerance)
formula, mass = find_molecular_formula(mono_mass)
tolerance = 0.1
formula, mass = find_molecular_formula(mono_mass, tolerance)

print(f"The molecular formula with a monoisotopic mass closest to {mono_mass}(+/- {tolerance}) is {formula}.")
print(f"The molecular formula with a monoisotopic mass closest to {mono_mass} is {formula}.")
print(f"The molecular formula with a monoisotopic mass closest to {mono_mass}(+/- {tolerance}) is {formula}.")
print(f"with a mass of {mass}")

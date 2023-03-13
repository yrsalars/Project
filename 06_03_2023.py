#%%
import pandas as pd
BAC_metabolites=pd.read_excel(r'C:\Users\au708090\OneDrive\Dokument\PhD\Courses\Python\BAC_compounds.xlsx', sheet_name='Sheet1')
print(BAC_metabolites)

# %%
import pandas as pd
BAC_formulas=pd.read_excel(r'C:\Users\au708090\OneDrive\Dokument\PhD\Courses\Python\BAC_compounds.xlsx', sheet_name='Formulas')
print(BAC_formulas)
# %%
#Find monoisotopic mass that matches the measures monoisotopic mass, one column where the different of parent and product is written out
if BAC_metabolites[:,0]==filewithcompounds[:,0]

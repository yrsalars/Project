#%%
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from scipy.optimize import curve_fit

# Load data from CSV file
data = pd.read_csv('data.csv', header=None, names=['x', 'y', 'error'])

# Define the function to fit
def degradation_curve(x, a, b):
    return a * np.exp(-b * x)

# Fit the degradation curve to the data
popt, pcov = curve_fit(degradation_curve, data['x'], data['y'], sigma=data['error'], absolute_sigma=True)

# Plot the data with error bars and the fitted curve
plt.errorbar(data['x'], data['y'], yerr=data['error'], fmt='o', capsize=3)
plt.plot(data['x'], degradation_curve(data['x'], *popt), 'r-', label='Fit: a=%5.3f, b=%5.3f' % tuple(popt))
plt.legend()
plt.xlabel('x')
plt.ylabel('y')
plt.show()

import pandas as pd
import numpy as np
from scipy import integrate
from scipy import interpolate
import math
import matplotlib.pyplot as plt
import glob
import figstyle

base = 'trappe_methane_reference_free_energy'
data = pd.read_csv(f'{base}.csv', skipinitialspace=True)

fig, ax = plt.subplots(1, 1, figsize=(3.4,2.0))

styles = ['-', '-', '-', '-']
# styles = ['-', '--', ':', '-.']
colors = ['green', 'orange', 'blue', 'red']
# markers = ['o', 's', '^', 'v']

k = 8.3145E-3  # kJ/mol.K
temperatures = [300, 1200, 10000]

for T, style, color in zip(temperatures, styles, colors):
    x = data['lambda_vdw']
    y = np.exp(-data['F']/(k*T))
    y_spline = interpolate.BSpline(x, y, 2)
    x_smooth = np.linspace(x.min(), x.max(), 201)
    y_smooth = y_spline(x_smooth)
    y_smooth /= integrate.simps(y_smooth, x=x_smooth)
    p = ax.plot(x_smooth, y_smooth, linestyle=style, color=color, label=f'T = {T} K')

ax.set_xlabel(r'$\lambda_\mathrm{vdW}$')
ax.set_ylabel('Probability Density')
ax.set_xlim(left=0, right=1)
ax.set_ylim(bottom=0, top=3.5)
ax.legend()

plt.savefig(base)
plt.show()

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib._color_data as mcd

import figstyle

fig, ax = plt.subplots(2, 1, figsize=(3.4,4.5))
fig.subplots_adjust(hspace=0.3)

timesteps = [1, 3, 6, 9, 15, 30, 45, 90]

n = len(timesteps)
F_vdw = np.empty(n)
dF_vdw = np.empty(n)
F_sc = np.empty(n)
dF_sc = np.empty(n)

solutes = ['methanol', 'phenol', 'dioxane', 'dibenzo-p-dioxin']
models = ['gaff', 'gaff', 'gaff', 'gaff']
dt = 1
for solute, model in zip(solutes, models):
	label = f'{dt} fs'
	data = pd.read_csv(f'{solute}/{model}_{solute}_vdw_free_energies_{dt:02d}fs.csv')
	p = ax[0].plot(data['lambda'], data['F'], label=label, linestyle='None', marker='o', markersize=2)

	data = pd.read_csv(f'{solute}/{model}_{solute}_vdw_reweighting_{dt:02d}fs.csv')
	ax[0].plot(data['lambda'], data['F'], label=None, color=p[0].get_color())

	data = pd.read_csv(f'{solute}/{model}_{solute}_softcore_free_energies_{dt:02d}fs.csv')
	ax[1].plot(data['lambda'], data['F'], linestyle='--', marker='s', markersize=2,
	           color=p[0].get_color(), label=solute)

	for axis in ax:
		axis.set_ylim(bottom=0, top=20)
		axis.set_ylim(bottom=0, top=20)
		axis.set_xlabel(r'$\lambda$')
		axis.set_ylabel('Free Energy (kcal/mol)')
		axis.set_xlim(left=0, right=1)

ax[1].legend()
plt.savefig('all_molecules_vdw_profiles')
plt.show()

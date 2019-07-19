import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib._color_data as mcd

import figstyle

fig1, ax1 = plt.subplots(1, 1, figsize=(3.2, 2))
fig2, ax2 = plt.subplots(1, 1, figsize=(3.2, 2))
ax = [ax1, ax2]

model = 'gaff'
solute = 'dioxane'
timesteps = [1, 3, 6, 9, 15, 30, 45, 90]

n = len(timesteps)

solutes = ['methanol', 'phenol', 'dioxane', 'dibenzo-p-dioxin']
models = ['gaff', 'gaff', 'gaff', 'gaff']
for solute, model in zip(solutes, models):
	F_vdw = np.empty(n)
	dF_vdw = np.empty(n)
	F_sc = np.empty(n)
	dF_sc = np.empty(n)

	for i in range(n):
	    dt = timesteps[i]
	    label = f'{dt} fs'
	    data = pd.read_csv(f'{solute}/{model}_{solute}_vdw_free_energies_{dt:02d}fs.csv')
	    F_vdw[i] = data['F'].values[-1]
	    dF_vdw[i] = data['dF'].values[-1]

	    data = pd.read_csv(f'{solute}/{model}_{solute}_softcore_free_energies_{dt:02d}fs.csv')
	    F_sc[i] = data['F'].values[-1]
	    dF_sc[i] = data['dF'].values[-1]

	p = ax[0].errorbar(timesteps, F_vdw, 1.96*dF_vdw, marker='o', linestyle='-', label=solute)
	ax[0].fill_between(timesteps, F_vdw-1.96*dF_vdw, F_vdw+1.96*dF_vdw, alpha=0.1, color=p[0].get_color())

	p = ax[1].errorbar(timesteps, F_sc, 1.96*dF_sc, marker='o', linestyle='-', label=solute)
	ax[1].fill_between(timesteps, F_sc-1.96*dF_sc, F_sc+1.96*dF_sc, alpha=0.1, color=p[0].get_color())

	for axis, coupling in zip(ax, ['Scaling', 'Softcore']):
		axis.set_xlabel('Overall time step (fs)')
		axis.set_ylabel(f'{coupling} Free Energy (kcal/mol)')
		axis.set_ylim(bottom=0.0, top=2.2)
		axis.set_xscale('log')

ax[1].legend(ncol=2)
fig1.savefig(f'{model}_{solute}_vdw_free_energy_profiles')
fig2.savefig(f'{model}_{solute}_vdw_free_energies')
plt.show()

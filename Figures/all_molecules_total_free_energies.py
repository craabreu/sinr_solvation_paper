import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib._color_data as mcd

import figstyle

fig, axis = plt.subplots(1, 1, figsize=(3.4, 2))
fig.subplots_adjust(hspace=0.3)

timesteps = [1, 3, 6, 9, 15, 30, 45, 90]

n = len(timesteps)

df = pd.DataFrame(index=timesteps)
solutes = ['methanol', 'phenol', 'dioxane', 'dibenzo-p-dioxin']
models = ['gaff', 'gaff', 'gaff', 'gaff']
for solute, model in zip(solutes, models):
	F_sc = np.empty(n)
	dF_sc = np.empty(n)
	F_coul = np.empty(n)
	dF_coul = np.empty(n)

	for i in range(n):
	    dt = timesteps[i]
	    label = f'{dt} fs'
	    data = pd.read_csv(f'{solute}/{model}_{solute}_softcore_free_energies_{dt:02d}fs.csv')
	    F_sc[i] = data['F'].values[-1]
	    dF_sc[i] = data['dF'].values[-1]

	    data = pd.read_csv(f'{solute}/{model}_{solute}_coul_free_energies_{dt:02d}fs.csv')
	    F_coul[i] = data['F'].values[-1]
	    dF_coul[i] = data['dF'].values[-1]

	F = F_sc + F_coul
	dF = dF_sc + dF_coul
	p = axis.errorbar(timesteps, F, 1.96*dF, marker='o', linestyle='-', label=solute)
	axis.fill_between(timesteps, F-1.96*dF, F+1.96*dF, alpha=0.1, color=p[0].get_color())


	df[f'F_{solute}'] = F
	df[f'dF_{solute}'] = 1.96*dF

axis.set_xlabel('Overall time step (fs)')
axis.set_ylabel('Solvation Free Energy (kcal/mol)')
axis.set_xscale('log')
axis.set_ylim(top=-2, bottom=-6)

#axis.legend(ncol=2, loc=(0.1, 0.3))
axis.legend(ncol=2)
plt.savefig('all_molecules_total_free_energies')

print(df.transpose().to_latex())

plt.show()

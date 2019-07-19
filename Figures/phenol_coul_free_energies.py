import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib._color_data as mcd

import figstyle

fig1, ax1 = plt.subplots(1, 1, figsize=(3.2, 2))
fig2, ax2 = plt.subplots(1, 1, figsize=(3.2, 2))
ax = [ax1, ax2]

model = 'gaff'
solute = 'phenol'
timesteps = [1, 3, 6, 9, 15, 30, 45, 90]

n = len(timesteps)
F_coul = np.empty(n)
dF_coul = np.empty(n)

colors = [
	'#b2182b',
	'#d6604d',
	'#f4a582',
	'#fddbc7',
	'#d1e5f0',
	'#92c5de',
	'#4393c3',
	'#2166ac',
]

for i in range(n):
    dt = timesteps[i]
    color = colors[i]
    label = f'{dt} fs'
    data = pd.read_csv(f'{solute}/{model}_{solute}_coul_free_energies_{dt:02d}fs.csv')
    ax[0].plot(data['lambda'], data['F'], label=label, linestyle='None', marker='o', markersize=2, color=color)
    F_coul[i] = data['F'].values[-1]
    dF_coul[i] = data['dF'].values[-1]

    data = pd.read_csv(f'{solute}/{model}_{solute}_coul_reweighting_{dt:02d}fs.csv')
    ax[0].plot(data['lambda'], data['F'], label=None, color=color)

# ax[0].annotate('scaling', xy=(0.1, 0.45), xycoords='axes fraction', rotation=40)

ax[0].set_xlabel(r'$\lambda$')
ax[0].set_ylabel('Free Energy (kcal/mol)')
ax[0].set_xlim(left=0, right=1)
# ax[0].set_ylim(bottom=0, top=15)
# ax[0].set_yticks(5*np.arange(4))
# ax[0].set_ylim(bottom=-2)
ax[0].legend(ncol=2)

color = 'xkcd:blue'
ax[1].errorbar(timesteps, F_coul, 1.96*dF_coul, color=color, marker='o', linestyle='-', label='scaling')
ax[1].fill_between(timesteps, F_coul-1.96*dF_coul, F_coul+1.96*dF_coul, color=color, alpha=0.1)

ax[1].set_xlabel('Overall time step (fs)')
ax[1].set_ylabel('Coupling Free Energy (kcal/mol)')
# ax[1].set_ylim(bottom=0)
ax[1].set_xscale('log')
# ax[1].legend()

fig1.savefig(f'{model}_{solute}_coul_free_energy_profiles')
fig2.savefig(f'{model}_{solute}_coul_free_energies')
plt.show()

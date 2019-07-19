import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib._color_data as mcd

import argparse
import figstyle

parser = argparse.ArgumentParser()
parser.add_argument('solute', help='the solute name', choices=['methane', 'phenol'])
args = parser.parse_args()

fig, ax = plt.subplots(2, 1, figsize=(3.4,4.5))
fig.subplots_adjust(hspace=0.3)

model = 'trappe' if args.solute == 'methane' else 'gaff'
timesteps = [1, 3, 6, 9, 15, 30, 45, 90]

n = len(timesteps)
F_vdw = np.empty(n)
dF_vdw = np.empty(n)
F_sc = np.empty(n)
dF_sc = np.empty(n)

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
    data = pd.read_csv(f'{args.solute}/{model}_{args.solute}_vdw_free_energies_{dt:02d}fs.csv')
    ax[0].plot(data['lambda'], data['F'], label=label, linestyle='None', marker='o', markersize=2, color=color)
    F_vdw[i] = data['F'].values[-1]
    dF_vdw[i] = data['dF'].values[-1]

    data = pd.read_csv(f'{args.solute}/{model}_{args.solute}_vdw_reweighting_{dt:02d}fs.csv')
    ax[0].plot(data['lambda'], data['F'], label=None, color=color)

    data = pd.read_csv(f'{args.solute}/{model}_{args.solute}_softcore_free_energies_{dt:02d}fs.csv')
    ax[0].plot(data['lambda'], data['F'], label=None, linestyle='--', marker='s', markersize=2, color=color)
    F_sc[i] = data['F'].values[-1]
    dF_sc[i] = data['dF'].values[-1]

ax[0].annotate('scaling', xy=(0.1, 0.45), xycoords='axes fraction', rotation=56)
ax[0].annotate('softcore', xy=(0.2, 0.25), xycoords='axes fraction', rotation=45)

ax[0].set_xlabel(r'$\lambda$')
ax[0].set_ylabel('Free Energy (kcal/mol)')
ax[0].set_xlim(left=0, right=1)
# ax.set_ylim(bottom=0, top=3.5)
ax[0].legend(ncol=2)

color = 'xkcd:blue'
ax[1].errorbar(timesteps, F_vdw, 1.96*dF_vdw, color=color, marker='o', linestyle='-', label='scaling')
ax[1].fill_between(timesteps, F_vdw-1.96*dF_vdw, F_vdw+1.96*dF_vdw, color=color, alpha=0.1)

color = 'xkcd:orange'
ax[1].errorbar(timesteps, F_sc, 1.96*dF_sc, color=color, marker='o', linestyle='-', label='softcore')
ax[1].fill_between(timesteps, F_sc-1.96*dF_sc, F_sc+1.96*dF_sc, color=color, alpha=0.1)

ax[1].set_xlabel('Overall time step (fs)')
ax[1].set_ylabel('Solvation Free Energy (kcal/mol)')
# ax[1].set_ylim(bottom=0)
ax[1].set_xscale('log')
ax[1].legend()

plt.savefig(f'{model}_{args.solute}_vdw_free_energies')
plt.show()

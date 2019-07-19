import matplotlib.pyplot as plt

params = {
	'font.size': 8,
	'text.usetex': True,
	'lines.linewidth': 0.5,
	'lines.markersize': 4,
	'errorbar.capsize': 2,
	'legend.frameon': False,
	'legend.columnspacing': 1,
	'savefig.format': 'png',
	'savefig.dpi': 600,
	'savefig.bbox': 'tight',
	'figure.subplot.hspace': 0.1,
}

plt.style.use('seaborn-dark-palette')
plt.rcParams.update(params)

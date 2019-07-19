import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib._color_data as mcd

import figstyle

fig, axis = plt.subplots(1, 1, figsize=(3.2, 2))

x = np.linspace(0, 1, 201)

functions = [
	np.vectorize(lambda x: x),
	np.vectorize(lambda x: x - np.sin(2*np.pi*x)/(2*np.pi)),
	np.vectorize(lambda x: x**3*(10 - 15*x + 6*x**2)),
	np.vectorize(lambda x: x**4*(5 - 4*x)),
]

equations = [
	'$\\lambda$',
	'$\\lambda - \\frac{\\sin(2\\pi \\lambda)}{2\\pi}$',
	'$\\lambda^3 (10 - 15 \\lambda + 6\\lambda^2)$',
	'$\\lambda^4 (5 - 4 \\lambda)$',
]

names = [
	'Linear coupling',
	'Abrams \\textit{et al}. (2006)',
# 	'5\\textsuperscript{th}-degree switch',
	'$g = 1 - f_5(\\lambda)$',
	'$g = \\lambda^4(5-4\\lambda)$',
]

for name, equation, function in zip(names, equations, functions):
	axis.errorbar(x, function(x), label=name)

axis.set_xlabel('$\\lambda$')
axis.set_ylabel('$g(\\lambda)$')
axis.set_xlim(0, 1)
axis.set_ylim(0, 1)
axis.legend()

plt.savefig('coupling_functions')
plt.show()

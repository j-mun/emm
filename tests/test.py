

import emm
import matplotlib.pyplot as plt
import numpy as np

emm.avail()

emm.avail('Ag')



f,e = emm.read('Ag\\Johnson.yaml', 'm','e')

plt.figure()
plt.plot(f, np.real(e))
plt.plot(f, np.imag(e))
plt.show()


f = np.linspace(400e-9, 900e-9, 101)
e = emm.load('Ag/Johnson', )

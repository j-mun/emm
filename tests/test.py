

import emm
import matplotlib.pyplot as plt
import numpy as np

emm.avail()

emm.avail('Ag')



f,e = emm.read('Ge/Aspnes', 'm','e')

plt.figure()
plt.plot(f, np.real(e))
plt.plot(f, np.imag(e))
plt.show()



f = np.linspace(400e-9, 900e-9, 101)
n = emm.load('Ag/Johnson', f)

plt.figure()
plt.plot(f, np.real(n))
plt.plot(f, np.imag(n))
plt.show()



f = np.linspace(400e-9, 900e-9, 101)
n = emm.load('Ag/Johnson', f, interp='cubic')

plt.figure()
plt.plot(f, np.real(n))
plt.plot(f, np.imag(n))
plt.show()

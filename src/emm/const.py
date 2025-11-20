"""emm.const







Jungho Mun, 2019-07-11
Pohang University of Science and Technology (POSTECH), Korea

THIS FILE IS PART OF EMM LIBRARY
"""

_values = {
  "c": 299792458,
  "eps0": 8.8541878128e-12,
  "mu0": 1.25663706212e-6,
  "eta0": 376.730313668,
  "h": 6.62607015e-34,
  "hbar": 1.054571817e-34,
  "hbar_eV": 6.582119569e-16,
  "e": 1.602176634e-19,
  "m_e": 9.1093837015e-31,
  "m_p": 1.67262192369e-27,
  "N_A": 6.02214076e+23,
  "eV": 1.602176634e-19,
  "a": 7.2973525693e-3,
  "k": 1.380649e-23,
  "amu": 1.6605390666e-27,
  "a0": 5.291772109e-11,
  "Eh": 4.3597447222071e-18,
}

def const(
    p:str=None
  ):
  """list of physical constants

  constant          value                   unit            ref
  ---------------------------------------------------------------------
  c     	| 299 792 458           | [m/s]             | CODATA-18
  eps0  	| 8.854 187 8128 e-12   | [C/V/m = F/m]     | CODATA-18
  mu0   	| 1.256 637 062 12 e-6  | [V/A*s/m = H/m]   | CODATA-18
  eta0    | 376.730 313 668       | [V/A = ¥Ø]         | CODATA-18
  h       | 6.626 070 15 e-34     | [J/Hz]            | CODATA-18
  hbar  	| 1.054 571 817 e-34    | [J*s]             | CODATA-18
  hbar_eV | 6.582 119 569 e-16    | [eV*s]            |
  e     	| 1.602 176 634 e-19    | [C]               | CODATA-18
  m_e   	| 9.109 383 7015 e-31   | [kg]              | CODATA-18
  m_p     | 1.672 621 923 69 e-27 | [kg]              | CODATA-18
  N_A   	| 6.022 140 76 e+23     | [1/mol]           | CODATA-18
  eV      | 1.602 176 634 e-19    | [J]               | CODATA-18
  a       | 7.297 352 5693 e-3    |                   | CODATA-18
  k       | 1.380 649 e-23        | J/K               | CODATA-18
  amu     | 1.660 539 066 60 e-27 | kg                | CODATA-18
  a0      | 5.291 772 109 03 e-11 | m                 | CODATA-18
  Eh      | 4.359 744 722 2071 e-18 | J               | CODATA-18
  E       | *                     | [V/m]             
  D       | *                     | [C/m^2]
  B       | *                     | [V*s/m^2 = T]
  H       | *                     | [A/m]
  """

  if p is None:
    print(__doc__)
    return
  
  if p in _values.keys():
    return _values[p]
  
  else:
    raise ValueError(f"the key {p} does not exist.")
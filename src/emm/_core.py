"""


THIS FILE IS PART OF EMM LIBRARY
"""

import os
import sys
import numpy as np
import yaml

_path = os.path.abspath(__file__)
_dir = os.path.dirname(_path)
_src = os.path.dirname(_dir)
_dat = _src + '\\dat'


print(_path)
print(_dir)
print(_dat)






def avail(
    name:str=None,
    dat:str=None
  )->None:
  """
  Args:
    name: name of the material or project
    dat: data directory
  """

  if dat is None:
    dat = _dat
  
  if name is not None:
    dat += '/' + name

  if name is None:
    dirs = [d for d in os.listdir(dat) if os.path.isdir(os.path.join(dat, d))]
    print(dirs)
    return
  
  else:
    files = [f for f in os.listdir(dat) if os.path.isfile(os.path.join(dat, f))]
    print(files)
    return



def _read(
    file:str
  ):
  """read a raw file
  
  Args:
    file: file name

  Returns:
    f: frequency
    re: real part of material property
    im: imaginary part of material property
    unit: frequency units
    parm: material property {'n' or 'e'}
  """
  with open(file, 'r') as f:
    data = yaml.safe_load(f)['DATA'][0]
    unit = data["unit"]
    parm = data["parm"]
    dat = np.fromstring(data['data'], dtype=float, sep=' ').reshape(-1,3)
    f = dat[:,0]
    re = dat[:,1]
    im = dat[:,2]

  return (
    f,
    re,
    im,
    unit,
    parm
  )


def read(
    name:str,
    unit:str='m',
    parm:str='n',
    dat:str=None
  ):
  """read a raw data
  """

  if name is None:
    raise ValueError('emm::read::material name should be provided!')
  
  if dat is None:
    dat = _dat
  
  dat += '\\' + name

  f,re,im,raw_unit,raw_parm = _read(dat)

  # convert frequency units
  f = _convert_unit(f, f'{raw_unit}->{unit}')

  # convert parameter
  re,im = _convert_parm(re, im, f'{raw_parm}->{parm}')

  return (
    f,
    re+1j*im
  )




def load(
    name:str,
    w:np.ndarray
  ):
  """
  
  
  """
  pass


# interp

# warning for out-of-bounds

# export raw data (with unit/param conversion)








from .const import _values as _const

def _convert_unit(
    f:np.ndarray,
    key:str="m->m"
  ):
  """
  Hz, GHz, THz, 
  eV
  nm, um, m

  """
  parts = key.split('->')
  unit_i = parts[0]
  unit_j = parts[1]

  if unit_i == unit_j:
    return f
  
  # convert to [m]
  match unit_i:
    case 'm': # [?]->[m]
      pass
    case 'nm':
      f *= 1e-9
    case 'um':
      f *= 1e-6
    case 'Hz':
      f = _const['c'] / f
    case 'GHz':
      f = 1e-9 * _const['c'] / f
    case 'THz':
      f = 1e-12 * _const['c'] / f
    case 'cm-1':
      f = 100.0 / f
    case 'eV':
      f = 2*np.pi*_const['c']*_const['hbar_eV'] / f

  # convert to the final unit
  match unit_j: # [m]->[?]
    case 'm':
      pass
    case 'nm':
      f *= 1e+9
    case 'um':
      f *= 1e+6
    case 'Hz':
      f = _const['c'] / f
    case 'GHz':
      f = 1e-9 * _const['c'] / f
    case 'THz':
      f = 1e-12 * _const['c'] / f
    case 'cm-1':
      f = 100.0 / f
    case 'eV':
      f = 2*np.pi*_const['c']*_const['hbar_eV'] / f

  return f


def _convert_parm(
    re:np.ndarray,
    im:np.ndarray,
    key:str="n->n"
  ):
  """
  Args:
    parm: {'n','nk','e','eps'}
    key: {'n->n','n->nk','n->e','n->eps', ...}
  """
  parts = key.split('->')
  
  parm_i = parts[0]
  parm_j = parts[1]

  if parm_i == 'nk':
    parm_i = 'n'
  elif parm_i == 'eps':
    parm_i = 'e'
  
  if parm_j == 'nk':
    parm_j = 'n'
  elif parm_j == 'eps':
    parm_j = 'e'

  if parm_i == parm_j:
    return (re, im)
  
  elif parm_i == 'n': # [n]->[e]
    return (re**2-im**2, 2*re*im)
  
  else: # [e]->[n]
    z = np.sqrt(re + 1j*im)
    return (np.real(z), np.imag(z))







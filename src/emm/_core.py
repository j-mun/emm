"""
THIS FILE IS PART OF EMM LIBRARY
"""

import os
import sys
import numpy as np
import scipy
import yaml


_path = os.path.abspath(__file__)
_dir = os.path.dirname(_path)
_src = os.path.dirname(_dir)
_default_dat = os.path.join(_src, '_emm_dat')
'''default data directory'''

from .const import _values as _const
def convert_unit(
    f:np.ndarray,
    option:str="m->m"
  ):
  """convert frequency units

  Args:
    f (np.ndarray): input frequency
    key (str): conversion option, e.g., 'm->nm' or 'm->THz'

  Returns:
    f (np.ndarray): converted frequency

  List of units:
    {m, um, nm, Hz, GHz, THz, eV, cm-1}
  """
  unit_i, unit_j = option.split('->')


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
    option:str="n->n"
  ):
  """
  Args:
    parm: {'n','nk','e','eps'}
    option: {'n->n','n->nk','n->e','n->eps', ...}
  """
  parm_i, parm_j = option.split('->')

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


def _read(
    file:str,
    verbose:bool=True
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
    raw = yaml.safe_load(f)
    data = raw['DATA'][0]
    unit = data["unit"]
    parm = data["parm"]
    dat = np.fromstring(data['data'].replace(',',' '), dtype=float, sep=' ').reshape(-1,3)
    f = dat[:,0]
    re = dat[:,1]
    im = dat[:,2]

  if verbose:
    print(f'  importing... {raw['NAME']}')

  return (
    f,
    re,
    im,
    unit,
    parm
  )








#==============================================
def read(
    name:str,
    unit:str='m',
    parm:str='n',
    dat:str=None,
    return_complex:bool=True,
    verbose:bool=True
  ):
  """read a raw data
  """

  if name is None:
    raise ValueError('emm::read::material name should be provided!')
  
  if dat is None:
    dat = _default_dat
  elif not os.path.isdir(dat) or not os.path.exists(dat):
    raise ValueError('emm::read::data directory does not exist!')

  # set full file path
  filepath = os.path.join(dat, name)
  filename, ext = os.path.splitext(filepath)
  if ext == '.yml' or ext == '.yaml':
    filename = filepath
  elif os.path.isfile(filename+'.yml'):
    filename += '.yml'
  elif os.path.isfile(filename+'.yaml'):
    filename += '.yaml'
  else:
    raise ValueError('emm::read::raw file does not exist!')

  # read raw data
  f,re,im,raw_unit,raw_parm = _read(filename, verbose=verbose)

  # convert frequency units
  f = convert_unit(f, f'{raw_unit}->{unit}')

  # convert parameter
  re,im = _convert_parm(re, im, f'{raw_parm}->{parm}')

  if return_complex:
    return (f,re+1j*im)
  else:
    return (f,re,im)


#==============================================
def load(
    name:str,
    f:np.ndarray,
    unit:str='m',
    parm:str='n',
    interp:str='linear',
    extrap:str='constant', # extrap?
    dat:str=None,
    verbose:bool=True
  ):
  """
  
  print help if name is None?
  
  """
  if verbose:
    print(
      '-------------------------------'
      'emm::load'
      '-------------------------------'
    )

  # read raw data
  raw_f,raw_re,raw_im = read(name, unit, parm, dat, False, verbose=verbose)

  # check data range
  _check_range(f, raw_f)

  # interp
  if interp == 'linear':
    re = _interp_linear(f, raw_f, raw_re)
    im = _interp_linear(f, raw_f, raw_im)
  elif interp == 'cubic':
    re = _interp_cubic(f, raw_f, raw_re)
    im = _interp_cubic(f, raw_f, raw_im)
  else:
    raise NotImplementedError('emm::load::interpolation method is not implemented!')

  if verbose:
    print('  exporting interpolated data...')

  return re+1j*im

def _interp_linear(f, fi, vi):
  return np.interp(f, fi, vi)

def _interp_cubic(f, fi, vi):
  return scipy.interpolate.interp1d(fi, vi, kind='cubic', fill_value='extrapolate')(f)


# interp

def _check_range(
    f:np.ndarray,
    raw_f:np.ndarray
  ):
  if np.min(raw_f) > np.min(f):
    print('emm::warning::minimum out-of-range!')

  if np.max(raw_f) < np.max(f):
    print('emm::warning::maximum out-of-range!')
  return None





#==============================================
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
    dat = _default_dat
  elif not os.path.isdir(dat) or not os.path.exists(dat):
    raise ValueError('emm::avail::data directory does not exist!')
  
  if name is not None:
    # dat += _sep + name
    dat = os.path.join(dat, name)
  elif not os.path.isdir(dat) or not os.path.exists(dat):
    raise ValueError('emm::avail::data directory does not exist!')

  if name is None:
    print('> list of available materials:')
    dirs = [d for d in os.listdir(dat) if os.path.isdir(os.path.join(dat, d))]
    print(dirs)
    return
  
  else:
    print(f'> list of available models for {name}:')
    files = [
        os.path.splitext(f)[0] for f in os.listdir(dat) 
        if os.path.isfile(os.path.join(dat, f)) and f.lower().endswith(('.yml', '.yaml'))
    ]
    print(files)
    return

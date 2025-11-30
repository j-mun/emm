# emm | A Python electromagnetic material manager

This package helps managing tabulated electromagnetic material properties (refractive index or permittivity). 

# Features

- A material database with some common materials are provided (`_emm_dat` directory)

- Read raw material properties from the material database (`emm.read()`)

- Load interpolated material properties (`emm.load()`)

- Control over frequency units (`m, um, nm, Hz, GHz, THz, eV, ...`)

- Control over material parameter (`n` or `eps`)

- Check available materials and models from the database (`emm.avail()`)

- Use custom material database (`dat=/path/to/database`)

# Installation

```bash
python -m pip install .
```

# Usages

For basic usages, see `basics.ipynb` notebook.

To use custom database, see `custom_data.ipynb` notebook.

To use physics constants, see `const.ipynb` notebook.

# TODO

- Drude model

- Lorentz-Drude model
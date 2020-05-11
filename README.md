# CACmb convertor Toolkit

This toolkit contains Python programs that allow for CAC data file pre/post processing outside the scope of the core Fortran code.

The only package dependency is `numpy`. You can use pip to install these directly.

## convertor (_under development_)



The conversion type is inferred from file extension provided as input and output arguments

Currently supported conversions:

| From      | To        | Notes      |
| ------    | ------    | ------     |
| *.nodal   | *.cac     | readable by LAMMPS-CAC `read_data`     |
|           | *.last    | mixed-resolution NEB replica |
|           | *.cacovito| visualization of CAC nodes in OVITO     |


### Installation and usage
Virtual environments are recommended. From this directory...
```
pip install .
```

**Examples**

```
python -m convertor -h
python -m convertor -i INPUTFILE -o OUTPUTFILE
python -m convertor -i input.nodal -o output.cac
```


# pytetra

TETRA implementation in Python.

This projects implements the various layers of the TETRA protocol. 

Note : this project is under development and could be to heavily changed.

## Installation

```
git clone https://github.com/Tim---/pytetra.git
cd pytetra
python setup.py install
```

## Usage

The script `example/dump.py` reads a file containing unpacked binary data and dumps the decoded PDUs.

```
cd examples
python dump.py testnet.bits
```

The example file is provided by Dieter Spaar (http://tetra.osmocom.org/trac/wiki/Test_Samples).

# MicroPython for PiCoMo

This repository defines the PiCoMo MicroPython board with custom Python
and C modules.  The core MicroPython repository is a submodule and other
code, including board definitions, is part of this repository.

To set up MicroPython, check out the submodule and build `mpy-cross`:

    $ git submodule update --init lib/micropython
    $ make -C lib/micropython/mpy-cross

The various custom boards will require certain submodules of MicroPython
itself.  These can be initialised via:

    $ cd lib/micropython
    $ git submodule update --init lib/stm32lib lib/berkeley-db-1.xx
    $ cd ../..
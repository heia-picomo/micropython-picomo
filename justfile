mpy-cross:
    git submodule update --init lib/micropython
    make -C lib/micropython/mpy-cross

submodules:
    make -C lib/micropython/ports/rp2 submodules

build:
    make -C boards/HEIAFR_PICOMO

clean:
    make -C lib/micropython/ports/rp2 clean
    make -C boards/HEIAFR_PICOMO clean

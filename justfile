default: build

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

update-upstream:
    #! /bin/bash
    git submodule update --recursive --remote
    git submodule foreach --recursive git reset --hard
    git submodule update --init --recursive
    cd lib/micropython
    tag=$(git describe --tags $(git rev-list --tags --max-count=1))
    git checkout $tag
    cd ../..
    make -C lib/micropython/ports/rp2 submodules
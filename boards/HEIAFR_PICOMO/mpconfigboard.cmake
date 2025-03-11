# cmake file for HEIA-FR PiCoMo V2
set(PICO_BOARD "pico")
set(PICO_PLATFORM "rp2040")

set(USER_C_MODULES
    ${MICROPY_BOARD_DIR}/../../src/st7789_mpy/st7789/micropython.cmake
)

set(MICROPY_FROZEN_MANIFEST ${MICROPY_BOARD_DIR}/manifest.py)
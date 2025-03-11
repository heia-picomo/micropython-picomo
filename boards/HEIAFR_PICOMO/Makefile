# Makefile for custom MicroPython PiCoMo board.

BOARD ?= HEIAFR_PICOMO
MICROPY_TOP ?= $(abspath ../../lib/micropython)
PYTHON ?= python3

all: firmware

BOARD_DIR = $(abspath .)
BUILD = $(abspath build)

include $(MICROPY_TOP)/py/mkenv.mk
include $(MICROPY_TOP)/py/mkrules.mk

firmware:
	$(Q)$(MAKE) -C $(MICROPY_TOP)/ports/rp2 \
		PROJECT_TOP=$(abspath ../..) \
		BOARD=$(BOARD) \
		BOARD_DIR=$(BOARD_DIR) \
		BUILD=$(BUILD)

# include default manifest
include("$(PORT_DIR)/boards/manifest.py")

# include our own extra...
module("picomo.py", base_path="$(BOARD_DIR)/../../src/utils")
module("logo.py", base_path="$(BOARD_DIR)/../../src/utils")
module("main.py", base_path="$(BOARD_DIR)/../../src/utils")

module("fonts/bitmap/vga1_8x8.py", base_path="$(BOARD_DIR)/../../src/st7789_mpy")
module("fonts/bitmap/vga1_8x16.py", base_path="$(BOARD_DIR)/../../src/st7789_mpy")
module("fonts/bitmap/vga1_16x16.py", base_path="$(BOARD_DIR)/../../src/st7789_mpy")
module("fonts/bitmap/vga1_16x32.py", base_path="$(BOARD_DIR)/../../src/st7789_mpy")
module("fonts/bitmap/vga1_bold_16x16.py", base_path="$(BOARD_DIR)/../../src/st7789_mpy")
module("fonts/bitmap/vga1_bold_16x32.py", base_path="$(BOARD_DIR)/../../src/st7789_mpy")

module("fonts/bitmap/vga2_8x8.py", base_path="$(BOARD_DIR)/../../src/st7789_mpy")
module("fonts/bitmap/vga2_8x16.py", base_path="$(BOARD_DIR)/../../src/st7789_mpy")
module("fonts/bitmap/vga2_16x16.py", base_path="$(BOARD_DIR)/../../src/st7789_mpy")
module("fonts/bitmap/vga2_16x32.py", base_path="$(BOARD_DIR)/../../src/st7789_mpy")
module("fonts/bitmap/vga2_bold_16x16.py", base_path="$(BOARD_DIR)/../../src/st7789_mpy")
module("fonts/bitmap/vga2_bold_16x32.py", base_path="$(BOARD_DIR)/../../src/st7789_mpy")

from machine import Pin, PWM, I2C, SPI, ADC
import time
import st7789


class Buzzer:
    def __init__(self, pin):
        self.buzzer = PWM(pin, freq=4000, duty_u16=0)

    def beep(self, freq=4000, duration=200):
        self.buzzer.freq(freq)
        self.buzzer.duty_u16(32768)
        if duration > 0:
            time.sleep_ms(duration)
            self.buzzer.duty_u16(0)

    def off(self):
        self.buzzer.duty_u16(0)


class SHTC3:
    def __init__(self, sda_pin, scl_pin):
        self.addr = 0x70
        self.i2c = I2C(0, scl=scl_pin, sda=sda_pin, freq=400000)
        buf = bytearray([0x35, 0x17])
        self.i2c.writeto(self.addr, buf)
        time.sleep_ms(500)
        buf = bytearray([0xEF, 0xC8])
        self.i2c.writeto(0x70, buf)
        self.i2c.readfrom_into(0x70, buf)
        self.id = int.from_bytes(buf, "big")

    def read(self):
        buf = bytearray([0x7C, 0xA2])
        self.i2c.writeto(0x70, buf)
        buf = bytearray([0x00, 0x00, 0x00, 0x00, 0x00, 0x00])
        self.i2c.readfrom_into(0x70, buf)
        temp = (buf[1] | (buf[0] << 8)) * 175 / 65536.0 - 45.0
        humi = (buf[4] | (buf[3] << 8)) * 100 / 65536.0
        return temp, humi


class RGBLed:
    def __init__(self, pin_r, pin_g, pin_b):
        self.r = PWM(pin_r, freq=50000, duty_u16=0)
        self.g = PWM(pin_g, freq=50000, duty_u16=0)
        self.b = PWM(pin_b, freq=50000, duty_u16=0)

    def rgb(self, r, g, b):
        self.r.duty_u16(r * 65535 // 255)
        self.g.duty_u16(g * 65535 // 255)
        self.b.duty_u16(b * 65535 // 255)


def version():
    msb = Pin(13, Pin.IN, Pin.PULL_UP).value()
    lsb = Pin(14, Pin.IN, Pin.PULL_UP).value()
    code = msb * 2 + lsb
    if code == 2:
        return 3
    elif code == 3:
        return 2
    else:
        return -1


button_s1 = Pin(3, Pin.IN, Pin.PULL_UP)
button_s2 = Pin(5, Pin.IN, Pin.PULL_UP)
button_s3 = Pin(22, Pin.IN, Pin.PULL_UP)
button_s4 = Pin(7, Pin.IN, Pin.PULL_UP)
button_s5 = Pin(4, Pin.IN, Pin.PULL_UP)
button_s6 = Pin(23, Pin.IN, Pin.PULL_UP)
button_s7 = Pin(6, Pin.IN, Pin.PULL_UP)

button_up = button_s1
button_down = button_s2
button_left = button_s3
button_right = button_s4
button_middle = button_s5

if version() == 2:
    buzzer = Buzzer(Pin(11, Pin.OUT, value=0))
elif version() == 3:
    buzzer = Buzzer(Pin(12, Pin.OUT, value=0))

led = RGBLed(
    Pin(10, Pin.OUT, value=0), Pin(9, Pin.OUT, value=0), Pin(8, Pin.OUT, value=0)
)

display_spi = SPI(
    0,
    baudrate=62500000,
    polarity=0,
    phase=0,
    sck=Pin(18, Pin.OUT),
    mosi=Pin(19, Pin.OUT),
)

display = st7789.ST7789(
    display_spi,
    240,
    280,
    cs=Pin(17, Pin.OUT),
    dc=Pin(16, Pin.OUT),
    rotations=[
        (0x00, 240, 280, 0, 20),
        (0x60, 280, 240, 20, 0),
        (0xC0, 240, 280, 0, 20),
        (0xA0, 280, 240, 20, 0),
    ],
)

thermo = SHTC3(Pin(20, Pin.PULL_UP), Pin(21, Pin.PULL_UP))

adc = ADC(Pin(29))
usb_over_current = Pin(24, Pin.IN)

# SPDX-FileCopyrightText: Copyright (c) 2025 Jacques Supcik
#
# SPDX-License-Identifier: MIT

"""
Picomo library
"""


import time
import machine

from machine import PWM, Pin
from micropython import const
from st7789 import ST7789

DEFAULT_PWM_FREQ = const(4000)
DEBOUNCE_TIME = const(20 * 1000 * 1000)  # 20ms in ns


def version():
    msb = Pin(13, Pin.IN, Pin.PULL_UP).value()
    lsb = Pin(14, Pin.IN, Pin.PULL_UP).value()
    code = msb * 2 + lsb
    if code == 2:
        return 3.0
    elif code == 3:
        return 2.0
    else:
        return -1


class Singleton(object):
    _instance = None

    def __new__(class_, *args, **kwargs):
        if not isinstance(class_._instance, class_):
            class_._instance = object.__new__(class_, *args, **kwargs)
        return class_._instance


class Version(Singleton):
    def __init__(self):
        msb = Pin(13, Pin.IN, Pin.PULL_UP).value()
        lsb = Pin(14, Pin.IN, Pin.PULL_UP).value()
        code = msb * 2 + lsb
        if code == 2:
            self.version = 3.0
        elif code == 3:
            self.version = 2.0
        else:
            self.version = None

    @property
    def is_v2(self):
        return self.version == 2.0

    @property
    def is_v3(self):
        return self.version == 3.0

    def __str__(self):
        return "{}".format(self.version)


class UsbOverCurrent(Singleton, Pin):
    def __init__(self):
        super().__init__(24, Pin.IN)


class ADC(Singleton, machine.ADC):
    def __init__(self):
        super().__init__(Pin(29))


class Buzzer(Singleton):
    def __init__(self):

        v = Version()
        if v.is_v2:
            pin = Pin(11, Pin.OUT, value=0)
        elif v.is_v3:
            pin = Pin(12, Pin.OUT, value=0)
        else:
            raise ValueError("Unknown board version")
        self.buzzer = PWM(pin, freq=DEFAULT_PWM_FREQ, duty_u16=0)

    def beep(self, freq=DEFAULT_PWM_FREQ, duration=200):
        self.buzzer.freq(freq)
        self.buzzer.duty_u16(32768)
        if duration > 0:
            time.sleep_ms(duration)
            self.buzzer.duty_u16(0)
            self.buzzer.freq(DEFAULT_PWM_FREQ)

    def off(self):
        self.buzzer.duty_u16(0)
        self.buzzer.freq(DEFAULT_PWM_FREQ)


class AmbiantMeasure:
    def __init__(self, temperature, humidity):
        self.temperature = temperature
        self.humidity = humidity

    def temperature(self):
        return self.temperature

    def humidity(self):
        return self.humidity

    def __str__(self):
        return "Temperature: {} Humidity: {}".format(self.temperature, self.humidity)


class AmbiantSensor(Singleton):
    def __init__(self):
        self.addr = 0x70
        self.i2c = machine.I2C(
            0, scl=Pin(21, Pin.PULL_UP), sda=Pin(20, Pin.PULL_UP), freq=400000
        )
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
        return AmbiantMeasure(temp, humi)


class Led(Singleton):
    def __init__(self):
        v = Version()
        if v.is_v2:
            freq = DEFAULT_PWM_FREQ
        else:
            freq = 50000
        self.r = PWM(Pin(10, Pin.OUT, value=0), freq=freq, duty_u16=0)
        self.g = PWM(Pin(9, Pin.OUT, value=0), freq=freq, duty_u16=0)
        self.b = PWM(Pin(8, Pin.OUT, value=0), freq=freq, duty_u16=0)

    def rgb(self, r, g, b):
        self.r.duty_u16(r * 65535 // 255)
        self.g.duty_u16(g * 65535 // 255)
        self.b.duty_u16(b * 65535 // 255)


class Screen(Singleton, ST7789):
    def __init__(self):
        _spi = machine.SPI(
            0,
            baudrate=62500000,
            polarity=0,
            phase=0,
            sck=Pin(18, Pin.OUT),
            mosi=Pin(19, Pin.OUT),
        )
        super().__init__(
            _spi,
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
        self.init()


class Button(Pin):

    def __init__(self, id, mode=-1, pull=-1):
        super().__init__(id, mode, pull)
        self.irq(self.handler, Pin.IRQ_FALLING)
        self._pressed = False
        self._last_time = 0

    def handler(self, pin):
        _ = pin
        now = time.time_ns()
        if now - self.last_time > DEBOUNCE_TIME:
            self._pressed = True
            self._last_time = now

    def reset(self):
        self._pressed = False

    @property
    def pressed(self):
        if self._pressed:
            self._pressed = False
            return True
        return False


button_s1 = Button(3, Pin.IN, Pin.PULL_UP)
button_s2 = Button(5, Pin.IN, Pin.PULL_UP)
button_s3 = Button(22, Pin.IN, Pin.PULL_UP)
button_s4 = Button(7, Pin.IN, Pin.PULL_UP)
button_s5 = Button(4, Pin.IN, Pin.PULL_UP)
button_s6 = Button(23, Pin.IN, Pin.PULL_UP)
button_s7 = Button(6, Pin.IN, Pin.PULL_UP)

button_up = button_s1
button_down = button_s2
button_left = button_s3
button_right = button_s4
button_mid = button_s5
button_middle = button_s5
button_A = button_s6
button_B = button_s7

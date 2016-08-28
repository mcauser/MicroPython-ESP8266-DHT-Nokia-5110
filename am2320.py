"""
MicroPython Aosong AM2320 driver

Pinout (left to right, grill facing you)
1 VDD
2 SDA
3 GND
4 SCL
"""

import ustruct
import time

class AM2320:
    def __init__(self, i2c=None, address=0x5c):
        self.i2c = i2c
        self.address = address
        self.buf = bytearray(8)
    def measure(self):
        buf = self.buf
        address = self.address
        # wake sensor
        try:
        	self.i2c.writeto(address, b'')
        except OSError:
        	pass
        # read 4 registers starting at offset 0x00
        self.i2c.writeto(address, b'\x03\x00\x04')
        # wait at least 1.5ms
        time.sleep_ms(2)
        # read data
        self.i2c.readfrom_mem_into(address, 0, buf)
        # debug print
        print(ustruct.unpack('BBBBBBBB', buf))
        crc = ustruct.unpack('<H', bytearray(buf[-2:]))[0]
        if (crc != self.crc16(buf[:-2])):
            raise Exception("checksum error")
    def crc16(self, buf):
        crc = 0xFFFF
        for c in buf:
            crc ^= c
            for i in range(8):
                if crc & 0x01:
                    crc >>= 1
                    crc ^= 0xA001
                else:
                    crc >>= 1
        return crc
    def humidity(self):
        return (self.buf[2] << 8 | self.buf[3]) * 0.1
    def temperature(self):
        t = ((self.buf[4] & 0x7f) << 8 | self.buf[5]) * 0.1
        if self.buf[4] & 0x80:
            t = -t
        return t
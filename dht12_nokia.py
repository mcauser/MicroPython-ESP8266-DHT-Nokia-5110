import time, ustruct
from machine import I2C, Pin, HSPI

# Nokia 5110
import upcd8544, framebuf

# Temp sensor
import dht12

# Initialise temp sensor
i2c = I2C(scl=Pin(0), sda=Pin(2), freq=20000)

i2c.scan()
# should see sensor at [92]

dht = dht12.DHT12(i2c)

# Initialise HSPI for display
spi = HSPI(baudrate=80000000, polarity=0, phase=0)
RST = Pin(4)
CE = Pin(5)
DC = Pin(12)
BL = Pin(16)
lcd = upcd8544.PCD8544(spi, RST, CE, DC, BL)

# Initialise framebuffer for display
width = 84
height = 48
pages = height // 8
buffer = bytearray(pages * width)
framebuf = framebuf.FrameBuffer1(buffer, width, height)

# Update display
while(True):
	dht.measure()
	framebuf.fill(0)
	framebuf.text("DHT12 I2C", 0, 0, 1)
	framebuf.text("Temp", 0, 11, 1)
	framebuf.text("%.1f" % dht.temperature(), 0, 20, 1)
	framebuf.text("Humidity", 0, 31, 1)
	framebuf.text("%.1f" % dht.humidity(), 0, 40, 1)
	lcd.data(buffer)
	time.sleep_ms(4000)

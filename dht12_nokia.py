import time, ustruct
from machine import I2C, Pin, SPI

# Nokia 5110
import pcd8544, framebuf

# Temp sensor
import dht12

# Initialise I2C for temp sensor
i2c = I2C(scl=Pin(0), sda=Pin(2), freq=20000)

i2c.scan()
# should see sensor at [92]

dht = dht12.DHT12(i2c)

# Initialise SPI for display
spi = SPI(1, baudrate=80000000, polarity=0, phase=0)
cs = Pin(2)
dc = Pin(15)
rst = Pin(0)

# backlight on
bl = Pin(12, Pin.OUT, value=1)

lcd = pcd8544.PCD8544(spi, cs, dc, rst)

# Initialise framebuffer for display
buffer = bytearray((lcd.height // 8) * lcd.width)
framebuf = framebuf.FrameBuffer1(buffer, lcd.width, lcd.height)

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

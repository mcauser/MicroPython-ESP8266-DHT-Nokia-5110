# MicroPython ESP8266 DHT Nokia 5110

WeMos D1 mini + AM2320 + DHT12 + Nokia 5110 (PCD8544)

![DHT Nokia](https://raw.github.com/mcauser/MicroPython-ESP8266-DHT-Nokia-5110/master/photos/dht-nokia.jpg)

## Parts

* [WeMos D1 Mini](http://www.aliexpress.com/store/product/D1-mini-Mini-NodeMcu-4M-bytes-Lua-WIFI-Internet-of-Things-development-board-based-ESP8266/1331105_32529101036.html) $4.00 USD
* [Nokia 5110 module](http://www.aliexpress.com/item/1pc-Lowest-Price-84-48-84x84-LCD-Module-White-backlight-adapter-PCB-for-Nokia-5110-Newest/32401396134.html) $2.10 USD
* [Breadboard 400 point](http://www.aliexpress.com/item/Quality-mini-bread-board-breadboard-8-5CM-x-5-5CM-400-holes/32347239015.html) $1.02 USD
* [Jumper wire](http://www.aliexpress.com/item/Free-Shipping-140pcs-in-one-package-convenient-New-Solderless-Flexible-Breadboard-Jumper-wires-Cables-HOT-Sale/2044172287.html) $1.72 USD
* [DHT12](http://www.aliexpress.com/item/DHT12-Digital-Temperature-and-Humidity-Sensor-Fully-compatible-with-DHT11/32654795239.html) $0.92 USD
* [AM2320](http://www.aliexpress.com/item/AM2320-Digital-Temperature-and-Humidity-Sensor-Original-authentic-Can-replace-SHT20-SHT10/32653665528.html) $1.65 USD

## Pinouts

The DHT12 and AM2320 sensors have the same pins:

* 1 VDD
* 2 SDA
* 3 GND
* 4 SCL

Using D3 + D4 for I2C on the WeMos D1 Mini.

* D3 = GPIO0 = SCL
* D4 = GPIO2 = SDA


## Installation

Start by cloning this repo.

```
$ git clone git@github.com:mcauser/MicroPython-ESP8266-DHT-Nokia-5110.git
```

* [Install MicroPython on your ESP8266 device](#install-micropython-on-your-esp8266-device)
	* [Install python](#install-python)
	* [Download latest MicroPython firmware](#download-latest-micropython-firmware)
	* [Flash firmware with esptool](#flash-firmware-with-esptool)
	* [Verify firmware](#verify-firmware)
* [Install scripts with WebREPL](#install-scripts-with-webrepl)
	* [Configure Access Point](#configure-access-point)
	* [Start WebREPL](#start-webrepl)
	* [Connect to Access Point](#connect-to-access-point)
	* [Upload files with WebREPL](#upload-files-with-webrepl)
* [Setup and test Nokia 5110 display](#setup-and-test-nokia-5110-display)
* [Setup and test DHT12](#setup-and-test-dht12)
* [Setup and test AM2320](#setup-and-test-am2320)


## Install MicroPython on your ESP8266 device

I am using a [WeMos D1 Mini](http://www.wemos.cc/Products/d1_mini.html), but you can use any ESP8266 device.

The WeMos D1 Mini features an ESP-12F with 4MB flash.

If you already have [MicroPython](http://micropython.org/) [v1.8.x](https://github.com/micropython/micropython/releases) installed on your device, you can skip down to [installing the scripts](#install-scripts-with-webrepl).

### Install Python

If you are using [brew](http://brew.sh/), installing Python 2.7 is a one-liner. Install [pip](https://pip.pypa.io/en/stable/) to manage python packages.

```
$ brew install python
$ pip install --upgrade pip setuptools
```

You can use pip to install Python packages. eg.

```
$ pip search SomePackage
$ pip install SomePackage
$ pip install --upgrade SomePackage
$ pip uninstall SomePackage
```

Install [esptool](https://github.com/themadinventor/esptool/) with pip

```
$ pip install esptool
```

### Download latest MicroPython firmware

Open [http://micropython.org/download/#esp8266](http://micropython.org/download/#esp8266)

Download the latest firmware, currently v1.8.3-61

```
$ wget http://micropython.org/resources/firmware/esp8266-20160827-v1.8.3-61-g531217a.bin
```

### Flash firmware with esptool

The WeMos D1 mini uses a [CH340G](http://www.wch.cn/download/CH341SER_MAC_ZIP.html) USB-TTL driver, which shows up on my MacBook Pro as either `/dev/tty.wchusbserial1410` or `/dev/tty.wchusbserial1420`.

If you are using another device, you may find yours to be `/dev/ttyUSB0`. Find yours with:

```
$ ls /dev/tty*
```

When deploying new firmware, it's best to completely erase all previous versions. The first run executes suspiciously quick, so I run it twice.

```
$ esptool.py -p /dev/tty.wchusbserial1420 erase_flash
esptool.py v1.1
Connecting...
Erasing flash (this may take a while)...
```

Upload the new MicroPython firmware.

```
$ esptool.py -p /dev/tty.wchusbserial1420 write_flash -fm dio -fs 32m 0 esp8266-20160827-v1.8.3-61-g531217a.bin
esptool.py v1.1
Connecting...
Running Cesanta flasher stub...
Flash params set to 0x0240
Writing 532480 @ 0x0... 43008 (8 %)
...
Writing 532480 @ 0x0... 316416 (59 %)
...
Writing 532480 @ 0x0... 532480 (100 %)
Wrote 532480 bytes at 0x0 in 46.0 seconds (92.6 kbit/s)...
Leaving...
```

More info in the [MicroPython docs](http://docs.micropython.org/en/latest/esp8266/esp8266/tutorial/intro.html#deploying-the-firmware) on flashing the firmware.

### Verify firmware

```
$ screen /dev/tty.wchusbserial1420 115200
```

Click your hardware Reset button or `Control+D` in screen.

```
(lots of funny characters) ets_task(40100390, 3, 3fff6300, 4)
could not open file 'main.py' for reading

MicroPython v1.8.3-61-g531217a on 2016-08-27; ESP module with ESP8266
Type "help()" for more information.
>>>
```

Check the firmware md5 matches. You should see True. If not, `erase_flash` and `write_flash` again, or try different `write_flash` arguments after reading the [esptool](https://github.com/themadinventor/esptool/) readme.

```
>>> import esp
>>> esp.check_fw()
size: 531032
md5: f54e36598b104f8c5dec883181080aaa
True
```

To exit screen run: `Control+A` then `Control+\`.

## Install scripts with WebREPL

I was receiving `MemoryErrors` when trying to upload the scripts via REPL paste mode.

Using WebREPL `Send a file`, I'm able to upload the scripts successfully, but with WebREPL enabled, not enough ram to run them.

Reboot with WebREPL disabled and the scripts has enough resources to run.

### Configure Access Point

The default settings will give your device the ip 192.168.4.1

```
>>> import network
>>> ap_if = network.WLAN(network.AP_IF)
>>> ap_if.active(True)
```

Yep, it's 192.168.4.1. (ip,netmask,gateway,dns)

```
>>> ap_if.ifconfig()
('192.168.4.1', '255.255.255.0', '192.168.4.1', '208.67.222.222')
```

### Start WebREPL

```
>>> import webrepl
>>> webrepl.start()
WebREPL daemon started on ws://192.168.4.1:8266
Started webrepl in setup mode
```

### Connect to Access Point

Before leaving your working internet connection, open the WebREPL http://micropython.org/webrepl/ but don't connect yet.

Join the MicroPython-xxxxxx network. Password is `micropythoN`. Uppercase N is not a typo.

You should see something like this in the REPL:

```
>>> add 1
aid 1
station: 78:31:c1:bb:cc:dd join, AID = 1
```

Switch back to WebREPL tab in your browser and click `Connect`.

It will ask you to set a password.

```
Welcome to MicroPython!
Welcome to MicroPython WebREPL!

This is the first time you connect to WebREPL, so please set a password
to use for the following WebREPL sessions. Once you enter the password
twice, your board will reboot with WebREPL running in active mode. On
some boards, you may need to press reset button or reconnect power.

New password:
```

Enter a password twice and it will save the password and reboot.

```
New password: ********
Confirm password: ********
Password successfully set, restarting...
Disconnected
```

WebREPL will be disabled when it reboots, so you will need to start it again.

Later, to make it always on, you can add the start command to boot.py. In this case, we do not want it started by default.

Switch back to your terminal and start WebREPL again

```
>>> import webrepl
>>> webrepl.start()
WebREPL daemon started on ws://192.168.4.1:8266
Started webrepl in normal mode
```

Notice this time, it says `normal mode`. FYI - the WebREPL password you entered is saved in `port_config.py` in the root.

```
>>> import os
>>> os.listdir()
['boot.py', 'port_config.py']
```

Click `Connect` and enter your password.

```
Welcome to MicroPython!
Password:
WebREPL connected
>>>
```

### Upload files with WebREPL

Under `Send a file` on the right, choose the file `upcd8544.py`. It will list the file as `upcd8544.py - 9787 bytes`.

Click `Send to device`. At the bottom it should say `Sent upcd8544.py, 9787 bytes`.

Repeat for the files `dht12.py`, `dht12_nokia.py`, `am2320.py` and `am2320_nokia.py`.

Click `Disconnect`. Click your hardware Reset button, or use `machine.reset()`.

```
>>> import machine
>>> machine.reset()
```

After rebooting, if you do not need the Access Point anymore, you can disable it with:

```
>>> import network
>>> ap_if = network.WLAN(network.AP_IF)
>>> ap_if.active(False)
station: 78:31:c1:bb:cc:dd leave, AID = 1
rm 1
bcn 0
del if1
usl
mode : null
```

### Setup and test Nokia 5110 display

Connections:

WeMos D1 Mini (ESP8266) | Nokia 5110 PCD8544 LCD | Description
----------------------- | ---------------------- | ----------------------------------------------
D2 (GPIO4)              | 0 RST                  | Output from ESP to reset display
D1 (GPIO5)              | 1 CE                   | Output from ESP to chip select/enable display
D6 (GPIO12)             | 2 DC                   | Output from display data/command to ESP
D7 (GPIO13)             | 3 Din                  | Output from ESP SPI MOSI to display data input
D5 (GPIO14)             | 4 Clk                  | Output from ESP SPI clock
3V3                     | 5 Vcc                  | 3.3V from ESP to display
D0 (GPIO16)             | 6 BL                   | 3.3V to turn backlight on, or PWM
G                       | 7 Gnd                  | Ground

Test the display:

```
>>> from machine import Pin, HSPI
>>> import time
>>> import upcd8544

>>> spi = HSPI(baudrate=80000000, polarity=0, phase=0)
>>> RST = Pin(4)
>>> CE = Pin(5)
>>> DC = Pin(12)
>>> BL = Pin(16)
>>> lcd = upcd8544.PCD8544(spi, RST, CE, DC, BL)
```

For my Nokia 5110 display, the `lcd.light_on()` and `lcd.light_off()` methods are reversed.

Switch off the backlight:

```
>>> lcd.light_on()
```

Switch on the backlight:

```
>>> lcd.light_off()
```

Use a framebuffer to store the 4032 pixels (84x48):

```
>>> import framebuf
>>> width = 84
>>> height = 48
>>> pages = height // 8
>>> buffer = bytearray(pages * width)
>>> framebuf = framebuf.FrameBuffer1(buffer, width, height)
```

Light every pixel:

```
>>> framebuf.fill(1)
>>> lcd.data(buffer)
```

Clear screen:

```
>>> framebuf.fill(0)
>>> lcd.data(buffer)
```

Print `Hello, World!` using the 8x8 font:

```
>>> framebuf.text("Hello,", 0, 0, 1)
>>> framebuf.text("World!", 0, 9, 1)
>>> lcd.data(buffer)
```

If all this works, let's try the sensors.

![Test](https://raw.github.com/mcauser/MicroPython-ESP8266-DHT-Nokia-5110/master/photos/test.jpg)

## Setup and test DHT12

![DHT12](https://raw.github.com/mcauser/MicroPython-ESP8266-DHT-Nokia-5110/master/photos/dht12.jpg)

Sensor pinout:

* 1 VDD
* 2 SDA
* 3 GND
* 4 SCL

Connections:

WeMos D1 Mini (ESP8266) | DHT12  | Description
----------------------- | ------ | ------------
3V3                     | 1 VDD  | 3.3V
D4 (GPIO2)              | 2 SDA  | Serial data
D3 (GPIO0)              | 3 SCL  | Serial clock
G                       | 4 GND  | Ground

Connect two pull-up resistors for I2C between 3V3-SDA and 3V3-SCL.

Test the DHT12 sensor:

```
>>> from machine import I2C, Pin
>>> import dht12

>>> i2c = I2C(scl=Pin(0), sda=Pin(2), freq=20000)
>>> i2c.scan()
```

You should see sensor at [92]

```
dht = DHT12(i2c)
dht.measure()
dht.temperature()
dht.humidity()
```

Display the temperature and humidity on the Nokia 5110 display, updated every 4 seconds:

```
>>> import dht12_nokia
```

## Setup and test AM2320

![AM2320](https://raw.github.com/mcauser/MicroPython-ESP8266-DHT-Nokia-5110/master/photos/am2320.jpg)

Sensor pinout:

* 1 VDD
* 2 SDA
* 3 GND
* 4 SCL

Connections:

WeMos D1 Mini (ESP8266) | AM2320 | Description
----------------------- | ------ | ------------
3V3                     | 1 VDD  | 3.3V
D4 (GPIO2)              | 2 SDA  | Serial data
D3 (GPIO0)              | 3 SCL  | Serial clock
G                       | 4 GND  | Ground

Connect two pull-up resistors for I2C between 3V3-SDA and 3V3-SCL.

Test the AM2320 sensor:

```
>>> from machine import I2C, Pin
>>> import am2320

>>> i2c = I2C(scl=Pin(0), sda=Pin(2), freq=20000)
>>> i2c.scan()
```

You should see sensor at [92]

```
>>> dht = AM2320(i2c)
>>> dht.measure()
>>> dht.temperature()
>>> dht.humidity()
```

Display the temperature and humidity on the Nokia 5110 display, updated every 4 seconds:

```
>>> import am2320_nokia
```

## Credits

* Markus Birth's [wipy Nokia 5110 library](https://github.com/mbirth/wipy-upcd8544) (MIT license) with [my ESP8266 modifications](https://github.com/mbirth/wipy-upcd8544/issues/1).

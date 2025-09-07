# epaper10in2.py to drive a 10.2 inch e-paper display

'''
DC pin changed from 32 to 15
BUSY pin changed from 34 to 27
'''
from machine import Pin, SPI
from epaper10in2 import EPD
# from epaper2in1 import EPD

sck = Pin(18)
miso = Pin(19)
mosi = Pin(23)
dc = Pin(15)
cs = Pin(26)
rst = Pin(25)
busy = Pin(27)
spi = SPI(2, baudrate=4000000, polarity=0, phase=0, sck=sck, miso=miso, mosi=mosi)

e = EPD(spi, cs, dc, rst, busy)
init_ok = e.init()
print(f"{init_ok=}")
e._command(0x12, b'\x00')
# e.clear()

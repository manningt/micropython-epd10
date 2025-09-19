"""
MicroPython Waveshare 10.2" Black/White/Yellow/red  e-paper display driver
https://github.com/mcauser/micropython-waveshare-epaper

MIT License

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
"""

from micropython import const
from time import sleep_ms
import ustruct

# Display resolution
EPD_WIDTH  = const(960)
EPD_HEIGHT = const(640)

# Display commands
PANEL_SETTING                  = const(0x00)
POWER_SETTING                  = const(0x01)
POWER_OFF                      = const(0x02)
#POWER_OFF_SEQUENCE_SETTING     = const(0x03)
POWER_ON                       = const(0x04)
#POWER_ON_MEASURE               = const(0x05)
BOOSTER_SOFT_START             = const(0x06)
DEEP_SLEEP                     = const(0x07)
DATA_START_TRANSMISSION_1      = const(0x10)
#DATA_STOP                      = const(0x11)
DISPLAY_REFRESH                = const(0x12)
#IMAGE_PROCESS                  = const(0x13)
#LUT_FOR_VCOM                   = const(0x20)
#LUT_BLUE                       = const(0x21)
#LUT_WHITE                      = const(0x22)
#LUT_GRAY_1                     = const(0x23)
#LUT_GRAY_2                     = const(0x24)
#LUT_RED_0                      = const(0x25)
#LUT_RED_1                      = const(0x26)
#LUT_RED_2                      = const(0x27)
#LUT_RED_3                      = const(0x28)
#LUT_XON                        = const(0x29)
PLL_CONTROL                    = const(0x30)
#TEMPERATURE_SENSOR_COMMAND     = const(0x40)
TEMPERATURE_CALIBRATION        = const(0x41)
#TEMPERATURE_SENSOR_WRITE       = const(0x42)
#TEMPERATURE_SENSOR_READ        = const(0x43)
VCOM_AND_DATA_INTERVAL_SETTING = const(0x50)
#LOW_POWER_DETECTION            = const(0x51)
TCON_SETTING                   = const(0x60) # Timing Control
TCON_RESOLUTION                = const(0x61)
SPI_FLASH_CONTROL              = const(0x65)
#REVISION                       = const(0x70)
#GET_STATUS                     = const(0x71)
#AUTO_MEASUREMENT_VCOM          = const(0x80)
#READ_VCOM_VALUE                = const(0x81)
VCM_DC_SETTING                 = const(0x82)
FLASH_MODE                     = const(0xE5)

BUSY = const(0)  # 0=busy, 1=idle

class EPD:
    def __init__(self, spi, cs, dc, rst, busy):
        self.spi = spi
        self.cs = cs
        self.dc = dc
        self.rst = rst
        self.busy = busy
        self.cs.init(self.cs.OUT, value=1)
        self.dc.init(self.dc.OUT, value=0)
        self.rst.init(self.rst.OUT, value=0)
        self.busy.init(self.busy.IN)
        self.width = EPD_WIDTH
        self.height = EPD_HEIGHT

    def _command(self, command, data=None):
        self.dc(0)
        self.cs(0)
        self.spi.write(bytearray([command]))
        self.cs(1)
        if data is not None:
            self._data(data)

    def _data(self, data):
        self.dc(1)
        self.cs(0)
        self.spi.write(data)
        self.cs(1)

    def init(self):
        print('EPD init: starting')
        self.reset()

        self._command(PANEL_SETTING, b'\x0F\x29') #x00
        self._command(BOOSTER_SOFT_START, b'\x0F\x8B\x93\xC1') #x06
        self._command(TEMPERATURE_CALIBRATION, b'\x00') #x41
        self._command(VCOM_AND_DATA_INTERVAL_SETTING, b'\x37') #0x50
        self._command(TCON_SETTING, b'\x02\x02') #0x60
        self._command(TCON_RESOLUTION, ustruct.pack(">HH", EPD_WIDTH, EPD_HEIGHT)) #0x61  
        # https://docs.micropython.org/en/latest/library/struct.html  big-endian, unsigned short
        # self._command(TCON_RESOLUTION, b'\x03\xC0\x02\x80') #0x61  width/256, width%256, height/256, height%256
        self._command(0x62, b'\x98\x98\x98\x75\xCA\xB2\x98\x7E') # LUT for VCOM ????
        self._command(SPI_FLASH_CONTROL, b'\x00\x00\x00\x00') #x65
        self._command(0xE7, b'\x1C') # LUT for red ?
        self._command(0xE3, b'\x00') # LUT for red ?
        self._command(0xE9, b'\x01') # LUT for red ?
        self._command(PLL_CONTROL, b'\x08') #x30
        self._command(POWER_ON) #0x04
        count = self.wait_until_idle()
        print(f'EPD init: wait_until_idle returned after count={count}') 
        if count > 200:
            print('wait_until_idle timed out after init')
            return False
        else:
            return True
        '''
        self._command(POWER_SETTING, b'\x37\x00') #x01
        self._command(PANEL_SETTING, b'\xCF\x08') #x00
        self.wait_until_idle()
        self._command(VCM_DC_SETTING, b'\x1E') #0x82 decide by LUT file
        self._command(FLASH_MODE, b'\x03') #0xE5
        '''

    def wait_until_idle(self):
        count = 0
        while self.busy.value() == BUSY:
            sleep_ms(10)
            count += 1
            if count > 2000:
                break
        return count
        
    def reset(self):
        self.rst(0)
        sleep_ms(200)
        self.rst(1)
        sleep_ms(200)

    def display(self, buf):
        self._command(DATA_START_TRANSMISSION_1)
        self._data(buf)
        self._command(DISPLAY_REFRESH)

    def sleep(self):
        self._command(POWER_OFF)
        self.wait_until_idle()
        self._command(DEEP_SLEEP, b'\xA5')

    def clear(self, color=0x55):
        # x00 black; 0xFF red;  0xAA yellow; 0x55 white
        if self.width % 4 == 0 :
            Width = self.width // 4
        else :
            Width = self.width // 4 + 1
        # Width = 960 // 4 = 240
        fill = bytearray([color] * Width)
        self._command(DATA_START_TRANSMISSION_1)
        for j in range(0, self.height):
            self._data(fill)
        self._command(DISPLAY_REFRESH)

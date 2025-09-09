import network, time
from ftplib import FTP
import machine
import ujson as json
import tinypico
from epaper10in2 import EPD

def setup_station(ssid, password):
   sta_if = network.WLAN(network.STA_IF)
   sta_if.active(True)
   sta_if.connect(ssid, password)
   return sta_if

def setup_ftp(host, user, password):
   try:
      ftp = FTP(host)
   except Exception as e:
      print(f"FTP connection error: {e}")
      return None
   try:
      ftp.login(user,password)
   except Exception as e:
      print(f"FTP login error: {e}")
      return None
   ftp.set_pasv(False)
   return ftp

def get_image_number(ftp):
   rc = None
   for i in range(1, 5):
      try:
         ftp.cwd(str(i))
         rc = i
         break
      except Exception as e:
         print(f"{i}: {e}")
   #restore cwd
   if rc is not None:
      ftp.cwd('..')
   return rc

def my_deep_sleep(seconds):
   print(f"deep sleep for {seconds} seconds")
   machine.deepsleep(seconds * 1000)

def read_config(filename="config.json"):
   config = None
   try:
      with open(filename, 'r') as f:
         config = json.load(f)
   except Exception as e:
      print(f"Error loading {filename}: {e}")
   return config

def restore_state():
   tmp = None
   try:
      tmp = json.loads(rtc.memory().decode)
      print(f"RTC.memory={tmp}")
      if type(tmp) is not dict:
            print(f"Warning (restore_state): RTC.memory={tmp} is not a dictionary")
            tmp = None
   except:
      print(f"Warning (restore_state): RTC.memory={tmp} was not JSON")
   return tmp


def main():
   tinypico.set_dotstar_power(False)
   rtc = machine.RTC()
   sck = machine.Pin(18)
   miso = machine.Pin(19)
   mosi = machine.Pin(23)
   dc = machine.Pin(15)
   cs = machine.Pin(26)
   rst = machine.Pin(25)
   busy = machine.Pin(27)

   config = read_config()
   if config is None:
      print("No config, sleeping 300 seconds")
      my_deep_sleep(15)

   setup_station(config['ssid'], config['password'])
   time.sleep_ms(3000)

   ftp = setup_ftp(config['ftp_host'], config['ftp_user'], config['ftp_password'])
   if ftp is None:
      print(f"FTP setup to {config['ftp_host']} failed")
      my_deep_sleep(config['sleep'])
   try:
      ftp.cwd('epaper')
   except Exception as e:
      print(f"{e} on cwd to epaper")
      my_deep_sleep(config['sleep'])

   server_image_number = get_image_number(ftp)
   ftp.quit()

   restored_state = restore_state()
   if restored_state is not None and 'img_num' in restored_state:
      restored_image_number = restored_state['img_num']
   else:
      restored_image_number = None

   if restored_image_number == server_image_number:
      print(f"{restored_image_number=} matches {server_image_number=}: not updating display")
      my_deep_sleep(config['sleep'])
   else:
      print(f"changing display from {restored_image_number=} to {server_image_number=}")
      rtc.memory(bytearray(json.dumps({"img_num": server_image_number}).encode()))

      # spi = machine.SPI(2, baudrate=4000000, polarity=0, phase=0, sck=sck, miso=miso, mosi=mosi)
      # e = EPD(spi, cs, dc, rst, busy)
      # if not e.init():
      #    print("e-paper init failed")
      # with open("open-welcome.bin", 'rb') as file:
      #    byte_array = bytearray(file.read())
      # e.display(byte_array)


   if 0:
      state = {"img_num": 3}
      rtc.memory(bytearray(json.dumps(state).encode())) # store state as JSON in RTC memory
      restored_image_number = json.loads(rtc.memory().decode())


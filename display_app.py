import network, time
from ftplib import FTP
import machine
import ujson as json
import tinypico

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


def main():
   tinypico.set_dotstar_power(False)

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

   image_number = get_image_number(ftp)
   ftp.quit()
   if image_number is None:
      print(f"Getting the image number failed")
      my_deep_sleep(config['sleep'])
   print(f"image_number={image_number}")


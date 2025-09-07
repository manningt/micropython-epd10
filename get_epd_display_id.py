
import network, time
sta_if = network.WLAN(network.STA_IF)
sta_if.active(True)
sta_if.connect('BayberryLedge', '40Edgemoor')
from ftplib import FTP
time.sleep_ms(1000)
ftp = FTP('10.0.1.67')
ftp.login('pi','readysetcrash')
ftp.set_pasv(False)
try:
   ftp.cwd('epaper')
except Exception as e:
   print(f"{e} to epaper")

def get_epd_display_id():
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

# Overview
The objective is to have an e-paper display on the visitor's entrance that be changed by being either locally connected or remotely connected.  Example use-cases can be illustrated by what is on the display, e.g.
- Open: Tours on the hour from noon to 3.
- Open: A tour is in progress.  Please return at N PM for the next tour.
- Closed: The Museum is open Fri, Sat, Sun with tours on the hour from noon to 3
- Closed: Sorry for the inconvenience, our tour guide is not avaiable.

For example, if the tour guide is not available, then a parameter on the Museum's server can be modified to change the message to the last one.  If the staff is a tour guide only (no greeter to talk to incoming visitors), then message 2 can be selected by the tour guide while she is at the Museum.
The display will be battery powered since it will be mounted to the screen door.  During the off-season, the display will be removed and stored.

In order to be battery powered, the device (ESP32) which writes the e-paper display will sleep most the time; it will wake at intervals to determine whether the displayed should be changed.  However, being able to change the message at anytime is required in order to be user-friendly.  So a server (a Raspberry Pi) will serve a web-page to that will allow someone at the Museum to select the message to dislay.

The display can be changed remotely by using Tailscale to change a parameter on the server.

To save inventing a networking protocol between the ESP and the linux server, FTP can be used. It is simpler to not do a data transfer and only use the command channel. FTP has a 'change working directory' command (cwd) that can be used to detect if a directory exists, or not.  The ESP can use cwd to detect which directory exists - cwd returns a failure code if it does not exist.  So on the server, a directory named epaper is created, and a single directory with a name between 1 and N is created.  The ESP tries to cwd to directories 1 though N, and uses the first directory that cwd returns success.  Note that the FTP command 'dir' (or ls) requires using the data cchannel.

## ESP firmware
Because the ESP32 can be battery powered when using long intervals of DEEP_SLEEP, it was selected to drive the e-paper display.
Upon waking up from deep sleep, main.py would:
- turn on Wifi and connect to the SHM wifi network
- use FTP to determine which e-paper file to display by checking which directory exists.  The FTP client software is at https://github.com/SpotlightKid/micropython-ftplib/blob/master/ftplib.py
- 

# server software
Install FTP server software as per these instructions: https://www.geeksforgeeks.org/linux-unix/setup-and-configure-an-ftp-server-in-linux/
- the config variables for an FTP user and passive mode do not have to be configured
- make sure other ports are enabled: sudo ufw allow 5000:10000/tcp

# Hardware


# useful links:
 - https://github.com/mcauser/micropython-waveshare-epaper
 - 10.2inch display:
   - https://www.waveshare.com/product/displays/e-paper/epaper-1/10.2inch-e-paper-hat-g.htm?___SID=U
   - https://www.waveshare.com/wiki/10.2inch_e-Paper_HAT_(G)
   - https://www.waveshare.com/wiki/E-Paper_Driver_HAT#Questions_about_Hardware
 - https://docs.micropython.org/en/latest/reference/repl.html
 - https://github.com/dhylands/rshell
 - Tinypico:
   - https://www.tinypico.com/code-examples
   - https://help.unexpectedmaker.com/index.php/knowledge-base/what-voltage-range-can-the-5v-pin-accept-and-is-it-an-input-and-output/

 - adafruit breakout Friend:
   - https://www.adafruit.com/product/4224
- 2.13inch display:
   - https://seengreat.com/product/190/2-13inch-e-paper-display
   - https://github.com/seengreat/2.13inch-E-Paper-Display-V2/blob/main/Raspberry-Pi_2.13_V2/python/epd_2inch13.py
- other ESP32 modules:
   - https://detailspin.com/wp-content/images/zkw-esp32-wroom-pinout-arduino.jpg



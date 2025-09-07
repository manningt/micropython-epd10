# Overview
The objective is to have an e-paper display on the visitor's entrance that be changed by being either locally connected or remotely connected.  Example use-cases can be illustrated by what is on the display, e.g.
- Open: Tours on the hour from noon to 3.
- Open: A tour is in progress.  Please return at N PM for the next tour.
- Closed: The Museum is open Fri, Sat, Sun with tours on the hour from noon to 3
- Closed: Sorry for the inconvenience, our tour guide is not avaiable.

For example, if the tour guide is not available, then a parameter on the Museum's server can be modified to change the message to the last one.  If the staff is a tour guide only, then message 2 can be selected by the tour guide while she is at the Museum.
The display will be battery powered since it will be mounted to the screen door.  During the off-season, the display will be removed and stored.

In order to be battery powered, the device (ESP32) which writes the e-paper display will sleep most the time; it will wake at intervals to determine whether the displayed should be changed.  However, being able to change the message at anytime is required in order to be user-friendly.  So a server (a Raspberry Pi) will serve a web-page to that will allow someone at the Museum to select the message to dislay.

## ESP firmware
Because the ESP32 can be battery powered when using long intervals of DEEP_SLEEP, it was selected to drive the e-paper display.
Upon waking up from deep sleep, main.py would:
- turn on Wifi and connect to the SHM wifi network
- use FTP to determine which e-paper file to display
   - https://github.com/SpotlightKid/micropython-ftplib/blob/master/ftplib.py
   - passive mode is more complex (opens another port), so just using 'cwd' to determine what directory is present
-

# server software
Install FTP server software as per these instructions: https://github.com/SpotlightKid/micropython-ftplib/blob/master/ftplib.py
- the config variables for an FTP user and passive mode do not have to be configured
- 
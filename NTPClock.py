###############################################################################
#
# NTPClock.py
#
# This is a micropython program that allows a Raspberry Pi Pico W and MAX7219
# 7-segment display to be used as a clock which syncs with an NTP server.
#
# Thanks to Paul Dwerryhouse, who wrote the max7219_8digit library, to Roberto
# Bellingeri, who wrote the localPTZtime library, and to Andy Lawton AJ9L,
# whose program I stole from shamelessly, and who supplied some of the hardware
# for my very intimidating-looking clock.
#
# To use, set Brightness as you prefer, choose an NTP host, copy a valid POSIX
# timezone into the program (EST is not a valid POSIX timezone; you'll need to
# Google yours up!) and add your WiFi credentials.
#
# Copyright (c)2025 Chris Reitz, N9CVR
#
# This program is released under the GNU GPL v3.
#
# This program is free software: you can redistribute it and/or modify it
# under the terms of the GNU General Public License as published by the Free
# Software Foundation, either version 3 of the License, or (at your option)
# any later version.
#
# This program is distributed in the hope that it will be useful, but WITHOUT
# ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS
# FOR A PARTICULAR PURPOSE. See the GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License along with
# this program. If not, see <https://www.gnu.org/licenses/>. 
#
###############################################################################

import network
import time
import math
import ntptime
import socket
import localPTZtime
from machine import Pin, SPI
import max7219_8digit

###
#
# User Inputs
#
###
brightness = 15 # integer, 0-15. 0 = off; 15 = max bright
ntptime.host = '1.2.3.4' # IP address or domain. If in doubt, use pool.ntp.org
TZ = "CST6CDT,M3.2.0/2:00:00,M11.1.0/2:00:00" # Chicago POSIX timezone
wlanSSID = "stealme" # Your SSID
wlanPW = "asdf1234" # Your password

###
#
# Initialize display
#
###
spi = SPI(0, baudrate=100000, polarity=1, phase=0, sck=Pin(2), mosi=Pin(3))
ss = Pin(5, Pin.OUT)
intensity_register=0x0a
display = max7219_8digit.Display(spi, ss)
display.set_register(intensity_register,brightness)

###
#
# Connect to WiFi
#
###
wlanMaxWait = 10
wlan = network.WLAN(network.STA_IF)
print('Connect to WiFi')
wlan.active(True)
wlan.connect(wlanSSID, wlanPW)
for i in range(wlanMaxWait):
    if wlan.status() < 0 or wlan.status() >= 3:
        break
    display.write_to_buffer('init')
    display.display()
    time.sleep(1)
    
if wlan.isconnected():
    print('WiFi Connected. IP: ', wlan.ifconfig()[0],' Subnet: ',wlan.ifconfig()[1],' Gateway: ',wlan.ifconfig()[2],' DNS: ',wlan.ifconfig()[3])
else:
    print('No WiFi Connection')
    print('WiFi Status:', wlan.status())
    display.write_to_buffer('WIFI Fail')
    display.display()

###
#
# Set time from NTP
#
###
def set_time():
    delta = abs(ntptime.time() - time.time())
    if delta > 0:
        print("At",("{:02d}:{:02d}:{:02d},".format(time.localtime()[3],time.localtime()[4],time.localtime()[5])),"time was off by",delta,"seconds. Syncing.")
        ntptime.settime()
        print("Time is now",("{:02d}:{:02d}:{:02d} UTC.".format(time.localtime()[3],time.localtime()[4],time.localtime()[5])))

set_time()

###
#
# Print the current UTC time
#
###
UTC_display_string = ("{:02d}:{:02d}:{:02d} UTC.".format(time.localtime()[3], time.localtime()[4], time.localtime()[5]))
print(UTC_display_string)

###
#
# Convert UTC Time to local time
#
###
localtime = localPTZtime.tztime(time.time(), TZ)
print("Local time is {:02d}:{:02d}:{:02d}".format(localtime[3], localtime[4], localtime[5]))

###
#
# Do the clock thing and display the time
#
###
one_shot = 0 # Used to set time only once.
while (True):
    localtime = localPTZtime.tztime(time.time(), TZ)
    if localtime[4] == 0 and localtime[5] == 0 and one_shot == 0:
        set_time()
        one_shot = 1
        print("It's {:02d}:{:02d}:{:02d}".format(localtime[3], localtime[4], localtime[5]))
    elif localtime[4] == 0 and localtime[5] == 1:
        one_shot = 0
    else:
        if localtime[5] % 2 ==0:
            display_string = ("{:02d}.{:02d}.{:02d}".format(localtime[3], localtime[4], localtime[5]))
        else:
            display_string = ("{:02d} {:02d} {:02d}".format(localtime[3], localtime[4], localtime[5]))
        display.write_to_buffer(display_string)
        display.display()
        



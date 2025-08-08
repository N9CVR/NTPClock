This is a micropython program that allows a Raspberry Pi Pico W and MAX7219
7-segment display to be used as a clock which syncs with an NTP server.

Thanks to Paul Dwerryhouse, who wrote the max7219_8digit library, to Roberto
Bellingeri, who wrote the localPTZtime library, and to Andy Lawton AJ9L,
whose program I stole from shamelessly, and who supplied some of the hardware
for my very intimidating-looking clock.

In order for this program to work, you will need to download the following
libraries:

MAX7219_8digit from https://github.com/pdwerryhouse/max7219_8digit
localPTZtime from https://github.com/bellingeri/localPTZtime

To use the program, set Brightness as you prefer, choose an NTP host, copy a
valid POSIX timezone into the program (EST is not a valid POSIX timezone; 
you'll need to Google yours up!) and add your WiFi credentials.

Copyright (c)2025 Chris Reitz, N9CVR

This program is released under the GNU GPL v3.

This program is free software: you can redistribute it and/or modify it
under the terms of the GNU General Public License as published by the Free
Software Foundation, either version 3 of the License, or (at your option)
any later version.

This program is distributed in the hope that it will be useful, but WITHOUT
ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS
FOR A PARTICULAR PURPOSE. See the GNU General Public License for more details.

You should have received a copy of the GNU General Public License along with
this program. If not, see <https://www.gnu.org/licenses/>. 

Roadmap:

v1.0 - Initial release (8/9/2025)

v2.0 - improve calls to NTP server. I'd like to detect how long the clock has
  been accurate, and only call the NTP server when we're starting to lose
  accuracy.

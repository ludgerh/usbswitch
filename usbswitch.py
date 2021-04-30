# Copyright (C) 2021 Ludger Hellerhoff, ludger@booker-hellerhoff.de
# This program is free software; you can redistribute it and/or
# modify it under the terms of the GNU General Public License
# as published by the Free Software Foundation; either version 3
# of the License, or (at your option) any later version.
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  
# See the GNU General Public License for more details.
# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software
# Foundation, Inc., 59 Temple Place - Suite 330, Boston, MA  02111-1307, USA.

from argparse import ArgumentParser
from sys import argv, exit
from usb.util import get_string
from usbaccess import devicelist, type_string
from time import sleep

version_string = '0.1.0'

print('Program Version', argv[0], version_string)


parser = ArgumentParser("USB Switcher")
parser.add_argument("-n", "--number", dest="snumber", type=int, default=None,
  help='Serial number of the device, default: first found device')
parser.add_argument("-a", "--action", dest="action", type=int,
  help='0 is off, 1 is on')
parser.add_argument("-d", "--debug", dest="debug", action="store_true",
  help='Show additional information')
parser.add_argument("-l", "--ledonly", dest="ledonly", action="store_true",
  help='Just changing the light, no switching')
parser.add_argument("-r", "--relaisonly", dest="relaisonly", action="store_true",
  help='No LED change')
parser.add_argument("-i", "--reset", dest="reset", action="store_true",
  help='Reset the device before switching')
parser.add_argument("-s", "--secure", dest="secure", action="store_true",
  help='Check after switching')
args = parser.parse_args()

dlist = devicelist(0x0d50, 0x0008, args.ledonly, args.relaisonly, args.reset)

if args.debug:
  print('Found', len(dlist.devices), 'devices')
count = 0
for dev in dlist.devices:
  if args.debug:
    print('Device #'+str(count)
      +':  Type='+type_string(dev.idProduct)
      +':  Version='+str(dev.bcdDevice)
      +':  SNumber='+str(int(get_string(dev, dev.iSerialNumber), 16))
    )
    count += 1

if args.snumber:
  devindex = dlist.get_index_from_serial(args.snumber)
  if devindex is None:
    print('No device with serial number', args.snumber)
    exit()

if args.debug:
  print('Old switch setting:', dlist.get_switch())

if args.action == 1:
  dlist.set_switch(True)
elif args.action == 0:
  dlist.set_switch(False)
else:
  print(args.action, 'is no possible action')
  exit()
if args.secure:
  if dlist.wait_for(args.action==1):
    print('Done...')
  else:
    print('Timeout...')
    

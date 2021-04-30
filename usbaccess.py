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

from usb.core import find, USBError
from usb.util import get_string
from time import sleep, time


def type_string(nr):
  if nr == 0x08:
    return('SWITCH1_DEVICE')
  else:
    return('UNKNOWN')

class devicelist:
  def __init__(self, vi, pi, ledonly, relaisonly, reset):
    self.ledonly = ledonly
    self.relaisonly = relaisonly
    self.index = 0
    self.devices = []
    devicesraw = find(idVendor=vi, idProduct=pi, find_all=True)
    for dev in devicesraw:
      dev.id = len(self.devices)
      self.devices.append(dev)
    for dev in self.devices:
      if dev:
        ep=dev[0].interfaces()[0].endpoints()[0]
        intf=dev[0].interfaces()[0].bInterfaceNumber
        if dev.is_kernel_driver_active(intf):
          try:
            dev.detach_kernel_driver(intf)
          except USBError as e:
            sys.exit('Could not detatch kernel driver:'+str(e))
        try:
          dev.set_configuration()
          if reset:
            dev.reset()
        except USBError as e:
          sys.exit('Could not set configuration:'+str(e))
        dev.eaddr=ep.bEndpointAddress
        while True:
          result = self.bulk_transfer_from_device(6)
          if result[0] == 0:
            sleep(0.1)
          else:
            break
        self.old_state = result
      else:
        print ('No device connected')

  def bulk_transfer_from_device(self, count):
    return(self.devices[self.index].read(self.devices[self.index].eaddr, count))

  def control_sequence_out(self, data):
    cvalue = self.devices[self.index][0].bConfigurationValue #maybe 0x200 is better ?
    return(self.devices[self.index].ctrl_transfer(0x22, 0x09, cvalue, 0x0, data))

  def get_index_from_serial(self, serial):
    for dev in self.devices:
      if serial == int(get_string(dev, dev.iSerialNumber), 16):
        self.index = dev.id
        return(self.index)
    return(None) 

  def get_switch(self):
    result = (self.old_state[0] & 1) == 1
    return(result)

  def wait_for(self, status):
    sleep(0.1)
    ts = time()
    while True:
      result = self.bulk_transfer_from_device(6)
      if ((result[0] & 1) == 1) == status:
        break
      else:
        if (time() - ts) > 5:
          return(False)
        else:
          sleep(0.01)
    return(True)

  def set_switch(self, value): 
    if not self.ledonly:
      data = [0x0] * 3
      data[1] = 16
      if value:
        data[2] = 1
      self.control_sequence_out(data)
    if not self.relaisonly:
      data = [0x0] * 3
      if not value:
        data[2] = 15
      self.control_sequence_out(data)
      data = [0x0] * 3
      data[1] = 1
      if value:
        data[2] = 15
      self.control_sequence_out(data)
    return(0)


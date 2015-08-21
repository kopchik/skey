#!/usr/bin/env python3
from usb.util import CTRL_IN, CTRL_OUT, CTRL_TYPE_CLASS, CTRL_RECIPIENT_INTERFACE, CTRL_RECIPIENT_DEVICE
import usb
import sys
import time

# USB stuff
report_id  = 0x01
set_report = 0x09
get_report = 0x01

req_recv = usb.util.build_request_type(CTRL_IN,  CTRL_TYPE_CLASS, CTRL_RECIPIENT_DEVICE)
req_send = usb.util.build_request_type(CTRL_OUT, CTRL_TYPE_CLASS, CTRL_RECIPIENT_DEVICE)


class DigiConsole:
  def __init__(self):
    self.reattach = False
    reported = False
    while True:
      self.dev = usb.core.find(idVendor=0x16c0, idProduct=0x05df)
      if self.dev:
        break
      if not reported:
        print("waiting for the device", end="")
        reported = True
      print(".", end="")
      sys.stdout.flush()
      time.sleep(1)

    if self.dev.is_kernel_driver_active(0):
      self.reattach = True
      self.dev.detach_kernel_driver(0)
    self.dev.set_configuration()

  def readln(self):
    result = ""
    while True:
      buf = self.dev.ctrl_transfer(req_recv, get_report, (3 << 8) | report_id, 0, 1)
      if not buf:
        print("empty buf")
        time.sleep(0.05)
      result += buf.tostring().decode(errors='ignore')
      if result.endswith('\n'):
        break
    return result[:-1]


  def writeln(self, s):
    assert isinstance(s, str)
    if not s.endswith('\n'):
      s = s + '\n'
    wValue = (3 << 8) | report_id
    for b in s.encode():
      res = self.dev.ctrl_transfer(req_send, set_report, wValue, b, [])


  def disconnect(self):
    usb.util.dispose_resources(self.dev)  # prevent attach_kernel_driver from "Resource busy"
    if self.reattach:
      self.dev.attach_kernel_driver(0)  # may raise USBError if there's e.g. no kernel driver loaded at all


if __name__ == '__main__':
  con = DigiConsole()
  from random import choice
  from string import ascii_uppercase, digits
  for x in range(10):
    s = ''.join(choice(ascii_uppercase + digits) for _ in range(8))
    con.writeln(s)
    time.sleep(0.02);
    ret = con.readln()
    print("result", ret, s == ret);
  con.disconnect()

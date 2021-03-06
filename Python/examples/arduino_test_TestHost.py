#!/usr/bin/python

#
# This is a test harness for the device defined in Arduino/libraries/IOToy/examples/TestHost.ino
# If that device is plugged in, and shows up as ttyUSB2, on a device that supports 19200 baud
# then this code can and will introspect that device and perform a live test of the device.
#

import os
import sys
import time

from iotoy.deviceproxy import serial_io, DeviceProxy

io = serial_io("/dev/ttyUSB2", 19200, debug=False)
for i in "wait":
    sys.stdout.write(".")
    sys.stdout.flush()
    time.sleep(1)
sys.stdout.write("\n")
sys.stdout.flush()

p = DeviceProxy(device=io)
p.introspect_device()

if p.devinfo()["devicename"] != 'testhosttiny':
    print "This test harness only tests devices that are of type testhosttiny"
    sys.exit(0)

print p

print

print "p.drive_forward_time_ms", repr(p.drive_forward_time_ms)
p.drive_forward_time_ms = 1000
print "p.drive_forward_time_ms", repr(p.drive_forward_time_ms)
assert p.drive_forward_time_ms == 1000


print

print "p.turn_time_ms", repr(p.turn_time_ms)
p.turn_time_ms = 500
print "p.turn_time_ms", repr(p.turn_time_ms)

assert p.turn_time_ms == 500

try:
    p.turn_time_ms = True
except ValueError as e:
    assert e.message == "turn_time_ms is an int, but you provided True which is 'bool'"
    print "Successfully caught attempt to put a bool into an int"

try:
    p.turn_time_ms = 1.1
except ValueError as e:
    if e.message != "turn_time_ms is an int, but you provided 1.1 which is 'float'":
        raise e
    print "Successfully caught attempt to put a float into an int"

try:
    p.turn_time_ms = 'hello'
except ValueError as e:
    if e.message != "turn_time_ms is an int, but you provided 'hello' which is 'str'":
        raise e
    print "Successfully caught attempt to put a str into an int"


print p.barecommand
p.barecommand()

p.one_arg_int
p.one_arg_int(1)

try:
    p.one_arg_int(1.1)
except ValueError as e:
    if e.message != "Should be int, recieved float":
       raise
    print "Successfully caught bad argument:", e

try:
    p.one_arg_int("hello")
except ValueError as e:
    if e.message != "Should be int, recieved str":
       raise
    print "Successfully caught bad argument:", e

try:
    p.one_arg_int(True)
except ValueError as e:
    if e.message != "Should be int, recieved bool":
       raise
    print "Successfully caught bad argument:", e

p.one_arg_str("hello")
try:
    p.one_arg_str(1)
except ValueError as e:
    if e.message != "Should be str, recieved int":
       raise
    print "Successfully caught bad argument:", e

try:
    print p.one_arg_str(1.1)
except ValueError as e:
    if e.message != "Should be str, recieved float":
       raise
    print "Successfully caught bad argument:", e

try:
    p.one_arg_str(True)
except ValueError as e:
    if e.message != "Should be str, recieved bool":
       raise
    print "Successfully caught bad argument:", e

p.one_arg_float(1.1)
try:
    p.one_arg_float(1)
except ValueError as e:
    if e.message != "Should be float, recieved int":
       raise
    print "Successfully caught bad argument:", e

try:
    p.one_arg_float("hello")
except ValueError as e:
    if e.message != "Should be float, recieved str":
       raise
    print "Successfully caught bad argument:", e

try:
    p.one_arg_float(True)
except ValueError as e:
    if e.message != "Should be float, recieved bool":
       raise
    print "Successfully caught bad argument:", e

print p.no_arg_result_int()
print p.no_arg_result_bool()
print p.no_arg_result_str()
print p.no_arg_result_float()
print p.no_arg_result_T()

print p.ratio



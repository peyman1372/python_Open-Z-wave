#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""

This file is part of **python-openzwave** project http://code.google.com/p/python-openzwave.
    :platform: Unix, Windows, MacOS X
    :sinopsis: openzwave wrapper

.. moduleauthor:: bibi21000 aka Sébastien GALLET <bibi21000@gmail.com>

License : GPL(v3)

**python-openzwave** is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

**python-openzwave** is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
GNU General Public License for more details.
You should have received a copy of the GNU General Public License
along with python-openzwave. If not, see http://www.gnu.org/licenses.

"""
import sys, os
import time
try :
    import libopenzwave
    from libopenzwave import PyManager
    print("Openzwave is installed.")
except :
    print("Openzwave is not installed. Get it from tmp directory.")
    sys.path.insert(0, os.path.abspath('../build/tmp/usr/local/lib/python2.6/dist-packages'))
    sys.path.insert(0, os.path.abspath('../build/tmp/usr/local/lib/python2.7/dist-packages'))
    sys.path.insert(0, os.path.abspath('build/tmp/usr/local/lib/python2.6/dist-packages'))
    sys.path.insert(0, os.path.abspath('build/tmp/usr/local/lib/python2.7/dist-packages'))
    import libopenzwave
    from libopenzwave import PyManager

device="/dev/zwave-aeon-s2"
log="Info"
sniff=60.0

for arg in sys.argv:
    if arg.startswith("--device"):
        temp,device = arg.split("=")
    elif arg.startswith("--log"):
        temp,log = arg.split("=")
    elif arg.startswith("--sniff"):
        temp,sniff = arg.split("=")
        sniff = float(sniff)
    if arg.startswith("--help"):
        print("help : ")
        print("  --device=/dev/yourdevice ")
        print("  --log=Info|Debug")
        print("  --sniff=0 : sniff for zwave messages a number of seconds")
        exit(0)

options = libopenzwave.PyOptions()

# Specify the open-zwave config path here
options.create("../openzwave/config/","","--logging true")
options.lock()
manager = libopenzwave.PyManager()
manager.create()

# callback order: (notificationtype, homeid, nodeid, ValueID, groupidx, event)
def callback(args):
    print('\n%s\n[%s]:\n' % ('-'*20, args['notificationType']))
    if args:
        print('homeId: 0x%.8x' % args['homeId'])
        print('nodeId: %d' % args['nodeId'])
        v = args['valueId']
        print('valueID: %s' % v['id'])
        if v.has_key('groupIndex') and v['groupIndex'] != 0xff: print('GroupIndex: %d' % v['groupIndex'])
        if v.has_key('event') and v['event'] != 0xff: print('Event: %d' % v['event'])
        if v.has_key('value'): print('Value: %s' % str(v['value']))
        if v.has_key('label'): print('Label: %s' % v['label'])
        if v.has_key('units'): print('Units: %s' % v['units'])
        if v.has_key('readOnly'): print('ReadOnly: %s' % v['readOnly'])
    print('%s\n' % ('-'*20,))

print("Add watcher")
manager.addWatcher(callback)
print("Add device")
manager.addDriver(device)
print("Sniff network during %s seconds" % sniff)
time.sleep(sniff)
print("Remove watcher")
manager.removeWatcher(callback)
print("Remove device")
manager.removeDriver(device)

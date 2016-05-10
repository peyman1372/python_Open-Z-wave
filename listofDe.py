#!/usr/bin/env python
# -*- coding: utf-8 -*-

import logging
import sys, os

# logging.getLogger('openzwave').addHandler(logging.NullHandler())
# logging.basicConfig(level=logging.DEBUG)
logging.basicConfig(level=logging.INFO)

logger = logging.getLogger('openzwave')

try:
    import openzwave
    from openzwave.node import ZWaveNode
    from openzwave.value import ZWaveValue
    from openzwave.scene import ZWaveScene
    from openzwave.controller import ZWaveController
    from openzwave.network import ZWaveNetwork
    from openzwave.option import ZWaveOption

    print("Openzwave is installed.")
except:
    print("Openzwave is not installed. Get it from tmp directory.")
    sys.path.insert(0, os.path.abspath('../build/tmp/usr/local/lib/python2.6/dist-packages'))
    sys.path.insert(0, os.path.abspath('../build/tmp/usr/local/lib/python2.7/dist-packages'))
    sys.path.insert(0, os.path.abspath('build/tmp/usr/local/lib/python2.6/dist-packages'))
    sys.path.insert(0, os.path.abspath('build/tmp/usr/local/lib/python2.7/dist-packages'))
    import openzwave
    from openzwave.node import ZWaveNode
    from openzwave.value import ZWaveValue
    from openzwave.scene import ZWaveScene
    from openzwave.controller import ZWaveController
    from openzwave.network import ZWaveNetwork
    from openzwave.option import ZWaveOption
import time
from louie import dispatcher, All

device = "/dev/ttyACM0"
log = "None"
sniff = 300.0

for arg in sys.argv:
    if arg.startswith("--device"):
        temp, device = arg.split("=")
    elif arg.startswith("--log"):
        temp, log = arg.split("=")
    elif arg.startswith("--sniff"):
        temp, sniff = arg.split("=")
        sniff = float(sniff)
    elif arg.startswith("--help"):
        print("help : ")
        print("  --device=/dev/yourdevice ")
        print("  --log=Info|Debug")

#Define some manager options
options = ZWaveOption(device, \
                      config_path="../openzwave/config", \
                      user_path=".", cmd_line="")
options.set_log_file("OZW_Log.log")
options.set_append_log_file(False)
options.set_console_output(False)
options.set_save_log_level('Debug')
options.set_logging(True)
options.lock()


def louie_network_started(network):
    print("Hello from network : I'm started : homeid %0.8x - %d nodes were found." % \
          (network.home_id, network.nodes_count))


def louie_network_failed(network):
    print("Hello from network : can't load :(.")


print "1"


def louie_network_ready(network):
    print("Hello from network : I'm ready : %d nodes were found." % network.nodes_count)
    print("Hello from network : my controller is : %s" % network.controller)

    dispatcher.connect(louie_node_update, ZWaveNetwork.SIGNAL_NODE)

    dispatcher.connect(louie_value_update, ZWaveNetwork.SIGNAL_VALUE)


def louie_node_update(network, node):
    print('Hello from node : %s.' % node)


print "5"


def louie_value_update(network, node, value):
    print('Hello from value : %s.' % value)


print "6"
#Create a network object
network = ZWaveNetwork(options, autostart=False)

#We connect to the louie dispatcher
dispatcher.connect(louie_network_started, ZWaveNetwork.SIGNAL_NETWORK_STARTED)
print "7"
dispatcher.connect(louie_network_failed, ZWaveNetwork.SIGNAL_NETWORK_FAILED)
print "8"
dispatcher.connect(louie_network_ready, ZWaveNetwork.SIGNAL_NETWORK_READY)
print "9"
network.start()

#We wait for the network.
print "***** Waiting for network to become ready : "
for i in range(0, 25):
    if network.state >= network.STATE_READY:
        print "***** Network is ready"
        break
    else:
        sys.stdout.write(".")
        sys.stdout.flush()
        time.sleep(1.0)

time.sleep(5.0)

for node in network.nodes.itervalues():
    
    print("node is :%s" %node)
    for val in node.get_switches():
        print("Val is:%s"%val)
        state = node.get_switch_state(val)
        if state:
            print "Switch is on"
        elif state == False:
            print "Switch is off"

        print "for on type 1 and off type 0"

        while True:
            mydata = raw_input('Prompt :')
            if mydata == "1":
                node.set_switch(val, True)
                print "on"
            elif mydata == "0":
                print "off"
                node.set_switch(val, False)
            elif mydata == "2":
                break

time.sleep(10.0)
network.stop()
        
    
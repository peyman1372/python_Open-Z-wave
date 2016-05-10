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

# Define some manager options
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


def louie_network_ready(network):
    print("Hello from network : I'm ready : %d nodes were found." % network.nodes_count)
    print("Hello from network : my controller is : %s" % network.controller)
    dispatcher.connect(louie_node_update, ZWaveNetwork.SIGNAL_NODE)
    dispatcher.connect(louie_value_update, ZWaveNetwork.SIGNAL_VALUE)


def louie_node_update(network, node):
    print('Hello from node : %s.' % node)


def louie_value_update(network, node, value):
    print('Hello from value : %s.' % value)

# Create a network object
network = ZWaveNetwork(options, autostart=False)

# We connect to the louie dispatcher
dispatcher.connect(louie_network_started, ZWaveNetwork.SIGNAL_NETWORK_STARTED)
dispatcher.connect(louie_network_failed, ZWaveNetwork.SIGNAL_NETWORK_FAILED)
dispatcher.connect(louie_network_ready, ZWaveNetwork.SIGNAL_NETWORK_READY)

network.start()

#We wait for the network.
print "***** Waiting for network to become ready : "
for i in range(0, 30):
    if network.state >= network.STATE_READY:
        print "***** Network is ready"
        break
    else:
        sys.stdout.write(".")
        sys.stdout.flush()
        time.sleep(1.0)


# for node in network.nodes:
#     for val in network.nodes[node].get_switches():
#         print ("val issssssss:%s"%val)
#     print
#     print "------------------------------------------------------------"
#     print "%s - Name : %s" % (network.nodes[node].node_id,network.nodes[node].name)
#     print "%s - Manufacturer name / id : %s / %s" % (network.nodes[node].node_id,network.nodes[node].manufacturer_name, network.nodes[node].manufacturer_id)
#     print "%s - Product name / id / type : %s / %s / %s" % (network.nodes[node].node_id,network.nodes[node].product_name, network.nodes[node].product_id, network.nodes[node].product_type)
#     print "%s - Version : %s" % (network.nodes[node].node_id, network.nodes[node].version)
#     print "%s - Command classes : %s" % (network.nodes[node].node_id,network.nodes[node].command_classes_as_string)
#     print "%s - Capabilities : %s" % (network.nodes[node].node_id,network.nodes[node].capabilities)
#     print "%s - Neigbors : %s" % (network.nodes[node].node_id,network.nodes[node].neighbors)
#     print "%s - Can sleep : %s" % (network.nodes[node].node_id,network.nodes[node].can_wake_up())
#     print "%s - Product name / id / type : %s / %s / %s" % (network.nodes[node].node_id,network.nodes[node].product_name, network.nodes[node].product_id, network.nodes[node].product_type)
#
#     state = ("value is :%s" % network.get_value(72057594109837312))
#     if state:
#         print "Switch is on"
#     elif state == False:
#         print "Switch is off"
#     # if network.get_value(node) == network.get_value(72057594109837312):
#     print "goooo"
#     while True:
#
#         mydata = raw_input('Prompt :')
#         if mydata == "1":
#             print "on"
#             node.set_switch(72057594109837312, True)
#
#
#         elif mydata == "0":
#             print "off"
#             node.set_switch(72057594109837312, False)
#
#         elif mydata == "2":
#             break
#
#         elif mydata == "3":
#
#             print ("the power level is: %s" % node.get_power_levels(72057594109837312))
# values = {}
# for node in network.nodes:
#
#     # for val in network.nodes[node].values :
#
#     # print("value is :%s" % network.get_value(72057594109837312))
#     # print "%s - Product name / id / type : %s / %s / %s" % (network.nodes[node].node_id,network.nodes[node].product_name, network.nodes[node].product_id, network.nodes[node].product_type)
#
#     # for val in node.get_switches():
#     state = ("value is :%s" % network.get_value(72057594109837312))
#
#     if state:
#         print "Switch is on"
#     elif state == False:
#         print "Switch is off"
#     # if network.get_value(node) == network.get_value(72057594109837312):
#     print "goooo"
#     while True:
#
#         mydata = raw_input('Prompt :')
#         if mydata == "1":
#             node.set_switch(72057594109837312, True)
#
#             print "on"
#         elif mydata == "0":
#             print "off"
#             node.set_switch(72057594109837312, False)
#
#         elif mydata == "2":
#             break
#
#         elif mydata == "3":
#             for val in network.nodes[node].get_sensors() :
#
#                 print("  value: %s %s" % (network.nodes[node].get_sensor_value(val), network.nodes[node].values[val].units))
values = {}
while True:
    print "."
    print "-----------------------------------------------------------------------"
    print   "for turn on   :1        for turn off: 0"
    print   "for get detail:2        for exit  3"
    print "-----------------------------------------------------------------------"

    # for node in network.nodes:
    #     for val in network.nodes[node].get_switches():
    #         print("node/name/index/instance : %s/%s/%s/%s" % (
    #             node, network.nodes[node].name, network.nodes[node].values[val].index,
    #             network.nodes[node].values[val].instance))
    #         print(
    #             "  label/help : %s/%s" % (network.nodes[node].values[val].label, network.nodes[node].values[val].help))
    #         print("  id on the network : %s" % (network.nodes[node].values[val].id_on_network))
    #         print("  value: %s %s" % (network.nodes[node].get_sensor_value(val), network.nodes[node].values[val].units))
    # for node in network.nodes:
    #     for val in network.nodes[node].get_switches() :
    #         print network.nodes[node].node_id
    #         if network.nodes[node].node_id==3:
    #             print val
    for node in network.nodes.itervalues():
        for val in node.get_switches():
	        state = node.get_switch_state(72057594109837312)
                if state:
                    print "Switch is on"
                elif state == False:
                    print "Switch is off"
    # for node in network.nodes:
    #         for val in network.nodes[node].get_sensors() :
    #             print network.nodes[node].node_id
    #             if network.nodes[node].node_id==4:
    #                 print val
    mydata = raw_input('Prompt :')
    if mydata == "1":
        for node in network.nodes.itervalues():
            node.set_switch(72057594093060096, True)

    elif mydata == "0":
        for node in network.nodes.itervalues():
            node.set_switch(72057594093060096, False)
    if mydata == "2":
        for node in network.nodes:
            for val in network.nodes[node].get_sensors():
                if network.nodes[node].node_id == 2:
                    print("  %s %s %s" % (
                        network.nodes[node].values[val].label, network.nodes[node].get_sensor_value(val),
                        network.nodes[node].values[val].units))

    elif mydata == "3":
        break

    time.sleep(5.0)

time.sleep(10.0)
network.stop()
        
    


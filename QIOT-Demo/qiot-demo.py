#!/usr/bin/env python3
import subprocess
import os
from lib.qiot_http_client import *
from lib.thread_handler import *
from lib.gather_information import *
my_qiot = QIOT("./qiot-config.json")

hostname = os.uname()[1]
macaddress = subprocess.getoutput("cat /sys/class/net/eth0/address")
my_identity = [{"type": "MAC","value": macaddress}]

registration_token = my_qiot.register(hostname, my_identity)
mythingtoken = my_qiot.get_thing_token("qiot-keys-" + macaddress + ".json")

def gather_info_and_push_to_qiot():
    my_qiot.publish_message_to_thing([RaspberryPi().gather_all_info()], mythingtoken)

thread_caller = call_me_again(60, gather_info_and_push_to_qiot)
# gather_info_and_push_to_qiot()
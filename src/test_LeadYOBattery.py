import logging
import time

from lead_yo_battery import find_all_batteries

logging.basicConfig()
logging.getLogger('lead_yo_battery').setLevel(logging.DEBUG)
batteries = find_all_batteries()
print("Found batteries: " + str(batteries))
for i in range(10):
    for battery in batteries:
        print("Battery: " + battery.name())
        print("     Voltage: " + str(battery.voltage()))
    time.sleep(3)

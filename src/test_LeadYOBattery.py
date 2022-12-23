import logging
from lead_yo_battery import find_all_batteries

logging.basicConfig()
logging.getLogger('lead_yo_battery').setLevel(logging.DEBUG)
batteries = find_all_batteries()
print("Found batteries: " + str(batteries))
for battery in batteries:
    print("Voltage: " + str(battery.voltage()))

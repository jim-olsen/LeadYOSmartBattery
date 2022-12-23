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
        print("     Current: " + str(battery.current()))
        print("     Residual Capacity: " + str(battery.residual_capacity()))
        print("     Nominal Capacity: " + str(battery.nominal_capacity()))
        print("     Cycles: " + str(battery.cycles()))
        print("     Version: " + str(battery.version()))
        print("     Percent Charged: " + str(battery.capacity_percent()) + "%")
    time.sleep(3)

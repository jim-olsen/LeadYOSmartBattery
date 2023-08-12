import logging
import time

from lead_yo_battery import find_all_batteries

logging.basicConfig()
#logging.getLogger('lead_yo_battery').setLevel(logging.DEBUG)
batteries = find_all_batteries()
print("Found batteries: " + str(batteries))
for i in range(10):
    for battery in batteries:
        if battery.name().startswith('BANK'):
            print("Battery: " + battery.name())
            print("     Voltage: " + str(battery.voltage()))
            print("     Current: " + str(battery.current()))
            print("     Residual Capacity: " + str(battery.residual_capacity()))
            print("     Nominal Capacity: " + str(battery.nominal_capacity()))
            print("     Cycles: " + str(battery.cycles()))
            for i in range(battery.num_cells()):
                print("     Cell " + str(i + 1) + " Balance Status: " + str(battery.balance_status(i + 1)))
            print("     Protection Issues: " + str(battery.protection_status()))
            print("     Version: " + str(battery.version()))
            print("     Percent Charged: " + str(battery.capacity_percent()) + "%")
            print("     Current Status: " + battery.control_status())
            print("     Number of Cells: " + str(battery.num_cells()))
            print("     Temperatures: " + str(battery.battery_temps_f()))
            print("     Cell Voltages: " + str(battery.cell_block_voltages()))
    time.sleep(3)

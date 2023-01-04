from lead_yo_battery.SmartBattery import SmartBattery
import asyncio
import logging
from bleak import BleakScanner

logger = logging.getLogger('lead_yo_battery')


async def async_find_all_batteries() -> [SmartBattery]:

    logger.debug("Finding all available batteries within range")
    found_batteries = []
    devices = await BleakScanner.discover(timeout=10, return_adv=False)
    for d in devices:
        logger.debug('%s>>%s>>%s>>%s', str(d.name), str(d.address), str(d.metadata), str(d.rssi))
        manufacturer_data = d.metadata.get('manufacturer_data', {})
        if 15984 in manufacturer_data:
            logger.info("Found battery %s at %s", str(d.name), str(d.address))
            found_batteries.append(SmartBattery(d.address, d.name))

    return found_batteries


def find_all_batteries() -> [SmartBattery]:
    return asyncio.run(async_find_all_batteries())


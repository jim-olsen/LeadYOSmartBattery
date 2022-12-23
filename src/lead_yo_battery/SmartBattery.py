import asyncio
import logging
import time

from bleak import BleakClient

logger = logging.getLogger('lead_yo_battery')

class SmartBattery:
    SPP_DATA_UUID = '0000ff01-0000-1000-8000-00805f9b34fb'
    SPP_COMMAND_UUID = '0000ff02-0000-1000-8000-00805f9b34fb'

    def __init__(self, battery_address, battery_name):
        self.battery_address = battery_address
        self.battery_name = battery_name
        self.spp_command_characteristic = None
        self.spp_data_characteristic = None
        self.basic_information_and_status = None
        self.last_basic_info_update = None

    async def async_update_characteristics(self, client):
        self.spp_data_characteristic = None
        self.spp_command_characteristic = None
        for service in client.services:
            logger.debug("%s", str(service))
            try:
                logger.debug(">>>> Service Characteristics")
                for characteristic in service.characteristics:
                    logger.debug("      %s:%s", str(characteristic), str(characteristic.properties))
                    if characteristic.uuid == SmartBattery.SPP_DATA_UUID:
                        logger.debug("Found SPP data characteristic")
                        self.spp_data_characteristic = characteristic
                    elif characteristic.uuid == SmartBattery.SPP_COMMAND_UUID:
                        logger.debug("Found SPP command characteristic")
                        self.spp_command_characteristic = characteristic
            except Exception as e:
                print(e)

    async def async_get_basic_info_and_status(self):
        command_complete = asyncio.Event()
        data_length_of_response = 0

        def data_received(characteristic, data):
            nonlocal data_length_of_response
            logger.debug("Received data: %s", str(data))

            # If we receive the correct response to our request to get the info start gathering it
            if data[:2] == bytearray([0xDD, 0x03]):
                self.basic_information_and_status = bytearray()
                data_length_of_response = int.from_bytes(bytearray([0x00]) + data[3:4], byteorder='big')
                logger.debug("Total length of data response %s", str(data_length_of_response))
                self.basic_information_and_status = bytearray(data[4:])
                logger.debug("Current response data: " + str(self.basic_information_and_status))
                if len(self.basic_information_and_status) == data_length_of_response:
                    logger.debug("Got all the data, proceeding")
                    command_complete.set()
                else:
                    logger.debug("Response data not complete, waiting for more data to arrive")
            elif data_length_of_response != 0:
                logger.debug("Appending additional data")
                self.basic_information_and_status.extend(data[:-3])
                logger.debug("New length of data is now %s", len(self.basic_information_and_status))
                if len(self.basic_information_and_status) >= data_length_of_response:
                    logger.debug("Got all the data, proceeding")
                    command_complete.set()
            else:
                self.basic_information_and_status = None
                command_complete.set()

        self.basic_information_and_status = None
        while self.basic_information_and_status is None:
            try:
                async with BleakClient(self.battery_address) as client:
                    await self.async_update_characteristics(client)
                    await client.start_notify(self.spp_data_characteristic, data_received)
                    while self.basic_information_and_status is None:
                        try:
                            command_complete.clear()
                            logger.debug("Sending command to fetch basic info and status from battery")
                            await client.write_gatt_char(self.spp_command_characteristic,
                                         bytearray([0xDD, 0xA5, 0x03, 0x00, 0xFF, 0xFD, 0x77]), response=False)
                            await asyncio.wait_for(command_complete.wait(), 1)
                        except Exception as e:
                            logger.error("Failed to receive result from battery to command request: %s" + str(e))
            except Exception as e:
                logger.error("Failed to connect to battery: " + str(e))
            except asyncio.exceptions.CancelledError as ce:
                logger.error("Failed to connect to battery: " + str(ce))
        self.last_basic_info_update = time.time()

    def get_basic_info_and_status(self):
        asyncio.run(self.async_get_basic_info_and_status())

    def name(self) -> str:
        return self.battery_name

    def voltage(self) -> float:
        if self.basic_information_and_status is None or self.last_basic_info_update is None or \
                time.time() - self.last_basic_info_update >= 5:
            self.get_basic_info_and_status()
        return float(int.from_bytes(self.basic_information_and_status[0:2], byteorder='big')) / 100


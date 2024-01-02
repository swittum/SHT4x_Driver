#!./venv/bin/python3
import struct
import asyncio
import bleak
from bleak import BleakScanner, BleakClient

import numpy as np


async def scan_devices():
    devices = await BleakScanner.discover()
    for device in devices:
        print(device)


class SHT:
    def __init__(self, UUID):
        self._client = BleakClient(UUID)

    async def connect(self):
        print('Connecting to SHT')
        try:
            await self._client.connect()
            if self._client.is_connected:
                print('Connection successful')
        except bleak.exc.BleakDeviceNotFoundError:
                print('Could not find SHT')
                exit(1)

    async def disconnect(self):
        print('Closing connection to SHT')
        await self._client.disconnect()

    async def get_services(self):
        services = await self._client.get_services()
        for service in services:
            print(f"Service: {service}")
            for char in service.characteristics:
                print(f"Characteristic: {char}")

    async def get_battery(self):
        out = await self._client.read_gatt_char('00002a19-0000-1000-8000-00805f9b34fb')
        status = struct.unpack('B', out)
        return status[0]
    
    async def get_humidity(self):
        out = await self._client.read_gatt_char('00001235-b38d-4985-720e-0f993a68ee41')
        RH = struct.unpack('<f', out)[0]
        return RH
    
    async def get_temperature(self):
        out = await self._client.read_gatt_char('00002235-b38d-4985-720e-0f993a68ee41')
        T = struct.unpack('<f', out)[0]
        return T
    
    async def get_dewpoint(self):
        RH = await self.get_humidity()
        T = await self.get_temperature()
        a = 17.625
        b = 243.04
        alpha = np.log(RH/100)+a*T/(b+T)
        dp = b*alpha/(a-alpha)
        return dp


if __name__ == '__main__':
    asyncio.run(scan_devices())
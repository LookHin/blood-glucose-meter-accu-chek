import sys
import asyncio
import time

from typing import Sequence
from bleak import BleakClient, BleakScanner
from bleak.backends.device import BLEDevice

GLUCOSE_DEVICE_ADDRESS = "84:C6:XX:XX:64:64" # Change to your device address

async def getDeviceInfo(address):
  print("Connect To: ", address, "\t\t", time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()))

  async with BleakClient(address) as client:
    services = client.services

    for service in services:
      print("\nService: ", service.handle, service.uuid, service.description)

      characteristics = service.characteristics

      for char in characteristics:
        print("\tCharacteristic: ", char.handle, char.uuid, char.description, char.properties)

        descriptors = char.descriptors

        for desc in descriptors:
          print("\t\tDescriptor: ", desc)

    print("--------------------------------------------------\n")

async def findBluetoothDevice():
    devices: Sequence[BLEDevice] = await BleakScanner.discover(timeout=1)

    for device in devices:
        if device.address == GLUCOSE_DEVICE_ADDRESS:
            await getDeviceInfo(device.address)

print("If you want to exit, you can press Ctrl + C.\n")

while True:
    try:
        loop = asyncio.get_event_loop()
        loop.run_until_complete(findBluetoothDevice())
    except KeyboardInterrupt:
        print("\nExit\n")
        sys.exit(0)
    except Exception as e:
        print("Exception Message:", str(e))
        time.sleep(1)

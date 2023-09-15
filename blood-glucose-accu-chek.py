# pip3 install requests
# pip3 install bleak
# pip3 install asyncio

import sys
import asyncio
import struct
import requests
import time
import platform

from typing import Sequence
from bleak import BleakClient, BleakScanner
from bleak.backends.device import BLEDevice
from datetime import datetime
from requests.structures import CaseInsensitiveDict

GLUCOSE_DEVICE_ADDRESS = "84:C6:XX:XX:64:64" # Change to your device address
GLUCOSE_MEASUREMENT_UUID = "00002a18-0000-1000-8000-00805f9b34fb" # glucose measurement UUID

def glucoseMeasurement(handle, data):
    unpackData = [dt[0] for dt in struct.iter_unpack("<B", data)]

    hexData = [hex(dt) for dt in unpackData]
    print("hexData:", hexData)

    deviceDateTime = "{:04d}-{:02d}-{:02d} {:02d}:{:02d}:{:02d}".format(int(((unpackData[4] & 0xFF) << 8) | unpackData[3]), int(unpackData[5]), int(unpackData[6]), int(unpackData[7]), int(unpackData[8]), int(unpackData[9]))

    # Convert to Local Time Zone
    currentTimestamp = time.time()
    localTimeZoneOffset = datetime.fromtimestamp(currentTimestamp) - datetime.utcfromtimestamp(currentTimestamp)
    currentDateTime = datetime.strptime(deviceDateTime, "%Y-%m-%d %H:%M:%S") + localTimeZoneOffset

    glucoseMg = "{:.1f}".format((((unpackData[12] & 0xFF) << 8) | (unpackData[11] & 0xFF)) / 256.0)
    glucoseMm = "{:.1f}".format(((((unpackData[12] & 0xFF) << 8) | (unpackData[11] & 0xFF)) / 256.0) / 18.0)

    print("Date Time: ", str(currentDateTime.strftime("%Y-%m-%d %H:%M:%S")), "\t\tGlucose: ", glucoseMm, "mmol/L , ", glucoseMg, "mg/dL")

async def receiveNotification():
    print("Connect To: ", GLUCOSE_DEVICE_ADDRESS, "\t\t", time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()))

    async with BleakClient(GLUCOSE_DEVICE_ADDRESS) as client:
        await client.start_notify(GLUCOSE_MEASUREMENT_UUID, glucoseMeasurement)
        await asyncio.sleep(5.0)
        await client.stop_notify(GLUCOSE_MEASUREMENT_UUID)

async def findBluetoothDevice():
    devices: Sequence[BLEDevice] = await BleakScanner.discover(timeout=1)

    for device in devices:
        if device.address == GLUCOSE_DEVICE_ADDRESS:
            await receiveNotification()

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

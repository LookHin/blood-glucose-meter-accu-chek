import sys
import asyncio
import time

from typing import Sequence
from bleak import BleakScanner
from bleak.backends.device import BLEDevice

async def findBluetoothDevice():
    devices: Sequence[BLEDevice] = await BleakScanner.discover(timeout=1)

    print("** Date Time: ", time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()), "**\n")

    for device in devices:
        print(device)

    print("--------------------------------------------------\n")

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

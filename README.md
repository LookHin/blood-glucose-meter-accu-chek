# bloud-glucose-meter-accu-chek

![Image](https://www.onlyme.dev/github/glucose-meter-accu-chek/1.png?v=3)

### Caution
The distance between the accu-chek meter and computer must be within 3 meters.

### 0. Install library

```
# apt-get update
# apt-get install -y bluez* pkg-config libbluetooth-dev libglib2.0-dev
# apt-get install -y libboost-thread-dev libboost-python-dev python3-capstone

# pip3 install requests
# pip3 install bleak
# pip3 install asyncio
```

### 1. discover.py

```
# nano discover.py
```

```python
import sys
import asyncio
import time

from typing import Sequence
from bleak import BleakScanner

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
```

### 2. Find device address

```
# python3 discover.py
```

![Image](https://www.onlyme.dev/github/glucose-meter-accu-chek/2.png)

### 3. Pairing device and enter PIN code
```
# bluetoothctl
[bluetooth]# scan on
[bluetooth]# trust 84:C6:XX:XX:64:64
[bluetooth]# pair 84:C6:XX:XX:64:64
```
![Image](https://www.onlyme.dev/github/glucose-meter-accu-chek/6.png?v=2)

![Image](https://www.onlyme.dev/github/glucose-meter-accu-chek/3.png?v=2)

### 4. blood-glucose-accu-chek.py

```
# nano blood-glucose-accu-chek.py
```

```python
import sys
import asyncio
import struct
import requests
import time
import platform

from typing import Sequence
from bleak import BleakClient, BleakScanner
from datetime import datetime
from requests.structures import CaseInsensitiveDict

GLUCOSE_DEVICE_ADDRESS = "84:C6:XX:XX:64:64" # Change to your device address
GLUCOSE_MEASUREMENT_UUID = "00002a18-0000-1000-8000-00805f9b34fb" # Glucose measurement UUID

def glucoseMeasurement(handle, data):
    unpackData = [dt[0] for dt in struct.iter_unpack("<B", data)]

    hexData = [hex(dt) for dt in unpackData]
    print("hexData : ", hexData)

    deviceDateTime = "{:04d}-{:02d}-{:02d} {:02d}:{:02d}:{:02d}".format(int(((unpackData[4] & 0xFF) << 8) | unpackData[3]), int(unpackData[5]), int(unpackData[6]), int(unpackData[7]), int(unpackData[8]), int(unpackData[9]))

    # Convert to Local Time Zone
    currentTimestamp = time.time()
    localTimeZoneOffset = datetime.fromtimestamp(currentTimestamp) - datetime.utcfromtimestamp(currentTimestamp)
    currentDateTime = datetime.strptime(deviceDateTime, "%Y-%m-%d %H:%M:%S") + localTimeZoneOffset

    glucoseMm = (unpackData[10] / 10.0)
    glucoseMg = "{:.1f}".format((unpackData[10] / 10.0) * 18)

    print("Date Time: ", str(currentDateTime.strftime("%Y-%m-%d %H:%M:%S")), "\t\tGlucose: ", glucoseMm, "mmol/L , ", glucoseMg, "mg/dL")

async def receiveNotification():
    print("Connect To: ", GLUCOSE_DEVICE_ADDRESS, "\t\t", time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()))

    async with BleakClient(GLUCOSE_DEVICE_ADDRESS) as client:
        await client.start_notify(GLUCOSE_MEASUREMENT_UUID, glucoseMeasurement)
        await asyncio.sleep(60)
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
```

### 5. Run

```
# python3 blood-glucose-accu-chek.py
```

![Image](https://www.onlyme.dev/github/glucose-meter-accu-chek/5.png)


## About Us
Name : Khwanchai Kaewyos (LookHin)

Email : khwanchai@gmail.com

## Website
[https://www.onlyme.dev](https://www.onlyme.dev)

[https://www.facebook.com/LookHin](https://www.facebook.com/LookHin)


## License

MIT License

Copyright (c) 2023 Khwanchai Kaewyos

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.


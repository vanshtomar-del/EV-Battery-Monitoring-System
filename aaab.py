import network
import urequests
import ujson
import random
import time

# Wi-Fi Credentials
SSID = "Wifi-Name"
PASSWORD = "Wifi-Password"

# Firebase URL
FIREBASE_URL = "https://ev-battery-monitoring-fba3e-default-rtdb.firebaseio.com/battery.json"

# Connect to Wi-Fi
wifi = network.WLAN(network.STA_IF)
wifi.active(True)

if not wifi.isconnected():
    wifi.connect(SSID, PASSWORD)
    while not wifi.isconnected():
        pass

print("WiFi Connected")

while True:
    voltage = round(random.uniform(3.2, 4.2), 2)
    current = round(random.uniform(0.5, 3.0), 2)
    temperature = random.randint(25, 45)
    soc = random.randint(20, 100)
    power = round(voltage * current, 2)

    # Alert Logic
    if temperature > 40:
        status = "High Temperature"
    elif voltage < 3.3:
        status = "Low Battery"
    elif current > 2.5:
        status = "High Current"
    else:
        status = "Normal"

    data = {
        "voltage": voltage,
        "current": current,
        "temperature": temperature,
        "soc": soc,
        "power": power,
        "status": status
    }

    response = urequests.put(
        FIREBASE_URL,
        data=ujson.dumps(data),
        headers={"Content-Type": "application/json"}
    )

    print(data)

    response.close()
    time.sleep(5)
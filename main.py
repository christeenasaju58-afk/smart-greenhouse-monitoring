import network
import time
import dht
import urequests
from machine import Pin

# DHT22 connected to GPIO 15
sensor = dht.DHT22(Pin(15))

# Wokwi Wi-Fi
SSID = "Wokwi-GUEST"
PASSWORD = ""

# ThingSpeak
API_KEY = "YOUR_WRITE_API_KEY"
URL = "http://api.thingspeak.com/update"

# Connect to Wi-Fi
wifi = network.WLAN(network.STA_IF)
wifi.active(True)
wifi.connect(SSID, PASSWORD)

print("Connecting to Wi-Fi...")

while not wifi.isconnected():
    time.sleep(1)

print("Wi-Fi connected!")
print("IP address:", wifi.ifconfig()[0])

# Greenhouse monitoring
while True:
    try:
        # Read DHT22
        sensor.measure()

        temperature = sensor.temperature()
        humidity = sensor.humidity()

        print("----------------------")
        print("Greenhouse Monitoring")
        print("Temperature:", temperature, "°C")
        print("Humidity:", humidity, "%")

        # Send data to ThingSpeak
        response = urequests.get(
            URL +
            "?api_key=" + API_KEY +
            "&field1=" + str(temperature) +
            "&field2=" + str(humidity)
        )

        print("ThingSpeak response:", response.text)
        response.close()

    except Exception as e:
        print("Error:", e)

    # ThingSpeak minimum interval is 15 seconds
    time.sleep(20)

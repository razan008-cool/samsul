import urequests
import network
import utime
from machine import Pin

# Konfigurasi WiFi
SSID = "Nama_WiFi"  # Ganti dengan SSID WiFi
PASSWORD = "Password_WiFi"  # Ganti dengan password WiFi

# Token API Ubidots
UBIDOTS_TOKEN = "BBUS-Y5s7CObAKhExn20yRnu9kKoGYTXnBB"  # Ganti dengan token Ubidots
DEVICE_LABEL = "esp32_ultrasonic"
VARIABLE_LABEL = "distance"
UBIDOTS_URL = f"http://industrial.api.ubidots.com/api/v1.6/devices/{DEVICE_LABEL}/"

# Inisialisasi WiFi
def connect_wifi():
    wlan = network.WLAN(network.STA_IF)
    wlan.active(True)
    wlan.connect(SSID, PASSWORD)

    while not wlan.isconnected():
        print("Menghubungkan ke WiFi...")
        utime.sleep(2)

    print("Terhubung ke WiFi:", wlan.ifconfig())

# Inisialisasi sensor ultrasonik
trig = Pin(23, Pin.OUT)
echo = Pin(22, Pin.IN)

def get_distance():
    trig.off()
    utime.sleep_us(2)
    trig.on()
    utime.sleep_us(10)
    trig.off()
    
    while echo.value() == 0:
        signal_off = utime.ticks_us()
    
    while echo.value() == 1:
        signal_on = utime.ticks_us()
    
    time_passed = signal_on - signal_off
    distance = (time_passed * 0.0343) / 2  # Rumus jarak dalam cm
    return round(distance, 2)

# Kirim data ke Ubidots
def send_data(distance):
    headers = {
        "X-Auth-Token": UBIDOTS_TOKEN,
        "Content-Type": "application/json"
    }
    data = {VARIABLE_LABEL: distance}
    
    response = urequests.post(UBIDOTS_URL, json=data, headers=headers)
    print("Data terkirim:", response.json())
    response.close()

# Main Program
connect_wifi()

while True:
    distance = get_distance()
    print("Jarak:", distance, "cm")
    send_data(distance)
    utime.sleep(5)  # Kirim data setiap 5 detik

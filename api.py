import os
import sys
import adafruit_dht
import board
import django
from django.conf import settings
from django.http import JsonResponse
from django.urls import path
from django.core.management import execute_from_command_line
from django.core.wsgi import get_wsgi_application

# Minimal Django settings
settings.configure(
    DEBUG=False,
    ROOT_URLCONF=__name__,
    ALLOWED_HOSTS=['*'],
    MIDDLEWARE=[],
    INSTALLED_APPS=[
        'django.contrib.contenttypes',
    ],
)

# Setup Django
django.setup()

def read_sensor():
    try:
        # Initialize the DHT sensor inside the function
        dht_device = adafruit_dht.DHT22(board.D4)
        print("Reading sensor data...")
        temperature_c = dht_device.temperature
        humidity = dht_device.humidity
        print(f"Read temperature: {temperature_c}, humidity: {humidity}")
        return {"temperature": temperature_c, "humidity": humidity}
    except RuntimeError as e:
        print(f"Sensor reading error: {e}")
        return {"temperature": None, "humidity": None}
    finally:
        # Clean up the sensor to ensure it's ready for the next read
        dht_device.exit()

# Define a simple view
def index(request):
    data = read_sensor()
    if data["temperature"] is None or data["humidity"] is None:
        return JsonResponse({"error": "Failed to read sensor data"}, status=500)
    return JsonResponse(data)

# URL patterns
urlpatterns = [
    path('', index),
]

# WSGI application
application = get_wsgi_application()

if __name__ == "__main__":
    print("Starting Django server...")
    execute_from_command_line(sys.argv)

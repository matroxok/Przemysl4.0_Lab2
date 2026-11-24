import time
import random
import pigpio # http://abyz.co.uk/rpi/pigpio/python.html
import RPi.GPIO as GPIO
import paho.mqtt.client as mqtt

#konfiguracja protokołu MQTT
broker_address = "10.104.32.253" 
broker_port = 1883
topic = "sensor/data"

#konfiguracja diod LED z Zadania 1
led = [19, 18, 13, 12]
GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)
for i in range(0, 4):
    GPIO.setup(led[i], GPIO.OUT)
    GPIO.output(led[i], GPIO.LOW)

#inicjalizacja czujnika pigpio
pi = pigpio.pi()
poprzednia = 0

if not pi.connected:
    exit(0)

sensor = pi.spi_open(1, 1000000, 0) # CE1, 1Mbps, main SPI

#inicjalizacja klienta MQTT
client = mqtt.Client()
client.connect(broker_address, broker_port, 60)

stop = time.time() + 600
while time.time() < stop:
    c, d = pi.spi_read(sensor, 2)
    if c == 2:
        sign = (d[0] & 0x80) >> 7
        value = (((d[0] & 0x7f) << 8) | d[1]) >> 5
        temp = value * 0.125
        if sign == 1:
            temp = temp * -1

        # Sterowanie diodami LED (Zadanie 1)
        for i in range(0, 3):
            GPIO.output(led[i], GPIO.LOW)

        if poprz_temp := poprzednia:
            if poprz_temp > temp + 0.15:
                print("Spadek")
                GPIO.output(led[1], GPIO.HIGH)
            elif poprz_temp < temp - 0.15:
                print("Wzrost")
                GPIO.output(led[0], GPIO.HIGH)
            else:
                print("Stabilna")
                GPIO.output(led[2], GPIO.HIGH)

        poprzednia = temp

        humidity = random.randint(150, 300) / 10

        #wysyl
        payload = f"{temp:.2f} {humidity:.2f}"
        client.publish(topic, payload)
        
        print(f"Temperatura: {temp:.2f}°C | Wilgotność: {humidity:.2f}% | Opublikowano: {payload}")

    time.sleep(1) # Odczyt co 1 sekundę

pi.spi_close(sensor)
pi.stop()
GPIO.cleanup()



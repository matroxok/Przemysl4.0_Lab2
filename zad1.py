import time
import pigpio # http://abyz.co.uk/rpi/pigpio/python.html
import RPi.GPIO as GPIO

led = [19,18,13,12]
GPIO.setwarnings(False) # ignorowanie ostrzeżeń
GPIO.setmode(GPIO.BCM) # WAŻNY KROK -- ustawiamy jaką numerację pinów wykorzystamy
for i in range(0,4):
        GPIO.setup(led[i], GPIO.OUT)
        GPIO.output(led[i], GPIO.LOW)

pi = pigpio.pi()
poprzednia=0
if not pi.connected:
   exit(0)
sensor = pi.spi_open(1, 1000000, 0)   # CE1, 1Mbps, main SPI
stop = time.time() + 600
while time.time() < stop:
   c, d = pi.spi_read(sensor, 2)
   if c == 2:
    sign = (d[0] & 0x80) >> 7
    value = (((d[0] & 0x7f)<<8) | d[1]) >> 5
    temp = value * 0.125
    if sign == 1:
        temp = temp * -1
    for i in range(0,3):
        GPIO.output(led[i], GPIO.LOW)
    if poprzednia > temp + 0.15:
        print("Spadek")
        GPIO.output(led[1], GPIO.HIGH)
        poprzednia = temp
        
    elif poprzednia < temp - 0.15:
        print("Wzrost")
        GPIO.output(led[0], GPIO.HIGH)
        poprzednia = temp
    else:
       print("stabilna")    
       GPIO.output(led[2], GPIO.HIGH)
    print("{:.2f}".format(temp))
   
   time.sleep(1) # Don't try to read more often than 4 times a second.
pi.spi_close(sensor)
pi.stop()



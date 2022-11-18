import adafruit_l3gd20
from busio import I2C
from board import SDA, SCL

from time import sleep

i2c = I2C(SCL, SDA)
sensor = adafruit_l3gd20.L3GD20_I2C(i2c)


try:
    while True:
        print(sensor.gyro_raw)
        sleep(1)

except (KeyboardInterrupt, SystemExit):
    quit()
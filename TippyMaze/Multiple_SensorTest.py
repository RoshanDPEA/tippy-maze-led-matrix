from time import sleep
from hardware.LidarSensor import LidarSensor
from pidev.Cyprus_Commands import Cyprus_Commands_RPi as cyprus
from hardware.GumBallRelease import GumBallReleaseMotor


GUMBALL_RELEASE = GumBallReleaseMotor(motor_port=3, sensor_port=4, sensor_threshold=25)

UpperSensor = LidarSensor(port=0, threshold=25)  # first sensor on ramp down
LowerSensor = LidarSensor(port=2, threshold=25)  # Second sensor on ramp down
GumballSensor = LidarSensor(port=4, threshold=25)  # Sensor on exit ramp from Gumball dispenser

if __name__ == '__main__':
    cyprus.initialize()
    version = cyprus.read_firmware_version()  # read the version of the cyprus firmware
    print("Cyprus Version " + str(version))  # print the version to the screen - should be something like 3.1.2 (11/12/19)
    UpperSensor.reset()
    sleep(0.05)
    LowerSensor.reset()
    sleep(0.05)
    GumballSensor.reset()
    sleep(0.05)
    UpperSensor.refresh_last_read()
    sleep(0.05)
    LowerSensor.refresh_last_read()
    sleep(0.05)
    GumballSensor.refresh_last_read()
    try:
        while True:
            print("Upper   Sensor Distance " + str(UpperSensor.distance()))
            sleep(0.05)
            if UpperSensor.detected_object():
                print("*** ALERT -- Upper Sensor DETECTED OBJECT ***")
                sleep(0.05)
                UpperSensor.reset()
            print("Lower   Sensor Distance " + str(LowerSensor.distance()))
            sleep(0.05)
            if LowerSensor.detected_object():
                print("*** ALERT -- Lower Sensor DETECTED OBJECT ***")
                sleep(0.05)
                LowerSensor.reset()
            sleep(0.05)
            print("Gumball Sensor Distance " + str(GumballSensor.distance()))
            sleep(0.05)
            if GumballSensor.detected_object():
                print("*** ALERT -- Gumball Sensor DETECTED OBJECT ***")
                sleep(0.05)
                GumballSensor.reset()
            sleep(0.05)
    except KeyboardInterrupt:
         quit()
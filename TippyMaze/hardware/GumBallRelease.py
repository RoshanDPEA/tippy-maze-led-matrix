"""
@file GumBallRelease.py File to control the gumball release motor
"""
from time import sleep
from Slush.Devices import L6470Registers as LReg
from pidev.stepper import stepper

from hardware.LidarSensor import LidarSensor

GUMBALL_MOTOR_SETTINGS = {
    'hold_current': 2,
    'run_current': 26,
    'acc_current': 26,
    'dec_current': 26,
    'max_speed': 300,
    'min_speed': 0,
    'micro_steps': 4,
    'threshold_speed': 10000,
    'over_current': 3000,
    'stall_current': 3125,
    'accel': 0xffe,
    'decel': 0xffe,
    'slope': [0x0F05, 0x2F, 0x5A,0x5A]
}


class GumBallReleaseMotor:
    def __init__(self, motor_port, sensor_port, sensor_threshold, timeout=20):
        """
        Initialize the gumball release motor
        :param motor_port: port the gumball release motor is attached to
        :param sensor_port: Port the lidar sensor is attached to to detect if a ball has been released yet
        :param sensor_threshold: The threshold to determine whether a gumball has been release yet
        """
        self.motor = stepper(port=motor_port, speed=GUMBALL_MOTOR_SETTINGS['max_speed'])
        self.setup_motor()

        self.sensor = LidarSensor(port=sensor_port, threshold=sensor_threshold)
        self.sensor_timeout = timeout
        #self.released = False

    def setup_motor(self,):
        """
        Setup the motor with the predetermined settings
        :return: None
        """
        self.motor.setCurrent(hold=GUMBALL_MOTOR_SETTINGS['hold_current'], run=GUMBALL_MOTOR_SETTINGS['run_current'],
                              acc=GUMBALL_MOTOR_SETTINGS['acc_current'], dec=GUMBALL_MOTOR_SETTINGS['dec_current'])
        self.motor.setMaxSpeed(GUMBALL_MOTOR_SETTINGS['max_speed'])
        self.motor.setMinSpeed(GUMBALL_MOTOR_SETTINGS['min_speed'])
        self.motor.setMicroSteps(GUMBALL_MOTOR_SETTINGS['micro_steps'])
        self.motor.setThresholdSpeed(GUMBALL_MOTOR_SETTINGS['threshold_speed'])
        self.motor.setOverCurrent(GUMBALL_MOTOR_SETTINGS['over_current'])
        self.motor.setStallCurrent(GUMBALL_MOTOR_SETTINGS['stall_current'])
        self.motor.setAccel(GUMBALL_MOTOR_SETTINGS['accel'])
        self.motor.setDecel(GUMBALL_MOTOR_SETTINGS['decel'])

        slope = GUMBALL_MOTOR_SETTINGS['slope']
    #    self.motor.setSlope(slope[0], slope[1], slope[2], slope[3])

        self.motor.setLowSpeedOpt(False)
        self.motor.setParam(LReg.CONFIG, 0x3688)

    def release_gumball(self):
        """
        Release a gumball by running the motor until the lidar sensor detects a gumball.
        Warning this method is blocking.
        :return: None
        """
        #self.released = False
        self.motor.run(dir=1, spd=GUMBALL_MOTOR_SETTINGS['max_speed'])

        while not self.sensor.detected:
            sleep(.05)
            self.sensor.refresh_last_read()

        print("gumball detected")
        self.motor.hard_stop()

        self.sensor.reset()  # reset the sensor for next release
        #self.released = True

    def free(self):
        """
        Free the attached motor
        :return: None
        """
        self.motor.free()

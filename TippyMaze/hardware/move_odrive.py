import time
from time import sleep
from hardware.Joystick import Joystick

joystick = Joystick(0, True)


class move_odrive:

    def __init__(self, axis0, axis1, speed, current, length_of_track):
        self.axis_0 = axis0
        self.axis_1 = axis1
        self.axis_0.set_vel_limit(speed+5000)
        self.axis_1.set_vel_limit(speed+5000)
        self.axis_0.set_accel_limit(200000)
        self.axis_1.set_accel_limit(200000)
        self.axis_0.set_decel_limit(200000)
        self.axis_1.set_decel_limit(200000)
        self.axis_0.set_curr_limit(current)
        self.axis_1.set_curr_limit(current)
        self.vel_speed = speed
        self.full_length = length_of_track
        self.restricted_length = 20000

    # X-axis
    def run_axis_1(self):
        pos = self.axis_1.get_pos()

        if pos < (self.full_length - self.restricted_length) and joystick.get_axis('x') < -.05:
            self.axis_1.set_vel(self.vel_speed * -joystick.get_axis('x'))

        elif pos > self.restricted_length and joystick.get_axis('x') > .05:
            self.axis_1.set_vel(self.vel_speed * -joystick.get_axis('x'))

        else:
            self.axis_1.set_vel(0)

    # Y-axis
    def run_axis_0(self):
        pos = self.axis_0.get_pos()

        if pos > self.restricted_length and joystick.get_axis('y') < -.03:
            self.axis_0.set_vel(self.vel_speed * joystick.get_axis('y'))

        elif pos < (self.full_length - self.restricted_length) and joystick.get_axis('y') > .03:
            self.axis_0.set_vel(self.vel_speed * joystick.get_axis('y'))

        else:
            self.axis_0.set_vel(0)

    def trajectory_mode(self, location1, location2):
        """
        blocking function that sets the motors to a specific location
        :param location1: set point on the track one wants axis1 to go to
        :param location2: set point on the track one wants axis0 to go to
        :return: none
        """
        while abs(self.axis_1.get_pos() - location1) >= 50 or abs(self.axis_0.get_pos() - location2) >= 50:
            self.axis_0.set_pos_trap(location2)
            self.axis_1.set_pos_trap(location1)
            self.axis_1.get_pos()
            self.axis_0.get_pos()

    def home(self):
        """
        Method to home the Odrive
        :return: None
        """

        self.axis_0.home_with_vel(15000, -1)  # ODrive goes until it hits itself
        self.axis_0.set_pos(4000)  # a short but burst of movement to get the odrive off of itself
        sleep(1)
        now = time.time() + 7
        while abs(self.axis_0.get_pos() - 71000) >= 50 and time.time() <= now:  # moves odrive to be centered
            print("tracking y")
            self.axis_0.set_pos_trap(71000)
            self.axis_0.get_pos()

        # repeat process with axis_1
        self.axis_1.home_with_vel(15000, -1)
        self.axis_1.set_pos(4000)
        sleep(1)
        now = time.time() + 7
        while abs(self.axis_1.get_pos() - 74000) >= 50 and time.time() <= now:
            print("tracking x")
            self.axis_1.set_pos_trap(74000)
            self.axis_1.get_pos()

    def set_up_odrives(self):
        """
        A quick method to set up the odrives
        :return: None
        """
        self.axis_1.clear_errors()
        self.axis_0.clear_errors()
        self.axis_0.set_calibration_current(10)
        self.axis_1.set_calibration_current(10)
        self.axis_0.calibrate()
        self.axis_1.calibrate()

        # god tier code to switch variables if needed
        # right_end = right_end ^ left_end
        # left_end = right_end ^ left_end
        # right_end = right_end ^ left_end




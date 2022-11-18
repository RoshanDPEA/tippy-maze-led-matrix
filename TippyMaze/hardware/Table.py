"""
@file Table.py File containing Table Class code to control movement of the table, based upon given joystick input.
Note: Table knows nothing about how the Joystick has been implemented, only what to do with given values
"""
import numpy as np
from Slush.Devices import L6470Registers as LReg
from pidev.stepper import stepper


AXIS_MOTOR_SETTINGS = {
    'hold_current': 30,
    'run_current': 25,
    'acc_current': 25,
    'dec_current': 25,
    'max_speed': 135,
    'min_speed': 0,
    'micro_steps': 4,
    'threshold_speed': 800,
    'over_current': 2250,
    'stall_current': 2285.15625,
    'accel': 0xF00,
    'decel': 0xF00,
    'low_speed_opt': False,
    'homing_direction': 0,
    'homing_level_distance': 3.5,
    'output_max': None,
    'output_min': None,
    'scaling_factor': 9
}


class Table:
    """
    Class to handle moving the table
    """

    def __init__(self, x_axis_port, y_axis_port):
        """
        Initialize the table
        :param x_axis_port: Port the motor controlling the x-axis is on
        :param y_axis_port: Port the motor controlling the y-axis is on
        """
        steps_per_unit = (200/25.4) * 4.25
        self.motor_x = stepper(port=x_axis_port, speed=AXIS_MOTOR_SETTINGS['max_speed'], steps_per_unit=steps_per_unit)
        self.motor_y = stepper(port=y_axis_port, speed=AXIS_MOTOR_SETTINGS['max_speed'], steps_per_unit=steps_per_unit)
        self.motors = [self.motor_x, self.motor_y]
        self.setup_motors()

        self.homing = False

    def home(self):
        """
        Home the motors, then level the table.
        :return: None
        """
        self.homing = True
        offset_distance = AXIS_MOTOR_SETTINGS['homing_level_distance']

        # move table towards or away from motor_x to find a place where homing is possible
        # if self.motor_x.read_switch() == 0:
        #     self.motor_x.relative_move(-2)
        #     if self.motor_x.read_switch() == 1:
        #         self.motor_x.relative_move(2)
        # else:
        #     self.motor_x.start_relative_move(2)



        self.motor_y.home(direction=AXIS_MOTOR_SETTINGS['homing_direction'])
        self.motor_y.relative_move(offset_distance)
        self.motor_x.home(direction=AXIS_MOTOR_SETTINGS['homing_direction'])

        # Home twice to get a perfectly level table
        self.motor_x.relative_move(offset_distance)
        self.motor_y.home(direction=AXIS_MOTOR_SETTINGS['homing_direction'])
        self.motor_y.relative_move(offset_distance)
        self.motor_x.home(direction=AXIS_MOTOR_SETTINGS['homing_direction'])
        self.motor_x.relative_move(offset_distance)

        AXIS_MOTOR_SETTINGS['output_max'] = self.calculate_out_max()
        AXIS_MOTOR_SETTINGS['output_min'] = self.calculate_out_min() + 50

        self.homing = False

    def setup_motors(self):
        """
        Setup all instantiated motors with the predetermined settings
        :return: None
        """
        for motor in self.motors:
            motor.setCurrent(hold=AXIS_MOTOR_SETTINGS['hold_current'], run=AXIS_MOTOR_SETTINGS['run_current'], acc=AXIS_MOTOR_SETTINGS['acc_current'], dec=AXIS_MOTOR_SETTINGS['dec_current'])
            motor.setMaxSpeed(AXIS_MOTOR_SETTINGS['max_speed'])
            motor.setMinSpeed(AXIS_MOTOR_SETTINGS['min_speed'])
            motor.setMicroSteps(AXIS_MOTOR_SETTINGS['micro_steps'])
            motor.setThresholdSpeed(AXIS_MOTOR_SETTINGS['threshold_speed'])
            motor.setOverCurrent(AXIS_MOTOR_SETTINGS['over_current'])
            motor.setStallCurrent(AXIS_MOTOR_SETTINGS['stall_current'])
            motor.setAccel(AXIS_MOTOR_SETTINGS['accel'])
            motor.setDecel(AXIS_MOTOR_SETTINGS['decel'])
            motor.setLowSpeedOpt(AXIS_MOTOR_SETTINGS['low_speed_opt'])
            motor.setParam(LReg.CONFIG, 0x3688)


    def process_movement(self, x_val, y_val):
        """
        Process table movement based on a given value for the x and y axis
        :param x_val: Value corresponding to joysticks x axis. See Joystick for more info
        :param y_val: Value corresponding to joysticks y axis. See Joystick for more info
        :return: None
        """
        # Map the given x and y joystick value to position the motors can go to.
        x_mapped = int(self.map_val(value=x_val, in_min=1, in_max=-1, out_min=AXIS_MOTOR_SETTINGS['output_min'],
                                    out_max=AXIS_MOTOR_SETTINGS['output_max']))

        y_mapped = int(self.map_val(value=y_val, in_min=-1, in_max=1, out_min=AXIS_MOTOR_SETTINGS['output_min'],
                                    out_max=AXIS_MOTOR_SETTINGS['output_max']))

        # Construct two vectors one to hold where the motors currently are
        # and another holding where the motors need to go
        current_pos = np.array([self.motor_x.get_position(), self.motor_y.get_position()])
        mappings = np.array([x_mapped, y_mapped])

        # Calculate the scaling factor to determine how far away to set the new position.
        # The greater the distance to move the further the smaller the scaling factor
        scaling_factor = self.calculate_scaling_factor(mapping_vector=mappings, current_vector=current_pos)

        # Calculate the position where the motors need to go to.
        # Takes the difference between mapped position and where it currently is and divides by scaling factor.
        # Adds this final value to it's current position to ultimately decide where to go to
        calc_x_pos = int(current_pos[0] + ((x_mapped - current_pos[0]) / scaling_factor))
        calc_y_pos = int(current_pos[1] + ((y_mapped - current_pos[1]) / scaling_factor))

        if not self.motor_x.is_busy():  # If the x motor is not busy go to the calculated new position
            self.motor_x.go_to(calc_x_pos)

        if not self.motor_y.is_busy():  # If the y motor is not busy go to the calculated new position
            self.motor_y.go_to(calc_y_pos)

    def calculate_out_max(self) -> int:
        """
        Calculate the output maximum for mapping joystick input to moving the table.
        NOTE: This should only be run after the table has been homed and is level

        :rtype: integer
        :return: The calculated maximum output
        """
        pos = self.motor_x.get_position()
        min_output = self.calculate_out_min()

        max_val = ((pos - min_output) * 2) + min_output
        return max_val

    def calculate_out_min(self) -> int:
        """
        Calculate the output minimum used in process_movement

        :rtype: int
        :return: The calculated output minimum
        """
        return AXIS_MOTOR_SETTINGS['scaling_factor'] * AXIS_MOTOR_SETTINGS['micro_steps']

    def calculate_scaling_factor(self, mapping_vector, current_vector):
        """
        Calculate the scaling factor based on the current position and mapping vectors
        :param mapping_vector: Vector containing the mapped positions (target positions)
        :param current_vector: Vector containing the current positions
        :return: Integer representing the scaling factor
        """
        diff = mapping_vector - current_vector  # Get the difference vector
        mag = np.linalg.norm(diff)  # Get the magnitude of the difference vector

        # The greater the magnitude the greater distance the table needs to move
        if mag < 75:  # If the magnitude is less than 75 move in smaller increments
            return 8
        else:  # Needs to move a greater distance move in greater increments
            return 2


    def map_val(self, value, in_min, in_max, out_min, out_max):
        """
        Map a value from a given range to a new range.
        :param value: Value to map
        :param in_min: minimum value to map
        :param in_max: maximum value to map
        :param out_min: output minimum
        :param out_max: output maximum
        :return: Float of the mapped value in the output range
        """
        return (value - in_min) * (out_max - out_min) / (in_max - in_min) + out_min


    def check_movements(self):
        """
        Check to see if either of the axis motors are busy
        :rtype: bool
        :return: Whether either of the motors are currently moving/busy
        """
        return self.motor_x.isBusy() or self.motor_y.isBusy()


    def free_all(self):
        """
        Free all motors used by the table
        :return: None
        """
        for motor in self.motors:
            motor.free()


    def use_relative_move(self, x_val, y_val):
        """
        run the maze with only relative moves
        :param x_val: Value corresponding to joysticks x axis. See Joystick for more info
        :param y_val: Value corresponding to joysticks y axis. See Joystick for more info
        :return: None
        """
        if not self.motor_x.is_busy():
            self.motor_x.start_relative_move(-x_val)

        if not self.motor_y.is_busy():
            self.motor_y.start_relative_move(-y_val)


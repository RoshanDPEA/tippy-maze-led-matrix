from hardware.Table import Table
from hardware.GumBallRelease import GumBallReleaseMotor
from hardware.LidarSensor import LidarSensor
from pidev.Joystick import Joystick


TABLE = Table(x_axis_port=0, y_axis_port=1)
GUMBALL_RELEASE = GumBallReleaseMotor(motor_port=3, sensor_port=4, sensor_threshold=35)

JOYSTICK = Joystick(number=0, ssh_deploy=True)

TOP_RAMP_SENSOR = LidarSensor(port=0, threshold=85)  # first sensor on ramp down
LOWER_RAMP_SENSOR = LidarSensor(port=2, threshold=85)  # second sensor on ramp down

RESTART_GAME = True


def initialize_sensors():
    GUMBALL_RELEASE.reset_sensor()
    TOP_RAMP_SENSOR.reset()
    LOWER_RAMP_SENSOR.reset()


def refresh_all_sensors():
    TOP_RAMP_SENSOR.refresh_last_read()
    LOWER_RAMP_SENSOR.refresh_last_read()


def update_restart_game():
    global RESTART_GAME

    if TOP_RAMP_SENSOR.detected or LOWER_RAMP_SENSOR.detected:
        TOP_RAMP_SENSOR.reset()
        LOWER_RAMP_SENSOR.reset()

        RESTART_GAME = True


if __name__ == "__main__":
    global RESTART_GAME
    initialize_sensors()

    while True:
        if RESTART_GAME:
            TABLE.home()
            GUMBALL_RELEASE.release_gumball()
            RESTART_GAME = False

        refresh_all_sensors()
        update_restart_game()

        TABLE.process_movement(x_val=JOYSTICK.get_axis('x'), y_val=JOYSTICK.get_axis('y'))

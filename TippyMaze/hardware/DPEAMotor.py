from pidev.stepper import stepper

NEMA_17 = {
    'hold_current': 8,
    'run_current': 10,
    'acc_current': 10,
    'dec_current': 10,
    'max_speed': 525,
    'min_speed': 0,
    'micro_steps': 32,
    'threshold_speed': 1000,
    'over_current': 2000,
    'stall_current': 2187.5,
    'accel': 0x50,
    'decel': 0x10,
    'low_speed_opt': False,
    'slope': [0x562, 0x010, 0x01F, 0x01F]
    }

class DPEAMotor:
    def __init__(self, motor_port):
        """
        :param motor_port: port the DPEA gears motor goes on
        """
        self.motor = stepper(port=motor_port, speed=NEMA_17['max_speed'])

        self.setup_motor()
    
    def setup_motor(self):
        # self.motor.setCurrent(hold=NEMA_17['hold_current'],run=NEMA_17['run_current'],
        #                       acc=NEMA_17['acc_current'],dec=NEMA_17['dec_current'])
        self.motor.setMaxSpeed(NEMA_17['max_speed'])
        self.motor.setMinSpeed(NEMA_17['min_speed'])
        self.motor.setMicroSteps(NEMA_17['micro_steps'])
        self.motor.setThresholdSpeed(NEMA_17['threshold_speed'])
        self.motor.setOverCurrent(NEMA_17['over_current'])
        self.motor.setStallCurrent(NEMA_17['stall_current'])
        self.motor.setAccel(NEMA_17['accel'])
        self.motor.setDecel(NEMA_17['decel'])

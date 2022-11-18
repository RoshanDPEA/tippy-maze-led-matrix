from distutils.core import setup

setup(
    name="TippyMaze",
    author="Wade Varesio",
    version='1.0dev',
    packages=["hardware"],
    long_description="Package to handle software for the Tippy Maze Project",
    install_requires=["pyserial", "smbus", "adafruit-blinka", "adafruit-circuitpython-vl6180x", 'serial']
)

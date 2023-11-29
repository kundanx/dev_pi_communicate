from setuptools import find_packages
from setuptools import setup

setup(
    name='serial_motor_demo_msgs',
    version='0.0.0',
    packages=find_packages(
        include=('serial_motor_demo_msgs', 'serial_motor_demo_msgs.*')),
)

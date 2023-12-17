import os
from glob import glob
from setuptools import find_packages, setup

package_name = 'dev_pi_communicate'

setup(
    name=package_name,
    version='0.0.0',
    packages=find_packages(exclude=['test']),
    data_files=[
        (os.path.join('share', package_name, 'launch'), glob(os.path.join('launch', '*launch.[pxy][yma]*'))),
        ('share/ament_index/resource_index/packages',
            ['resource/' + package_name]),
        ('share/' + package_name, ['package.xml']),
    ],
   
    install_requires=['setuptools'],
    zip_safe=True,
    maintainer='kuns',
    maintainer_email='siwakotik89@gmail.com',
    description='TODO: Package description',
    license='TODO: License declaration',
    tests_require=['pytest'],
    entry_points={
        'console_scripts': [
            
            'publisher_node = dev_pi_communicate.publisher:main',
            'subscriber_node = dev_pi_communicate.subscriber:main',

            'static_baselink_laserframe_broadcaster = dev_pi_communicate.static_tf:main',

            'serial_comm_node = dev_pi_communicate.test:main',
            'camera_node = dev_pi_communicate.camera_node:main',
            'joy_node= dev_pi_communicate.joy_node:main',
            'teleop_key_node = dev_pi_communicate.teleop_key_node:main'
        ],
    },
)

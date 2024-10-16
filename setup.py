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
        # (os.path.join('share', package_name, 'config'), glob(os.path.join('config', '*'))),
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
            
            'publisher_node = scripts.publisher:main',
            'subscriber_node = scripts.subscriber:main',
            'vel_subscriber = scripts.vel_subscriber:main',

            'serial_bridge = scripts.serial_bridge:main',
            'serial_bluepill = scripts.serial_bluepill:main',
            'serial_rx_node = scripts.serial_rx_node:main',
            'serial_tx_node = scripts.serial_tx_node:main',
            'ds4_uart_node = scripts.ds4_uart_node:main',
            'imu_uart_node = scripts.imu_uart_node:main',
            'imu_uart_direct = scripts.imu_uart_direct:main',

            'ds4_node= scripts.ds4_node:main',
            'nav2_cmd_vel= scripts.nav2_cmd_vel:main',
            'camera_node = scripts.camera_node:main',
            
            'odom_baseLink_tf = transforms.odom_baseLink_tf:main',
            'baseLink_laserFrame_tf = transforms.baseLink_laserFrame_tf:main',
            'baseLink_imuLink_tf = transforms.baseLink_imuLink_tf:main',
            'map_baseLink_tf= transforms.map_baseLink_tf:main',
            'map_odom_tf = transforms.map_odom_tf:main'
        ],
    },
)

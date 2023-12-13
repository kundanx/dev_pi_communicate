from setuptools import find_packages, setup

package_name = 'dev_pi_communicate'

setup(
    name=package_name,
    version='0.0.0',
    packages=find_packages(exclude=['test']),
    data_files=[
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
            'talker_node = dev_pi_communicate.talker_node:main',
            'publisher_node = dev_pi_communicate.publisher:main',
            'subscriber_node = dev_pi_communicate.subscriber:main',
            'serial_comm_node = dev_pi_communicate.serial_comm_node:main',
            'camera_node = dev_pi_communicate.camera_recieve:main',
            'static_baselink_laserframe_broadcaster = dev_pi_communicate.static_tf:main',
            'frame_publisher = dev_pi_communicate.broadcaster:main',
            'joy_node= dev_pi_communicate.joy_node:main'
        ],
    },
)

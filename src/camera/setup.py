from setuptools import find_packages, setup

package_name = 'camera'

setup(
    name=package_name,
    version='0.0.0',
    packages=find_packages(exclude=['test']),
    data_files=[
        ('share/ament_index/resource_index/packages',
            ['resource/' + package_name]),
        ('share/' + package_name, ['package.xml']),
    ],
    install_requires=[
        'setuptools',
        'ultralytics',
        'supervision'
        ],
    zip_safe=True,
    maintainer='apil',
    maintainer_email='078bct017.apil@pcampus.edu.np',
    description='TODO: Package description',
    license='TODO: License declaration',
    tests_require=['pytest'],
    entry_points={
        'console_scripts': [
            'camera_node = camera.camera_node:main',
            'obj_track_node = camera.object_tracker:main'
        ],
    },
)

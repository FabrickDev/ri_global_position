from setuptools import find_packages, setup

package_name = 'ri_global_position'

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
    maintainer='faqisna-pm',
    maintainer_email='faqisna.pm@gmail.com',
    description='TODO: Package description',
    license='TODO: License declaration',
    extras_require={
        'test': [
            'pytest',
        ],
    },
    entry_points={
        'console_scripts': [
            'global_position = ri_global_position.fab_global_position:main',
            'vel_global_position = ri_global_position.fab_vel_global_position:main'
        ],
    },
)

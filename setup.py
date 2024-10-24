from setuptools import setup, find_packages

setup(
    name="my-air-monitor",
    version="0.1",
    packages=find_packages(),
    install_requires=[
        "py-air-control",
        "requests",
    ],
    entry_points={
        'console_scripts': [
            'my-air-monitor = my_air_monitor.monitor:main',
        ],
    },
)
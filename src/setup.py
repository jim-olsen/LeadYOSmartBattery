from setuptools import find_packages, setup

setup(
    name='lead_yo_battery',
    packages=find_packages(include=['LeadYOBattery']),
    version='0.0.1',
    description='A library to communicate with LeadYO Smart Cold Temp Batteries (including Chin batteries)',
    author='jim-olsen',
    license='Apache 2.0',
    install_requires=['bleak >= 0.19.5', 'asyncio >= 3.4.3']
)

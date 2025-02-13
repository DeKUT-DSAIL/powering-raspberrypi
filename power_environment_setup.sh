#!/bin/bash


sudo apt -y update
sudo apt -y full-upgrade

python -m venv power-env
source power-env/bin/activate


pip install --upgrade pip
pip install gpiod
pip install board
pip install smbus
pip install wheel
pip install cython
pip install numpy
pip install pandas
pip install gpiozero
pip install lgpio
pip install ipython
pip install adafruit-blinka
pip install adafruit-circuitpython-busdevice
pip install adafruit-circuitpython-register
pip install adafruit-circuitpython-ds3231
pip install adafruit-circuitpython-mcp3xxx

#!/bin/bash

cd powering-raspberrypi

source dsp-env/bin/activate

python power.py -w "((5,12),)"

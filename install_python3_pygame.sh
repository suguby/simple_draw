#!/usr/bin/env bash

sudo apt-get install python3-pip python3-dev libsdl-image1.2-dev libsdl-mixer1.2-dev libsdl-ttf2.0-dev libsdl1.2-dev libsmpeg-dev python3-numpy libportmidi-dev libswscale-dev libavformat-dev libavcodec-dev
sudo pip3 install -U hg+https://bitbucket.org/pygame/pygame
python3 simple_draw.py
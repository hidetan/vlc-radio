#!/bin/bash -xe
# -*- coding: utf-8 -*-
#

(
    cd ./vlc-3.0.17.3/build/
    make
)

source ./common.sh

exec ./vlc-3.0.17.3/build/bin/vlc-static \
     --verbose 2 \
     --playlist-tree \
     \
     --audio-filter normvol,compressor \
     --norm-buff-size 40 \
     --norm-max-level 10.0 \
     \
     --compressor-rms-peak 0.0 \
     --compressor-attack 50.0 \
     --compressor-release 200.0 \
     --compressor-threshold 0.0 \
     --compressor-ratio 20.0 \
     --compressor-knee 1.0 \
     --compressor-makeup-gain 0.0 \
     \
     --no-video \
     --preferred-resolution 144 \
     \
     --extraintf rc:http \
     --rc-host 0.0.0.0:9294 --rc-fake-tty \
     --http-host 0.0.0.0 --http-port 8080 --http-password raspberry \
     \
     ${playlist}



#!/bin/bash -xe
# -*- coding: utf-8 -*-
#

(
    cd ./vlc-3.0.12/build/
    make
)

source ./common.sh

exec ./vlc-3.0.12/build/bin/vlc-static \
     --verbose 2 \
     --playlist-tree \
     \
     --audio-filter normvol \
     --norm-buff-size 60 \
     --norm-max-level 1.8 \
     \
     --no-video \
     --preferred-resolution 144 \
     \
     ${playlist}



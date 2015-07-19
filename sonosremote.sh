#!/bin/bash

DIR=/home/pi/sonosremote

cd ${DIR}
python ${DIR}/sonosremote.py > ${DIR}/sonos.log 2>&1

#!/bin/sh
n=$RANDOM
screen -dmS server_screen$n sh -c "python3 start.py"
screen -S server_screen$n -r
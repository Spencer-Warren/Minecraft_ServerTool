#!/bin/sh
n=$RANDOM
screen -dmS server_screen$n sh -c "python /home/ec2-user/start.py"
screen -S server_screen$n -r
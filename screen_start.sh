screen -dmS server_screen sh -c "python /home/ec2-user/start.py; exec bash"
screen -S server_screen -r
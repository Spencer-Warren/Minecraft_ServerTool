# Minecraft_ServerTool
Personal project to have an easy way of managing and launching different minecraft server variants

This is a tool that sits on an linux AWS server that allows basic management of diffrent minecraft server versions. 
This tool creates and issues commands to a screen session in order to keep the minecraft server running without the putty/ssh screen open.
Simply issue a stop command to the minecraft server and it will properly shut it down and close the screen once it is done.

The file structure for this tool should be as follows:

home/ec2-user
|-- server1
|   |-- server.jar
|   `-- world
|-- server2
|   |-- server.jar
|   `-- world
|-- screen-start.sh
`-- start.py

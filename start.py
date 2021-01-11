#!/usr/bin/env python3
import os
import sys

def server_checker():
    """
    Looks for directories with a "server.jar" file in it 
    then saves it and passes it the next function
    """
    server_names = []
    for dr in os.listdir("."):
        if os.path.isdir(dr):
            for file in os.listdir(dr):
                if file == "LaunchServer.sh":
                    server_names.append(dr)

    server_name = server_names[menu(server_names, "Here are all the current servers:")]
    if server_name == "Exit":
        quit()

    check_eula_properties(server_name)
    server_options(server_name)

def menu(options,pre=""):
    """
    Standardized menu function
    Takes options in as list
    Takes optional pre text
    returns option picked
    """
    print("-"*25)
    if pre != "":
        print(pre +"\n")
    options.append("Exit")
    for i, name in enumerate(options):
        print("{}: {}".format(i+1, name))
    print("-"*25)
    choice=0
    options = [i+1 for i,_ in enumerate(options)]
    while choice not in options:
        choice=input("Select one:\n")
        try:
            choice = int(str(choice))
        except Exception:
            print("Enter int of choice")
    if choice == len(options) + 1:
        quit()
    return(choice - 1)

def check_eula_properties(server_name):
    """
    Checks if eula.txt and server.properties exist in the selected folder
    """
    file_list=[]
    for a, b, files in os.walk(server_name):
        file_list.append(files)
    if "server.properties" not in file_list[0]:
        create_properties(server_name)
    if "eula.txt" in file_list[0]:
            eula = open(os.path.join(server_name, "eula.txt"),"r")
            lines = eula.readlines()
            if len(lines) > 1:
                if "eula=true" not in lines[1]:
                    create_eula(server_name)
            else:
                if lines[0] !="eula=true\n":
                    create_eula(server_name)
    else:
        create_eula(server_name)

def create_eula(server_name):
    """
    Create Eula.txt file and set it to true
    """
    with open(os.path.join(server_name, "eula.txt"),"w") as file:
        file.write("eula=true")
    print("Eula.txt not detected or false, creating...")

def create_properties(server_name):
    """
    reads the default properties file and
    writes a new one in the selected directory
    """
    with open(os.path.join("default.properties"),"r") as file:
        properties = file.readlines()
    with open(os.path.join(server_name, "server.properties"),"w") as file:
        file.writelines(properties)
    print("Server.properties not detected, creating...")

def server_options(server_name):
    """
    Options to launch server 
    or change options
    """
    launch_options = ["Launch","Change world", "Change port", "Change Message of the Day", "Change player limit", "Change Selected Server"]
    launch_choice = menu(launch_options, "You've selected {}, changing dir to that".format(server_name))
    if launch_choice == 0:
        launch_server(server_name)
    else:
        options(server_name, launch_choice, launch_options)
        server_options(server_name)

def options(server_name,option,options):
    """
    Function promts the user on which setting thay want to change
    """
    print("You choose to {}".format(options[option].lower()))
    option -= 1
    if option < 4:
        properties_names = ["level-name=","server-port=","motd=","max-players="]
        internal_name = properties_names[option]
        if option == 0:
            worlds = detect_worlds(server_name)
            new_text = worlds[menu(worlds,"Choose a new world to load:")]
        else:
            new_text = input("{} ".format(properties_names[option]))
        change_option(server_name, internal_name, new_text)
    else:
        server_checker()
        
def detect_worlds(server_name):
    """
    Detect all world files in current server by serching for level.dat files
    """
    worlds = []
    for _, folders, _ in os.walk(server_name):
        for folder in folders:
            for _, _, files in os.walk(os.path.join(server_name,folder)):
                for file in files:
                    if file == "level.dat":
                        worlds.append(folder)
                        break
    return worlds

def change_option(server_name, internal, new_text):
    """
    Function takes what option was choosen to change and changes it
    """
    file = open(os.path.join(server_name, "server.properties"), "r")
    lines = file.readlines()
    for i, line in enumerate(lines):
        if line[0:len(internal)] == internal:
            lines[i] = internal + str(new_text) + "\n"
            print("Changing line")
    file.close()
    file = open(os.path.join(server_name, "server.properties"), "w")
    file.writelines(lines)
    file.close()
    print("Done")
    server_options(server_name)


def launch_server(server_name):
    """
    Launches the server
    """
    os.system("cd {}; ./LaunchServer.sh".format(server_name))
    os.system("exit")

if __name__ == "__main__":
    user = str(os.system("$USER"))
    os.system("cd {}".format(os.path.join("home",user)))
    server_checker()
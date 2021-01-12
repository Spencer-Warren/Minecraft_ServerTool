#!/usr/bin/env python3
import os
import sys

def server_checker():
    """
    Looks for directories with a jar file in it and allows user to choose one
    Returns: 
        Chosen server name
    """
    server_names = []
    for direc in os.listdir("."):
        if os.path.isdir(direc):
            for file in os.listdir(direc):
                if "server" in file and ".jar" in file:
                    server_names.append(direc)
    #user picks server they wish to change/run
    server_name = server_names[menu(server_names, "Here are all the current servers:")]
    if server_name == "Exit":
        sys.exit()
    return server_name

def menu(options,pre=""):
    """
    Standardized menu function
    Args:
        options as a list
        String to display before options
    Returns: 
        The index of the option picked
    """
    print("-"*25)
    if pre != "":
        print(pre +"\n")
    options.append("Enter q to Quit")
    for i, name in enumerate(options):
        print("{}: {}".format(i+1, name))
    print("-"*25)
    choice=0
    options = [i+1 for i,_ in enumerate(options)]
    while choice not in options:
        choice=input("Select one:\n")
        try:
            if choice =="q":
                break
            choice = int(str(choice))
        except Exception:
            print("Enter int of choice")
    if choice == "q":
        return "quit"
    return choice - 1

def check_eula_properties(server_name):
    """
    Checks if eula.txt and server.properties exist in the selected directory
    Args:
        Chosen server name
    """
    file_list=[]
    for _, _, files in os.walk(server_name):
        file_list.append(files)
    if "server.properties" not in file_list:
        create_properties(server_name)
    if "eula.txt" in file_list[0]:
        eula = open(os.path.join(server_name, "eula.txt"),"r")
        lines = eula.readlines()
        if len(lines) > 1:
            if "eula=true" not in lines[1]: #checking if eula is set to true
                create_eula(server_name)
        else:
            if lines[0] !="eula=true\n":
                create_eula(server_name)
    else:
        create_eula(server_name)

def create_eula(server_name):
    """
    Create Eula.txt file and set it to true
    Args:
        Chosen server name
    """
    with open(os.path.join(server_name, "eula.txt"),"w") as file:
        file.write("eula=true")
    print("Eula.txt not detected or false, creating...")

def create_properties(server_name):
    """
    Reads the default properties file and writes a new one in the selected directory
    Args:
        Chosen server name
    """
    print("Server.properties not detected, creating...")
    with open(os.path.join("default.properties"),"r") as file:
        properties = file.readlines()
    with open(os.path.join(server_name, "server.properties"),"w") as file:
        file.writelines(properties)

def server_options(server_name):
    """
    Gives user choice to change server parameters or to launch the selected server
    Args:
        Chosen server name
    Return:
        Users choice as string
    """
    launch_options = ["Launch","Change world", "Change port", "Change Message of the Day", "Change player limit", "Change Selected Server"]
    launch_choice = menu(launch_options, "You've selected {}, changing dir to that".format(server_name))
    if launch_choice == 0:
        launch_server(server_name)
    else:
        options(server_name, launch_choice, launch_options)
    return launch_choice

def options(server_name,option,options):
    """
    Function promts the user on which setting thay want to change then sends to change_option()
    Args:
        Chosen server name as string
        Chosen option as string
        list of options as a list
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
    Args:
        Chosen server name as string
    Return:
        worlds detected as list
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
    Function takes what option was choosen to change and writes it to the server.properties file
    Args:
        Chosen server name as string
        Internal names for options as list
        new text to replace the selected option as string
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

def launch_server(server_name):
    """
    Launches the server using selected server directory,
    max ram setting from options.txt and jar from other function
    Args:
        Chosen server name as string
    """
    jar = forge_test(server_name)
    os.system("cd {}; java -Xmx{} -jar {}".format(server_name, sys.argv[1], jar))
    os.system("exit")  #exits screen when jar is closed

def forge_test(server_name):
    """
    looks for .jar files in selected directory and returns one
    Args:
        Chosen server name as string
    Return:
        Name of jar file to use to launch server as string
    """
    jars = []
    for _, _, files in os.walk(server_name):
        for file in files:
            if ".jar" in file:
                jars.append(file)
                break
    for jar in jars:
        if "forge" or "FTB" in jar:
    # FTB and forge use custom jar files and you launch them instead of the vanilla mojang jar
            print("Detected Forge or FTB jar using that")
            return jar
    return jars[0]

def main():
    """
    Main body of program
    Passes selected server name to other functions
    """
    server_name = server_checker()
    check_eula_properties(server_name)
    quit_var = 0
    while quit_var != "quit": #allows changing of multiple options and quick exit
        quit_var = server_options(server_name)

if __name__ == "__main__":
    main()

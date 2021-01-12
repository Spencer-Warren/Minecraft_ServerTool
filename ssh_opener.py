import os
import random
def option_parse():
    """
    Parse options.txt to be used in the server tool
    returns: dictionary with options outlined in options.txt
    """
    file = open("options.txt")
    lines = file.readlines()
    options = {}
    for line in lines:
        line = line.split("=")
        options[line[0]] = line[1].rstrip()
    file.close()
    return options

def open_ssh(options):
    """
    Opens ssh and screen session simulataniously with specifications given in option_parse()
    """
    cmd = "screen -dmS server_screen{num} sh -c 'python3 server_tool.py {arg}'; screen -S server_screen{num} -r".format(num = random.randint(1,1000), arg = options["Max_Ram"])
    os.system("ssh -i ~/.ssh/{} {}@{} -t {}".format(options["Private_Key_Name"], options["AWS_Username"], options["Host_Name"], cmd))

def main():
    options = option_parse()
    open_ssh(options)

if __name__ =="__main__":
    main()
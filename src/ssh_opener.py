import os
import random
def option_parse():
    """
    Parse options.txt to be used in the server tool
    Returns:
        Dictionary with options outlined in options.txt
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
    Opens ssh and screen session simultaneously with specifications given in option_parse()
    Args:
        options from options.txt file as list
    """
    cmd = "screen -dmS server_screen{num} sh -c 'python3 server_tool.py {arg}'; screen -S server_screen{num} -r"
    cmd = cmd.format(num = random.randint(1,1000), arg = options["Max_Ram"])
    ssh = "ssh -i ~/.ssh/{} {}@{} -t {}"
    ssh = ssh.format(options["Private_Key_Name"], options["AWS_Username"], options["Host_Name"], cmd)
    os.system(ssh)

def main():
    """
    Pass options from one function to the other
    """
    options = option_parse()
    open_ssh(options)

if __name__ =="__main__":
    main()

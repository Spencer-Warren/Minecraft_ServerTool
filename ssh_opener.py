import os
import random
def option_parse():
    file = open("options.txt")
    lines = file.readlines()
    options = {}
    for line in lines:
        line = line.split("=")
        options[line[0]] = line[1].rstrip()
    file.close()
    return options

def open_ssh(options):
    cmd = "screen -dmS server_screen{num} sh -c 'python3 server_tool.py; exec bash'; screen -S server_screen{num} -r".format(num = random.randint(1,1000))
    os.system("ssh -i ~/.ssh/{} {}@{} -t {}".format(options["Private_Key_Name"], options["AWS_Username"], options["Host_Name"], cmd))

def main():
    options = option_parse()
    open_ssh(options)

if __name__ =="__main__":
    main()
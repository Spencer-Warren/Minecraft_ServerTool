import os
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
    os.system("ssh -i ~/.ssh/{} {}@{} python3 server_tool.py".format(options["Private_Key_Name"], options["AWS_Username"], options["Host_Name"]))

def main():
    options = option_parse()
    open_ssh(options)

if __name__ =="__main__":
    main()
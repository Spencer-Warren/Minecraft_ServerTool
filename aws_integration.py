import boto3
from ssh_opener import option_parse

def menu(options,pre=""):
    """
    Standardized menu function
    Args: 
        Possible options in as list
        Optional text to display before choices
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

def write_setting(key, value):
    """
    Writes given option to options.txt file
    Args:
        Key for option ex. VPC_id
        Value to write to setting
    """
    options = option_parse()
    options[key] = value
    lines = []
    for key in options:
        lines.append(key+"="+options[key]+"\n")
    file = open("options.txt","w")
    file.writelines(lines)
    file.close()
    return options

def list_instances(vpc):
    instances = []
    for i in vpc.instances.all():
        try:
            for tag in i.tags:
                if tag['Key'] == "Name":
                    instances.append(tag["Value"])
        except TypeError:
            index = len(instances) + 1
            instance_ids = [i.id for i in ec2.instances.all()]
            instances.append(instance_ids[index])
    return instances

def main():
    if option_parse()["VPC_id"] == "":
        vpc = input("Please enter your vpc id:\n")
        write_setting("VPC_id", vpc)
        vpc = ec2.Vpc(vpc)
    else:
        vpc = ec2.Vpc(option_parse()["VPC_id"])
        print("vpc accepted...")
    for i in list_instances(vpc):
        print(i)

if __name__ == "__main__":
    global ec2
    ec2 = boto3.resource("ec2")
    main()
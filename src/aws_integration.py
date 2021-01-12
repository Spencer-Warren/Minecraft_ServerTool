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
    options = [i+1 for i, _ in enumerate(options)]
    while choice not in options:
        choice=input("Select one:\n")
        try:
            if choice == "q" or choice == "":
                return choice
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
        lines.append(key + "=" + options[key] + "\n")
    file = open("options.txt", "w")
    file.writelines(lines)
    file.close()

def list_instances(vpc):
    """
    Grabs instance name tags and ids
    Args:
        AWS VPC id
    if an instance doesnt have a tag with a name,
    it grabs the instance id
    """
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
    return instances, instance_ids

def choose_instance(vpc):
    """
    Allows user to choose instance from list obtained from list_instance
    Args:
        AWS VPC id
    If user hits enter the default instance is selected
    """
    instances_names, instance_ids = list_instances(vpc)
    default_instance = option_parse()["Default_instance"]
    for i, instance in enumerate(instances_names):
        if instance == default_instance:
            instances_names[i] = instance + " (Default)"
    instance = menu(instances_names, "Choose an instance or hit enter to choose default")
    if instance == "":
        print("Yes")
        instance = default_instance
    if instance != default_instance:
        choice = input("Would you like to make {} your default instance? (y/n)\n")
        if choice == "y":
            write_setting("Default_instance", instance)
    return instance

def vpc_init():
    """
    gets vpc id or asks for it from the user
    Return:
        AWS VPC id
    """
    if option_parse()["VPC_id"] == "":
        vpc = input("Please enter your vpc id:\n")
        write_setting("VPC_id", vpc)
        print("vpc id written to settings...")
        return ec2.Vpc(vpc)
    else:
        print("vpc id accepted...")
        return ec2.Vpc(option_parse()["VPC_id"])        

def main():
    vpc = vpc_init()
    instance = choose_instance(vpc)

if __name__ == "__main__":
    global ec2
    ec2 = boto3.resource("ec2")
    main()

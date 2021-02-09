import boto3
from ssh_opener import option_parse

ec2 = boto3.resource("ec2")

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
    if an instance dosent have a tag with a name,
    it grabs the instance id
    """
    instances = []
    instance_ids = [i.id for i in ec2.instances.all()]
    for i in vpc.instances.all():
        try:
            for tag in i.tags:
                if tag['Key'] == "Name":
                    instances.append(tag["Value"])
        except TypeError:
            if len(instances) > 0:
                index = len(instances) + 1
            else:
                index = 0
            instances.append(instance_ids[index])
    return instances, instance_ids

def choose_instance(vpc, instance_names, instance_ids, default_instance):
    """
    Allows user to choose instance from list obtained from list_instance
    Args:
        AWS VPC id
    If user hits enter the default instance is selected
    """
    instance_descriptions = []
    for i, instance in enumerate(instance_ids):
        if instance == default_instance:
            instance_descriptions.append(instance + " (Default)")
    instance = menu(instance_names, "Choose an instance or hit enter to choose default")
    if instance == "":
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
    try:
        print("Requesting default vpc id")
        vpc = list(ec2.vpcs.filter(Filters=[{'Name': 'isDefault', 'Values': ['true']}]))[0]
        print(vpc.id)
    except Exception as e:
        print(e)
    return ec2.Vpc(vpc.id)
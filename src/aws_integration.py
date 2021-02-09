import boto3
import sys
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
            choice = int(str(choice))
        except TypeError:
            if choice.lower() == "q":
                sys.exit(0)
            print("Enter int of choice")
        except ValueError:
            return ""
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
        lines.append(key + "=" + str(options[key]) + "\n")
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
    instance_ids = [instance.id for instance in ec2.instances.all()]
    for instance in vpc.instances.all():
        try:
            for tag in instance.tags:
                if tag['Key'] == "Name":
                    instances.append(tag["Value"])
        except TypeError:
            instances.append(instance.id)
    return instances, instance_ids

def choose_instance(vpc, instance_names, instance_ids, default_instance):
    """
    Allows user to choose instance from list obtained from list_instance
    Args:
        AWS VPC id
    If user hits enter the default instance is selected
    """
    instance_descriptions = []
    for i, instance in enumerate(instance_names):
        if instance == default_instance:
            instance_descriptions.append(instance + " (Default)")
        instance_descriptions.append(instance)
    instance_index = menu(instance_descriptions, "Choose an instance or hit enter to choose default")
    if instance_index == "":
        instance = default_instance
        return instance
    instance_name = instance_names[instance_index]
    instance_id = instance_ids[instance_index]
    if instance != default_instance:
        choice = input("Would you like to make {} your default instance? (y/n)\n".format(instance_name))
        if choice.lower() == "y":
            write_setting("Default_instance", instance_name)
    return instance_name, instance_id

def vpc_init():
    """
    gets vpc id or asks for it from the user
    Return:
        AWS VPC id
    """
    try:
        print("Requesting default vpc id")
        vpc = list(ec2.vpcs.filter(Filters=[{'Name': 'isDefault', 'Values': ['true']}]))[0]
    except Exception as e:
        print(e)
    return ec2.Vpc(vpc.id)
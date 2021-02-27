import boto3
import sys
from ssh_opener import option_parse

ec2 = boto3.resource("ec2")

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
        else:
            instance_descriptions.append(instance)
    instance_index = menu(instance_descriptions, "Choose an instance or hit enter to choose default")
    if instance_index == "":
        instance = default_instance
        return instance
    instance_name = instance_names[instance_index]
    instance_id = instance_ids[instance_index]
    if instance_name != default_instance:
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

# def create_key()
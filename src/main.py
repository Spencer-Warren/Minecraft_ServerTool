from ssh_opener import vpc_init, choose_instance, list_instances
from aws_integration import option_parse, open_ssh

def main():
    vpc = vpc_init()
    options = option_parse()
    instance_names, instance_ids = list_instances(vpc)
    default_instance = options["Default_instance"]
    instance = choose_instance(vpc, instance_names, instance_ids, default_instance)
    open_ssh(options)

if __name__ == "__main__":
    main()
#!/usr/bin/env python3
import boto3
import json

def get_hosts():
    ec2 = boto3.client('ec2', region_name='us-east-1')
    instances = ec2.describe_instances(Filters=[
        {'Name': 'tag:Role', 'Values': ['App']},
        {'Name': 'instance-state-name', 'Values': ['running']}
    ])
    hosts = []
    for res in instances['Reservations']:
        for inst in res['Instances']:
            hosts.append(inst['PublicIpAddress'])
    return hosts

def main():
    hosts = get_hosts()
    inventory = {
        'app_servers': {
            'hosts': hosts,
            'vars': {
                'ansible_user': 'ec2-user',
                'ansible_ssh_private_key_file': '/home/ubuntu/Key.pem'
            }
        }
    }
    print(json.dumps(inventory))

if __name__ == "__main__":
    main()


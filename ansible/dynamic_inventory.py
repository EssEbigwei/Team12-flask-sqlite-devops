#!/usr/bin/env python3
import boto3
import json
import os
import sys

def get_aws_session():
    """Create AWS session with explicit error handling"""
    try:
        return boto3.Session(
            aws_access_key_id=os.environ.get('AWS_ACCESS_KEY_ID'),
            aws_secret_access_key=os.environ.get('AWS_SECRET_ACCESS_KEY'),
            region_name=os.environ.get('AWS_REGION', 'us-east-2')
        )
    except Exception as e:
        sys.stderr.write("ERROR: Failed to create AWS session. Check your credentials and environment variables.\n")
        sys.stderr.write(f"Details: {str(e)}\n")
        sys.exit(1)

def get_hosts(ec2_client):
    """Get EC2 instances with better error reporting"""
    try:
        response = ec2_client.describe_instances(Filters=[
            {'Name': 'tag:Role', 'Values': ['App']},
            {'Name': 'instance-state-name', 'Values': ['running']}
        ])
        return [inst['PublicIpAddress'] 
               for res in response['Reservations'] 
               for inst in res['Instances'] 
               if 'PublicIpAddress' in inst]
    except Exception as e:
        sys.stderr.write("ERROR: Failed to fetch EC2 instances. Possible causes:\n")
        sys.stderr.write("- Missing permissions (ec2:DescribeInstances)\n")
        sys.stderr.write("- Wrong region specified\n")
        sys.stderr.write(f"Details: {str(e)}\n")
        return []

def main():
    # Initialize with empty inventory in case of failures
    inventory = {'_meta': {'hostvars': {}}, 'app_servers': {'hosts': []}}
    
    try:
        session = get_aws_session()
        ec2 = session.client('ec2')
        hosts = get_hosts(ec2)
        
        if hosts:
            inventory = {
                'app_servers': {
                    'hosts': hosts,
                    'vars': {
                        'ansible_user': os.environ.get('ANSIBLE_USER', 'ec2-user'),
                        'ansible_ssh_private_key_file': os.environ.get(
                            'ANSIBLE_SSH_PRIVATE_KEY_FILE', 
                            '/home/ubuntu/Key.pem'
                        )
                    }
                }
            }
    except Exception as e:
        sys.stderr.write(f"CRITICAL ERROR: {str(e)}\n")
    
    print(json.dumps(inventory))

if __name__ == "__main__":
    main()
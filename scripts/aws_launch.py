import sys
import os
import hashlib
import datetime
import boto3
import time

num_instances = int(sys.argv[1])
real_run = eval(sys.argv[2])
ip_list = sys.argv[3]

# launch many spot blocks
ec2 = boto3.resource('ec2')
client = boto3.client('ec2')


# system parameters that won't change for these experiments
ami_id = 'ami-0170dbeefcf8a0d9f'
product_description = 'Linux/UNIX'
instance_type = 't3.micro'
region = 'us-east-2'
security_group = 'launch-wizard-1'
key_name = 'slangows'

try:
    os.remove(ip_list)
except OSError:
    pass

f = open(ip_list, 'a')
for i in range(0, num_instances, 128):
    this_instances = min(num_instances-i,128)
    print(this_instances)
    h = hashlib.sha256()
    h.update(str(datetime.datetime.now()).encode('utf-8'))
    client_token = h.hexdigest()
    response = client.run_instances(
        ImageId=ami_id,
        InstanceType=instance_type,
        KeyName='slangows',
        MaxCount=this_instances,
        MinCount=this_instances,
        Monitoring={
        'Enabled': False
        },
        Placement={
            'AvailabilityZone': region + 'c',
        },
        SecurityGroupIds=[
            security_group,
        ],
        ClientToken=client_token,
        DryRun=not real_run,
        InstanceInitiatedShutdownBehavior='stop',
        TagSpecifications=[
            {
                'ResourceType': 'instance',
                'Tags': [
                    {
                        'Key': 'project',
                        'Value': 'Lightning'
                    },
                    {
                        'Key': 'owner',
                        'Value': 'slangows',
                    }
                ]
            },
        ]
    )

    ips = []
    for inst in response['Instances']:
        ips.append(inst['NetworkInterfaces'][0]['PrivateIpAddress'])

    ips = sorted(ips)
    for ip in ips:
        f.write(ip + '\n')
f.close()

import sys
import boto3
import json

ip_list = "ip.list"


regions = ['us-east-2']

def tagged(instance):
    tags = instance['Tags']
    for t in tags:
        if t['Key'] == 'Name':
            return True
    return False

for r in regions:

    ec2 = boto3.client('ec2', region_name=r)

    response = ec2.describe_instances(
            DryRun=False,
    )

    f = open(ip_list, 'w')
    json.dump(response, f, default=str)
    f.close()

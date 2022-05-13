import sys
import boto3

ip_list = sys.argv[1]

ips = []
with open(ip_list) as f:
    lines = f.readlines()
    for line in lines:
        ips.append(line.rstrip('\n'))


def tagged(instance):
    tags = instance['Tags']
    for t in tags:
        if t['Key'] == 'Name':
            return True
    return False

def chunks(l, n):
    """Yield successive n-sized chunks from l."""
    for i in range(0, len(l), n):
        yield l[i:i + n]

regions = ['us-east-2', 'us-east-1']

for r in regions:
    session = boto3.Session(profile_name='mit')
    ec2 = session.client('ec2', region_name='us-east-2')

    response = ec2.describe_instances()

    instance_ids = []

    for resp in response['Reservations']:
        for inst in resp['Instances']:
            if inst['State']['Name'] == 'running' and inst['KeyName'] == 'slangows':
                if not tagged(inst):
                    if inst['NetworkInterfaces'][0]['PrivateIpAddress'] in ips:
                        instance_ids.append(inst['InstanceId'])
    print(f"Killing {len(instance_ids)} servers")
    for ids in chunks(instance_ids, 100):
        response = ec2.terminate_instances(
            InstanceIds=ids
        )

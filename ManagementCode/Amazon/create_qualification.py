import boto3
from pprint import pprint
#from boto3 import client
client = boto3.client(service_name ='sqs')
#mturk = boto3.client('mturk')
mturk = boto3.client(service_name = 'mturk', region_name='us-east-1')

qualification  = mturk.create_qualification_type(
    Name='Auto assigned when HIT is accepted',
    Description='Accept the HIT and you will granted the qualification',
    QualificationTypeStatus='Active',
    AutoGranted=True,
)

pprint(qualification)




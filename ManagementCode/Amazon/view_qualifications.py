import boto3
from pprint import pprint
#from boto3 import client

class UpdateQualification():
    mturk = boto3.client(service_name = 'mturk', region_name='us-east-1')
    response = mturk.list_qualification_types(
        Query='Auto',
        MustBeRequestable=True,
        MustBeOwnedByCaller=True,)
    for qual in response['QualificationTypes']:
        print (qual['QualificationTypeId'])





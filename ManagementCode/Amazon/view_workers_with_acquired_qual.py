import boto3
from boto.mturk.connection import MTurkConnection
from boto.mturk.question import ExternalQuestion
from boto.mturk.price import Price
import json
from pprint import pprint
HOST = 'mechanicalturk.sandbox.amazonaws.com'
#mturk = boto3.client(service_name = 'mturk',
#                                          endpoint_url =
#                                          'https://mturk-requester-sandbox.us-east-1.amazonaws.com')



mturk = boto3.client(service_name = 'mturk',region_name='us-east-1')
#hits = mturk.list_hits()


response = mturk.list_qualification_types(
            Query='Auto',
            MustBeRequestable=True,
            MustBeOwnedByCaller=True,)
for qual in response['QualificationTypes']:
    qual_id = (qual['QualificationTypeId'])
    workers = mturk.list_workers_with_qualification_type(QualificationTypeId=qual_id)
    for worker in workers['Qualifications']:
        print (worker['WorkerId'])
    marker = workers['NextToken']
    print(marker)
    if marker :
        while True:
            workers  = mturk.list_workers_with_qualification_type(QualificationTypeId=qual_id, NextToken=marker)
            for worker in workers['Qualifications']:
                print (worker['WorkerId'])
            if 'NextToken' in workers:
                marker = workers['NextToken']
            else:
                break

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

connection = MTurkConnection(aws_access_key_id='YOURKEY',
                             aws_secret_access_key='YOURSECRETKEY',
                             host=HOST)

mturk = boto3.client(service_name = 'mturk',region_name='us-east-1')


#hits = mturk.list_hits()
# Get Qualification ID
response = mturk.list_qualification_types(
            Query='Auto',
            MustBeRequestable=True,
            MustBeOwnedByCaller=True,
)

QualID = ''
if response['QualificationTypes'][0]:
    QualID = response['QualificationTypes'][0]['QualificationTypeId']
else:
    print("There is no qualification, please create one first")
    raise()


print(QualID)

workers =mturk.list_workers_with_qualification_type(QualificationTypeId=QualID)

for worker in workers['Qualifications']:
    print (worker['WorkerId'])
    mturk.disassociate_qualification_from_worker(
        WorkerId=worker['WorkerId'],
            QualificationTypeId=QualID,
            Reason='Starting a new batch, you can now take part in the  experiment again.'
    )
marker = workers['NextToken']
if marker :
    while True:
        workers =mturk.list_workers_with_qualification_type(QualificationTypeId=QualID, NextToken=marker)
        for worker in workers['Qualifications']:
            print (worker['WorkerId'])
            mturk.disassociate_qualification_from_worker(
                WorkerId=worker['WorkerId'],
                QualificationTypeId=QualID,
                Reason='Starting a new batch, you can now take part in the  experiment again.'
            )
        if 'NextToken' in workers:
            marker = workers['NextToken']
        else:
            break


print(marker)


#print(type(hits))
#pprint(hits)
#for hit in hits['HITs']:
#    print("HIT {} with HTITID {}".format(hit['HITId'], hit['HITTypeId']))
#for hit in hits:
#    print(type(hit))
#    print(hit["ResponseMetadata"])
#qualifications = mturk.list_qualification_requests()
#pprint(qualifications)

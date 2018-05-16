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


hits = mturk.list_hits()

print(type(hits))
#pprint(hits)


for hit in hits['HITs']:
    print("HIT {} with HTITID {}".format(hit['HITId'], hit['HITTypeId']))
    response = mturk.list_assignments_for_hit(
            HITId=hit['HITId'],
            AssignmentStatuses=[
                        'Submitted',
                    ]
    )
    pprint(response)
#for hit in hits:
#    print(type(hit))
#    print(hit["ResponseMetadata"])
#qualifications = mturk.list_qualification_requests()
#pprint(qualifications)

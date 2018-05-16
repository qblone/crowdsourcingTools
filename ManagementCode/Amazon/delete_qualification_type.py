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
# Get all qualifications
response = mturk.list_qualification_types(
        Query='Auto',
        MustBeRequestable=True,
        MustBeOwnedByCaller=True,
)


qualification = response['QualificationTypes'][0]['QualificationTypeId']

print("Deleting qualificationType {}".format(qualification))

response = mturk.delete_qualification_type(
        QualificationTypeId=qualification

)


pprint(response)

#print(type(hits))
#pprint(hits)
#for hit in hits['HITs']:
#    print("HIT {} with HTITID {}".format(hit['HITId'], hit['HITTypeId']))
#for hit in hits:
#    print(type(hit))
#    print(hit["ResponseMetadata"])
#qualifications = mturk.list_qualification_requests()
#pprint(qualifications)

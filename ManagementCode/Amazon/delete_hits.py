import boto3
from boto.mturk.connection import MTurkConnection
from boto.mturk.question import ExternalQuestion
from boto.mturk.price import Price
import json
from pprint import pprint
from datetime import datetime
HOST = 'mechanicalturk.sandbox.amazonaws.com'
#mturk = boto3.client(service_name = 'mturk',
#                                          endpoint_url =
#                                          'https://mturk-requester-sandbox.us-east-1.amazonaws.com')

connection = MTurkConnection(aws_access_key_id='YOURKEY',
                             aws_secret_access_key='YOURSECRETKEY',
                             host=HOST)

mturk = boto3.client(service_name = 'mturk',region_name='us-east-1')


hits = mturk.list_hits()

print(type(hits))
#pprint(hits)
for hit in hits['HITs']:
    hit_id =hit['HITId']
    response = mturk.list_assignments_for_hit(
        HITId=hit_id,
        AssignmentStatuses=['Submitted'], )
    assignments = response['Assignments']
    print ('The number of submitted assignments is {}'.format(len(assignments)))
    for assignment in assignments:
        WorkerId = assignment['WorkerId']
        assignmentId = assignment['AssignmentId']
        answer = assignment['Answer']
        print ('The Worker with ID {} submitted assignment {} and gave the answer {}'.format(WorkerId,assignmentId, answer))
        # Approve the Assignment
        print ('Approve Assignment {}'.format(assignmentId))
        mturk.approve_assignment(
            AssignmentId=assignmentId,
            RequesterFeedback='good',
            OverrideRejection=False
        )
for hit in hits['HITs']:
    print("Deleting {} HIT".format(hit['HITId']))
    mturk.update_expiration_for_hit(
            HITId=hit['HITId'],
            ExpireAt=datetime(2015, 1, 1)
    )


   # mturk.update_hit_review_status(HITId=hit['HITId'],Revert=True)
    mturk.delete_hit(HITId=hit['HITId'])
#for hit in hits:
#    print(type(hit))
#    print(hit["ResponseMetadata"])
#qualifications = mturk.list_qualification_requests()
#pprint(qualifications)

'''
This script gets the workers which has completed the task 

'''
import boto3
from boto.mturk.connection import MTurkConnection
from boto.mturk.question import ExternalQuestion
from boto.mturk.price import Price
import json
from pprint import pprint
HOST = 'mechanicalturk.sandbox.amazonaws.com'
#mturk = boto3.client(service_name = 'mturk',region ='us-east-1')

mturk = boto3.client(service_name = 'mturk', region_name='us-east-1')




hits = mturk.list_hits()

print(type(hits.keys()))
#pprint(hits)
print(hits['NextToken'])
print(len(hits))
for hit in hits['HITs']:
    #print(hit['HITId'])
    response = mturk.list_assignments_for_hit(HITId=hit['HITId'],)
    #pprint(response)
    assignments = response['Assignments']
    #pprint(assignments)
    for assignment in assignments:
        if assignment['AssignmentStatus'] == 'Approved':
            print("Worker {} HIT {} with HTITID {}".format(assignment['WorkerId'],hit['HITId'], hit['HITTypeId']))
        #pprint(assignment)
    #raise()
marker = hits['NextToken']
if marker :
    while True:
        hits = mturk.list_hits(NextToken=marker)
        #pprint(hits)
        if 'NextToken' in hits:
            marker = hits['NextToken']
            for hit in hits['HITs']:
                response = mturk.list_assignments_for_hit(HITId=hit['HITId'],)
                assignments = response['Assignments']
                for assignment in assignments:
                    if assignment['AssignmentStatus'] == 'Approved':
                        print("Worker {} HIT {} with HTITID {}".format(assignment['WorkerId'],hit['HITId'], hit['HITTypeId']))
                # Get all workers 
                #pprint(hit)
                #print("HIT {} with HTITID {}".format(hit['HITId'],hit['HITTypeId']))
        else:
            break


#for hit in hits:
#    print(type(hit))
#    print(hit["ResponseMetadata"])
#qualifications = mturk.list_qualification_requests()
#pprint(qualifications)

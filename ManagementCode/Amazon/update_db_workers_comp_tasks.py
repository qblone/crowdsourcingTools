'''
This script gets the workers which has completed the task and updates the
database accordingly. I wrote the script because bug in my initial code which 
resulted in wrong workerid being captured

'''
import sqlite3
import boto3
from boto.mturk.connection import MTurkConnection
from boto.mturk.question import ExternalQuestion
from boto.mturk.price import Price
import json
from pprint import pprint
HOST = 'mechanicalturk.sandbox.amazonaws.com'
#mturk = boto3.client(service_name = 'mturk',region ='us-east-1')

mturk = boto3.client(service_name = 'mturk', region_name='us-east-1')






def updateDB(workerid,hitid):
    conn = sqlite3.connect("/home/code/spoofer_project/db.sqlite3")
    cursor = conn.cursor()
    sql = '''UPDATE spoofer_amazonresults SET worker_id = ? WHERE hit_id =?'''
    print(sql,workerid,hitid )
    cursor.execute(sql, (workerid, hitid))
    cursor.close()
    conn.commit()
    conn.close()




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
            #print("Worker {} HIT {} with HTITID {}".format(assignment['WorkerId'],hit['HITId'], hit['HITTypeId']))
            updateDB(assignment['WorkerId'],hit['HITId'])
        else:
            pprint(assignment)
            raise()
        #pprint(assignment)
    #raise()
marker = hits['NextToken']
if marker :
    while True:
        hits = mturk.list_hits(NextToken=marker)
        #pprint(hits)
        for hit in hits['HITs']:
            response = mturk.list_assignments_for_hit(HITId=hit['HITId'],)
            assignments = response['Assignments']
            for assignment in assignments:
                if assignment['AssignmentStatus'] == 'Approved':
                    updateDB(assignment['WorkerId'],hit['HITId'])
                else:
                    pprint(assignment)
                    raise()
                        #print("Worker {} HIT {} with HTITID {}".format(assignment['WorkerId'],hit['HITId'], hit['HITTypeId']))
                # Get all workers 
                #pprint(hit)
                #print("HIT {} with HTITID {}".format(hit['HITId'],hit['HITTypeId']))
        if 'NextToken' in hits:
            marker = hits['NextToken']
        else:
            break


#for hit in hits:
#    print(type(hit))
#    print(hit["ResponseMetadata"])
#qualifications = mturk.list_qualification_requests()
#pprint(qualifications)

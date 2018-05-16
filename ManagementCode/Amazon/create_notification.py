import boto3
#from boto3 import client
client = boto3.client(service_name ='sqs')
#mturk = boto3.client('mturk')
mturk = boto3.client(service_name = 'mturk',
                     region_name='us-east-1')
#endpoint="https://mturk-requester-sandbox.us-east-1.amazonaws.com")
#response = client.create_queue(QueueName='NotificationQueue',)
#print(response)
mypolicy = {
     "Version": "2008-10-17",
     "Id":
    "arn:aws:sqs:us-east-1:375840132305:mturkNotificationQueue/MTurkOnlyPolicy",
     "Statement": [
           {
                  "Sid": "MTurkOnlyPolicy",
                  "Effect": "Allow",
                  "Principal": {
                          "AWS": "arn:aws:iam::755651556756:user/MTurk-SQS"
                         },
                  "Action": "SQS:SendMessage",
                  "Resource":
               "arn:aws:sqs:us-east-1:375840132305:mturkNotificationQueue"
                 }
          ]
}

myqueue =client.create_queue(QueueName='mturkNotificationQueue')
print(myqueue['QueueUrl'])


#Get the HITTypeID 
hits = mturk.list_hits()

#print(hits)
mHITTypeID =  hits['HITs'][0]['HITTypeId']
def getHitsType():
    all_hit_types = set()
    hits = mturk.list_hits()
    for hit in hits['HITs']:
        all_hit_types.add(hit['HITTypeId'])
    marker = hits['NextToken']
    if marker :
        while True:
            hits = mturk.list_hits(NextToken=marker)
            for hit in hits['HITs']:
                all_hit_types.add(hit['HITTypeId'])
            if 'NextToken' in hits:
                marker = hits['NextToken']
            else:
                break
    return all_hit_types


#print(getHitsType())

hit_types = getHitsType()
#raise()



for mHITTypeID in hit_types:
    #mHITTypeID = hit['HITTypeId']
    print("Creating notification for {}".format(mHITTypeID))
    response = mturk.update_notification_settings(
        HITTypeId=mHITTypeID,
        Notification={
                    'Destination': myqueue['QueueUrl'],
                    'Transport': 'SQS',
                    'Version':   '2006-05-05',
                    'EventTypes': [
                                    'AssignmentAccepted','AssignmentAbandoned','AssignmentSubmitted',
                        
                                ]
                },

)







#response_send_notification = client.send_test_event_notification(
#        Notification={
#                    'Destination': 'string',
#                    'Transport': 'Email'|'SQS',
#                    'Version': 'string',
#                    'EventTypes': [
#                                    'AssignmentAccepted'|'AssignmentAbandoned'|'AssignmentReturned'|'AssignmentSubmitted'|'AssignmentRejected'|'AssignmentApproved'|'HITCreated'|'HITExpired'|'HITReviewable'|'HITExtended'|'HITDisposed'|'Ping',
#                                ]
#                },
#        TestEventType='AssignmentAccepted'|'AssignmentAbandoned'|'AssignmentReturned'|'AssignmentSubmitted'|'AssignmentRejected'|'AssignmentApproved'|'HITCreated'|'HITExpired'|'HITReviewable'|'HITExtended'|'HITDisposed'|'Ping'
#)



#mturk.SendTestEventNotification()
#kms = boto3.client('kms', region_name='us-west-2')
#sqs = boto3.resource('sqs')
#queue = sqs.create_queue(QueueName='test', Attributes={'DelaySeconds': '0'})
#queue = sqs.get_queue_by_name(QueueName='test')
#print(queue.url)

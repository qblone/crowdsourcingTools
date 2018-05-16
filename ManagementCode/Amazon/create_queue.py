import boto3
#from boto3 import client
client = boto3.client(service_name ='sqs')
#mturk = boto3.client('mturk')
mturk = boto3.client(service_name = 'mturk', 
                     endpoint_url =
                     'https://mturk-requester-sandbox.us-east-1.amazonaws.com')
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
response = mturk.update_notification_settings(
        HITTypeId='3TAMZSB5GP382RPR3EH30Y24863XQ7',
        Notification={
                    'Destination': myqueue['QueueUrl'],
                    'Transport': 'SQS',
                    'Version':   '2006-05-05',
                    'EventTypes': [
                                    'AssignmentAccepted',
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

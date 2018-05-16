import boto3
from boto.mturk.connection import MTurkConnection
from boto.mturk.question import ExternalQuestion
from boto.mturk.price import Price
import json
from pprint import pprint


class RemoveWorkerQual():
    mturk = boto3.client(service_name = 'mturk',region_name='us-east-1')
    def __init__(self):
        self.mturk = boto3.client(service_name = 'mturk', region_name='us-east-1')

    def remove_qual(self,worker):
        response = mturk.list_qualification_types( Query='Auto', MustBeRequestable=True, MustBeOwnedByCaller=True,)
        QualID = ''
        if response['QualificationTypes'][0]:
            QualID = response['QualificationTypes'][0]['QualificationTypeId']
            mturk.disassociate_qualification_from_worker( WorkerId=worker['WorkerId'], QualificationTypeId=QualID, Reason='Starting a new batch, you can now take part in experiment again.')
            print("Removed worker qualification" , worker)
        
        else:
            print("There is no qualification, please create one first")
        


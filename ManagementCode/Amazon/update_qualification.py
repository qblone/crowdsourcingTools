import boto3
from pprint import pprint
#from boto3 import client

class UpdateQualification():
    mturk = boto3.client(service_name = 'mturk', region_name='us-east-1')
    def __init__(self):
        self.mturk = boto3.client(service_name = 'mturk', region_name='us-east-1')
    def add_qual(self,worker):
        mturk = boto3.client(service_name = 'mturk',region_name='us-east-1')
        qual = self.get_qualTypeID(mturk)
        response = mturk.associate_qualification_with_worker(
                QualificationTypeId=qual,
                WorkerId=worker,
                IntegerValue=1,
                SendNotification=False
        )
    def get_qualTypeID(self,mturk):
        response = mturk.list_qualification_types(
                    Query='Auto',
                    MustBeRequestable=True,
                    MustBeOwnedByCaller=True,
        )
        return response['QualificationTypes'][0]['QualificationTypeId']





import boto3
import sqlite3


def get_qualTypeID():
    mturk = boto3.client(service_name = 'mturk',region_name='us-east-1', aws_access_key_id='YOURID', aws_secret_access_key='YOURKEY')
    response = mturk.list_qualification_types(
                Query='Auto',
                MustBeRequestable=True,
                MustBeOwnedByCaller=True,
    )
    return response['QualificationTypes'][0]['QualificationTypeId']

def add_qual(worker):
    mturk = boto3.client(service_name = 'mturk',region_name='us-east-1', aws_access_key_id='YOURID', aws_secret_access_key='YOURKEY')
    qual = get_qualTypeID()
    response = mturk.associate_qualification_with_worker(
            QualificationTypeId=qual,
            WorkerId=worker,
            IntegerValue=1,
            SendNotification=False
    )
conn = sqlite3.connect("/home/code/spoofer_project/db.sqlite3")
c = conn.cursor()

# 1) Contents of all columns for row that match a certain value in 1 column
c.execute('select worker_id from spoofer_amazonresults;')
all_rows = c.fetchall()
for worker in all_rows:
    print(worker[0].strip())
    add_qual(worker[0].strip())



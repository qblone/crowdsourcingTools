import boto3
from boto.mturk.connection import MTurkConnection
from boto.mturk.question import ExternalQuestion
from boto.mturk.price import Price
import boto.mturk.qualification as mtqu
from pprint import  pprint





#from boto3 import client
client = boto3.client(service_name ='sqs')
#mturk = boto3.client('mturk')
mturk = boto3.client(service_name = 'mturk', 
                     region_name='us-east-1')






questionSampleFile = open("external_hit.question", "r")
questionSample = questionSampleFile.read()

# Create a qualification with Locale In('US', 'CA') requirement attached
# Get qualification
qualifications = mturk.list_qualification_types(
            Query='Auto',
            MustBeRequestable=True,
            MustBeOwnedByCaller=True,
)


qualification = qualifications['QualificationTypes'][0]['QualificationTypeId']

localRequirements = [{
        'QualificationTypeId': qualification,
        'Comparator': 'DoesNotExist',
        'RequiredToPreview': False
}]

# Create the HIT 
def create_hits(num_of_hits):
    for _ in range(num_of_hits):
        response = mturk.create_hit(
            MaxAssignments = 1,
            LifetimeInSeconds = 604800,
            AssignmentDurationInSeconds = 3600,
            Reward ='0.10',
            Title = 'Download and run a academic research application- 10 cents to qualify, possible $0.90 bonus!',
            Keywords = 'easy, research',
            Description = '''Run a research application and send us the results. Once you have completed one HIT, you can NOT work on subsequent HITs from this batch. We are running a limited number of.
            tests per Internet provider. We will pay you $0.10 to read the instructions and check whether we still need a test result for your Internet providers network. If you see instruction to
            download and run the test application, then you are eligible for a bonus of $0.90. If you see an error message, instead of instructions to run the test, it means that someone has already 
            run the test from your Internet providers network and you are not eligible for the bonus''',
            Question = questionSample,
            QualificationRequirements = localRequirements
    )
    return response
#response = create_hits_from_id()
response = create_hits(100)
pprint(response)
# The response included several fields that will be helpful later
hit_type_id = response['HIT']['HITTypeId']
hit_id = response['HIT']['HITId']
print ("Your HIT has been created. You can see it at this link:")
print("https://workersandbox.mturk.com/mturk/preview?groupId={}".format(hit_type_id))
print ("Your HIT ID is: {}".format(hit_id))

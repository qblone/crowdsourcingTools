""""" 
__author Qasim 

This files read new and old files and find the new records
It then checks the links and update databases for valid entries 

"""
import csv



import csv
import difflib
import sqlite3
import ipaddress
from lxml import html
import requests
from datetime import datetime
from pytz import timezone
import pytz
import math
utc = pytz.utc
from pprint import pprint
import boto3
import xml.etree.ElementTree as ET

class UpDataDB():

    def __init__(self):
        changed_file = '/home/code/spoofer_project/amazon_results/changes.csv'
    
    
    def validate_url_test (self,url):
        link_url = url.split('/')
        print(link_url, len(link_url))
        if len(link_url) !=4:
            return False
        else:
            if (link_url[2]) != 'spoofer.caida.org' and not link_url[3].contains("sessionkey"):
                return False


        # If page does not exist reply false
        page = requests.get(url)
        if page.status_code != 200:
            return False
        else:
            parsed_page = self.validate_testExists(page)
            if not parsed_page:
                print("Not valid key")
                return False
        return parsed_page 


    def validate_testExists(self,page):
        tree = html.fromstring(page.content)
        #print(tree)
        #result =  tree.xpath('//p/text()')
        result = tree.xpath('//div[@id="content"]/p')
        #print(len(result))
        #print(result[0].text.strip())
        if result[0].text.strip() == "Session key not found!":
            print("session key not found")
            return False
        return result


    def getInfoFromPage(self,parsed_page):
        raw = parsed_page[0].xpath('//div[@id="content"]/p/text()')
        date_time = raw[0].strip().split("at:")[1].strip()
        dt,tm,tz = date_time.split()






        print(dt,tm,tz)
        dt_tm = dt + ' ' +tm

        p = '%Y-%m-%d %H:%M:%S'
        epoch = datetime(1970, 1, 1)
        tm_tz = datetime.strptime(dt_tm, p)
        epoch = datetime(1970, 1, 1)
        pacific = timezone('US/Pacific')
        
        pst = pacific.localize(tm_tz, is_dst=True)
        utc_dt = pst.astimezone(utc)
        fmt = '%Y-%m-%d %H:%M:%S'
        utc_dt1 = utc_dt.strftime(fmt)
        dt1 = datetime.strptime(utc_dt1, p)

        print(utc_dt.strftime(fmt))
        #tm_tz = tm_tz.astimezone(timezone('US/Pacific'))

        #tm_tz.replace(tzinfo=timezone.pst)
        epoch_time = ( dt1 - epoch).total_seconds()
        
        result_value = parsed_page[0].xpath('//div[@id="content"]/p/a/text()')
        ip = result_value[0].strip()
        asn = result_value[1].split()[0].strip()
        
        #print()
        #print("time", time  )
        #ip,asn =parsed_page[0].xpath('//div[@id="content"]/p/a/text()')
        #asn = asn.split()[0]
        return [ip,asn,epoch_time ]


    def getEpochTime(self,dt):
        p = '%c'
        dt_new = dt.split()
        local_dt = '{0} {1} {2} {3} {4}'.format(dt_new[0], dt_new[1],dt_new[2],dt_new[3],dt_new[5])
        epoch = datetime(1970, 1, 1)
        tm_tz = datetime.strptime(local_dt, p)
        tz = pytz.timezone('America/New_York')
        eastern = timezone('US/Eastern')
        edt = eastern.localize(tm_tz, is_dst=True)
        utc_dt = edt.astimezone(utc)
        fmt = '%Y-%m-%d %H:%M:%S'
        utc_str = utc_dt.strftime(fmt)
        dt1 = datetime.strptime(utc_str, fmt)
        epoch_time = ( dt1 - epoch).total_seconds()
        print(epoch_time)
        print(dt)
        return epoch_time
    def getEpochTime_from_dt(self,dt):
        epoch = datetime(1970, 1, 1)
        tz = pytz.timezone('America/New_York')
        #eastern = timezone('US/Eastern')
        #edt = eastern.localize(dt, is_dst=True)
        utc_dt = dt.astimezone(utc)
        fmt = '%Y-%m-%d %H:%M:%S'
        utc_str = utc_dt.strftime(fmt)
        dt1 = datetime.strptime(utc_str, fmt)
        epoch_time = ( dt1 - epoch).total_seconds()
        return epoch_time
        



    def parse_page(self,url):
        try:
            page = validate_url_test(url)
            if page:
                test_info =self.getInfoFromPage(page)
                test_asn = test_info[1]
                test_network = self.getNetwork(test_info[0])
            else:
                print("Invalid URL")
        except:
            print("Something went wrong")

    def getNetwork(self,ip_add):
        ip_add = "%s/11" %(ip_add)
        n = ipaddress.ip_network(ip_add, strict=False)
        network = str(n.network_address)
        return network

    def createAmazonUser(self,url, accepted,worker_id, usr,assignmentId,hit_id):
        conn = sqlite3.connect("/home/code/spoofer_project/db.sqlite3")
        cursor = conn.cursor()
        sql = '''Insert into spoofer_amazonresults
        (url,accepted,worker_id,user_id,assignment_id,hit_id)
        values (?,?,?,?,?,?) '''
        print(sql,url, accepted,worker_id, usr,assignmentId,hit_id )
        cursor.execute(sql, (url, accepted,worker_id, usr,assignmentId,hit_id))
        cursor.close()
        conn.commit()
        conn.close()
        print("Updated table")


    def createAmazonUserNB(self,worker_id, usr,dt):
        conn = sqlite3.connect("/home/code/spoofer_project/db.sqlite3")
        cursor = conn.cursor()
        sql = '''Insert into spoofer_amazonnobonus
        (worker_id,user_id,date)
        values (?,?,?) '''
        print(sql,worker_id, usr,dt )
        cursor.execute(sql, (worker_id, usr,dt))
        cursor.close()
        conn.commit()
        conn.close()
        print("Updated table")
    
    def updateAmazonUser(self,url, accepted,worker_id, usr):
        conn = sqlite3.connect("db.sqlite3")
        cursor = conn.cursor()
        sql = '''UPDATE spoofer_amazonresults SET url = ?, accepted =? WHERE worker_id = ? and user_id =?'''
        print(sql,url, accepted,worker_id, usr )
        cursor.execute(sql, (url, accepted,worker_id, usr))
        cursor.close()
        conn.commit()
        conn.close()
        print("Updated table")
        
    def addToCompletedTests(self,usr, test_asn,test_network, url, dt):
        conn = sqlite3.connect("/home/code/spoofer_project/db.sqlite3")
        cursor = conn.cursor()
        sql = """ INSERT into spoofer_completedtests (user_id,asn, ip_network, spoofer_url, date) values (?,?,?,?,?) """
        cursor = conn.cursor()
        cursor.execute(sql, (usr, test_asn,test_network, url, dt))
        cursor.close()
        conn.commit()
        conn.close()

        print("Added value to completed tests!")

    def addComments(self,usr, test_asn,test_network, url, dt):
        conn = sqlite3.connect("/home/code/spoofer_project/db.sqlite3")
        cursor = conn.cursor()
        sql = """ INSERT into spoofer_comments (user_id,comments,date,platform, worker_id) values (?,?,?,?,?) """
        cursor = conn.cursor()
        cursor.execute(sql, (usr, test_asn,test_network, url, dt))
        cursor.close()
        conn.commit()
        conn.close()

        print("Added value to completed tests!")


    # Lets start by reading both files 
    def update_from_file(self):
        with open(changed_file) as newresults:
            reader = csv.DictReader(newresults, delimiter='\t')
            for row in reader:
                #row['Answer.userid'],row['assignmentsubmittime'],row['Answer.aform_pre-spoofer_url'],row['workerid'],row['Answer.bform_pre-comments']
                usr        = row['Answer.userid'] 
                submitTime = row['assignmentsubmittime']
                worker_id  = row['workerid']
                url        = row['Answer.aform_pre-spoofer_url']
                comments   = row['Answer.bform_pre-comments']

                page = validate_url_test(url)
                accepted = False
                if page:
                    accepted = True

                print(accepted)
                if worker_id and url:
                    updateAmazonUser(url, accepted,worker_id, usr)
                    
                if accepted:
                    test_info =self.getInfoFromPage(page)
                    test_asn = test_info[1]
                    test_network = self.getNetwork(test_info[0])
                    dt = test_info[2]
                    addToCompletedTests(usr, test_asn,test_network, url, dt)
                if comments and submitTime:
                    dt = getEpochTime(submitTime)
                    addComments(usr,comments,dt,"MTURK",worker_id)
        


    def update_from_platform(self,hit_id,workerid):
        #mturk = boto3.client(service_name = 'mturk',endpoint_url ='https://mturk-requester-sandbox.us-east-1.amazonaws.com')
        mturk = boto3.client(service_name = 'mturk', region_name='us-east-1')
        response = mturk.list_assignments_for_hit(
                HITId=hit_id,
                AssignmentStatuses=['Submitted'], 
        )
        assignments = response['Assignments']
        for assignment in assignments:
           worker_id = assignment['WorkerId']
           assignmentId = assignment['AssignmentId']
           answer = assignment['Answer']
           submitTime = assignment['SubmitTime']
           print(type(submitTime))
           epoch = datetime.utcfromtimestamp(0)
           dt = self.getEpochTime_from_dt(submitTime)
           print(dt)
           print(submitTime)
           #raise()
           #print ('The Worker with ID {} submitted assignment {} and gave the answer {}'.format(WorkerId,assignmentId,answer))
           tree = ET.ElementTree(ET.fromstring(answer))
           ns ={'ns':'http://mechanicalturk.amazonaws.com/AWSMechanicalTurkDataSchemas/2005-10-01/QuestionFormAnswers.xsd'}
           attr_values = dict()
           for res in tree.findall('ns:Answer',ns):
               attr =res.find('ns:QuestionIdentifier',ns).text
               val = res.find('ns:FreeText',ns).text
               attr_values[attr] = val
               print(attr,val)
           print(attr_values)
           usr        = attr_values['userid']
           url = ''
           comments = ''
           if 'aform_pre-spoofer_url' in attr_values: url =  attr_values['aform_pre-spoofer_url'] 
           if 'bform_pre-comments' in attr_values: comments   = attr_values['bform_pre-comments']
           
           print("printing parsed data",usr,url,comments)
           #pprint(assignment)
           page = False 
           if url:
               page = self.validate_url_test(url)
           else:
               self.createAmazonUserNB(worker_id,usr,dt)
           accepted = False
           if page:
               accepted = True
           print(accepted)
           if worker_id and url:
               self.createAmazonUser(url, accepted,worker_id,
                                     usr,assignmentId,hit_id)
            
           if accepted:
               test_info =self.getInfoFromPage(page)
               test_asn = test_info[1]
               test_network = self.getNetwork(test_info[0])
               dt = test_info[2]
               self.addToCompletedTests(usr, test_asn,test_network, url, dt)
          
           if comments:
               self.addComments(usr,comments,dt,"MTURK",worker_id)


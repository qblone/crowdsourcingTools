from django.shortcuts import render
from django.http import HttpResponse
import datetime
from spoofer.models import Comments as Commodel
from spoofer.models import SpooferUser as Usrmodel
from spoofer.models import Actions as Actmodel
from spoofer.models import CompletedTests as CompletedTestsmodel
from spoofer.models import RejectedUsers as RejectedUsersmodel
from spoofer.models import Asn_Stats as AsnStatsmodel
from spoofer.models import InvalidURLs as Invalidurlmodel
from spoofer.models import Exceptions as Exceptionsmodel
from spoofer.models import AmazonResults as Amazonmodel
from spoofer.models import ProA as Proamodel

from spoofer.models import ProANoBonus as ProANoBonusModel

from spoofer.models import UnresolvedIP as UnresolvedIPmodel
from spoofer.models import GenericPlatforms as OtherPlat
#from spoofer.models import spooferURL
from .forms import submitUrlForm
from .forms import submitCommentForm
from .forms import submitProAForm
from .forms import proAForm_nobonus
from .forms import mturkForm_nobonus


#from .forms import submitUrlForm, submitCommentForm, submitProAForm
#from .forms import submitCommentForm
#from .forms import submitCommentForm

from django.shortcuts import get_object_or_404
from django.views.generic import TemplateView
import pyasn
import time
import os 
from django.conf import settings as st
import ipaddress

from lxml import html
import requests
from datetime import datetime
from pytz import timezone
import pytz
import math
utc = pytz.utc

import boto3




def _get_form(request, formcls, prefix):

    #get_client_properties(request)
    


    #for key in request.POST.keys():
    #    print(key)
    data = request.POST if prefix in request.POST else None
    #data = request.POST if prefix in next(iter(request.POST.keys())) else None
    return formcls(data, prefix=prefix)


usr = Usrmodel()
no_of_online =''

class MyView(TemplateView):
    template_name = 'index.html'
    

    def get(self, request, *args, **kwargs):

        ip_ = get_client_ip(request)

        asn_ = getASN(ip_)

        usr_model = get_client_properties(request,asn_)
        platform_ = getPlatform(request)
        
        


        obj, created = Usrmodel.objects.get_or_create(ip_address=usr_model.ip_address, asn = usr_model.asn, 
            network = usr_model.network, devicetype = usr_model.devicetype, devicefamily = usr_model.devicefamily,
            browser= usr_model.browser,os= usr_model.os,platform=usr_model.platform)

        if not AsnStatsmodel.objects.filter(asn=asn_).exists():
            no_of_tests = getDataPoints_asn(asn_)
            asn_stats = AsnStatsmodel ()
            AsnStatsmodel.objects.get_or_create(asn = asn_, tests_req = no_of_tests)

        





        # Get all users with ipnetwork and asn 
        online_users = Usrmodel.objects.filter(network=usr_model.network, asn= usr_model.asn)

        # Now get a count of all users who viewed the task in past hour 
        # Time an hour ago 
        time_an_hour_ago = epoch_time = int(time.time()) - 3600

        #No of online users an hour ago , date > time_an_hour_ago 

        no_of_online = Actmodel.objects.filter(user=online_users , date__gte=time_an_hour_ago ,status=0).count()




        

        
        usr = obj
        act = Actmodel()
        act.user = obj
        act.status =0
        act.save()
        


        ip_ = get_client_ip(request)
        platform = getPlatform(request)
        test_permission = canPerformTest(obj, request )
        context ={
        'client_ip': str(ip_),'success' : 1,}

        


        #usr_model.save()
        #print(asn_)
        comment_success = 0
        submitbonus = 0
        if test_permission:
            if test_permission ==2:
                test_success =2 
            else:
                test_success = 1
                
              #args['assignment_id'] = args
            #response =  self.render_to_response({'aform': submitUrlForm.SubmitUrlForm(prefix='aform_pre', initial={'spoofer_url': '',}), 
            #    'bform': submitCommentForm.SubmitCommentsForm(prefix='bform_pre',initial={'comments': '',} ), 
             #   'client_ip': str(obj.network),'test_success' : 1, 'comment_success' : 0, 'no_online':no_of_online, "assignment_id": request.GET.get("assignmentId", ""),"userid":obj.id,
              #  })
              #return response
        else:
            test_success = 0
            #response =  self.render_to_response({'aform': submitUrlForm.SubmitUrlForm(prefix='aform_pre', initial={'spoofer_url': '',}), 
             #  'bform': submitCommentForm.SubmitCommentsForm(prefix='bform_pre',initial={'comments': '',} ), 'client_ip': str(usr_model.devicetype),"assignment_id": request.GET.get("assignmentId", ""),
              #  'test_success' : 0,  'comment_success' : 0,"userid":obj.id, })
            #response['x-frame-options'] = 'this_can_be_anything'
            #return response


        url =''
        args = getpostArguments (request,test_success, comment_success, no_of_online,obj.id,url,submitbonus)
        response = self.render_to_response(args)
        response['x-frame-options'] = 'this_can_be_anything'
        return response





    def post(self, request, *args, **kwargs):
        comp_test = CompletedTestsmodel()
        comm_inst = Commodel()
        submitbonus = 0 
        ip_ = get_client_ip(request)
        aform = _get_form(request, submitUrlForm.SubmitUrlForm, 'aform_pre')
        bform = _get_form(request, submitCommentForm.SubmitCommentsForm, 'bform_pre')
        proaform = _get_form(request, submitProAForm.SubmitProAForm, 'proaform')
        mturknobonus = _get_form(request, mturkForm_nobonus.SubmitMturkFormNB, 'mnbform')
        proanobonus = _get_form(request, proAForm_nobonus.SubmitProAFormNB, 'pnbform')


        #test_permission = canPerformTest(request, ip_ )

        asn_ = getASN(ip_)

        usr =  get_client_properties(request,asn_)
        # Get platform 
        platform = getPlatform(request)
        if not platform:
            platform ='WebBrowser'
        # Get worker 
        
        



        test_permission = canPerformTest(usr, request )
        test_success = -1
        comment_success = 0
        os_selected = request.POST.get('rg',None)
        usr_ = Usrmodel.objects.get(ip_address=usr.ip_address, asn = usr.asn, network = usr.network, 
                            devicetype = usr.devicetype, devicefamily = usr.devicefamily,browser= usr.browser,os= usr.os, platform = usr.platform)
        url =''


        if aform.is_bound and aform.is_valid():
            if test_permission:
                url = aform.cleaned_data['spoofer_url']
                
                #proaid = aform.cleaned_data['proa_value']
                

               
                try:
                    usr_ = Usrmodel.objects.get(ip_address=usr.ip_address, asn = usr.asn, network = usr.network, 
                            devicetype = usr.devicetype, devicefamily = usr.devicefamily,browser= usr.browser,os= usr.os,platform=usr.platform)
                    o_pltaform = OtherPlat()
                    o_pltaform.user = usr_
                    o_pltaform.url = url
                    o_pltaform.platform = usr_.platform
                    o_pltaform.save()
                    
                    page = validate_url_test(url)
                    if page:
                        test_info =getInfoFromPage(page)


                        test_asn = test_info[1]
                        test_network = getNetwork(test_info[0])

                        if canSubmitURL(usr_,test_network,test_asn,platform): 
                            # Save completed test 
                            comp_test.user = usr_
                            comp_test.asn = test_asn
                            comp_test.ip_network = test_network
                            comp_test.spoofer_url = url
                            comp_test.save()
                            test_success = 2

                        else:
                            test_success = 0

                    else:
                        #print("page does not exits or wrong url")
                        # Save invalid URLs
                        obj, created = Invalidurlmodel.objects.get_or_create(user=usr_, url=url)

                        test_success = -2
                except  Exception as inst:


                    usr_ = Usrmodel.objects.get(ip_address=usr.ip_address, asn = usr.asn, network = usr.network, 
                            devicetype = usr.devicetype, devicefamily = usr.devicefamily,browser= usr.browser,os= usr.os,platform=usr.platform)
                    #print(inst)

                    obj, created = Exceptionsmodel.objects.get_or_create(user=usr_, exception=inst)
                    test_success = -3


                # suburl_inst.spoofer_url = aform.cleaned_data['spoofer_url']
                # suburl_inst.ip_address = ip_ 
                # suburl_inst.pub_date = datetime.date.today()#
                # suburl_inst.status = '1'
                # suburl_inst.save()
               
            else: 
                test_success = 0
            comment_success =0


        elif mturknobonus.is_bound and mturknobonus.is_valid():
            test_success = 0
            submitbonus = 1

        elif proanobonus.is_bound and proanobonus.is_valid():
            test_success = 0
            submitbonus = 1
            usr_ = Usrmodel.objects.get(ip_address=usr.ip_address, asn = usr.asn, network = usr.network, 
                            devicetype = usr.devicetype, devicefamily = usr.devicefamily,browser= usr.browser,os= usr.os,platform=usr.platform)
            #uid = proanobonus.cleaned_data['participantID']
            pro_nobonus = ProANoBonusModel()
            pro_nobonus.user = usr_  
            pro_nobonus.worker_id = proanobonus.cleaned_data['participantID']
            pro_nobonus.save()


        


                # Process aform and render response
        elif bform.is_bound and bform.is_valid():
            usr_ = Usrmodel.objects.get(ip_address=usr.ip_address, asn = usr.asn, network = usr.network, 
                            devicetype = usr.devicetype, devicefamily = usr.devicefamily,browser= usr.browser,os= usr.os,platform=usr.platform)
            workerid = getWorkerId(request)

            comm_inst.comments = bform.cleaned_data['comments']
            comm_inst.user = usr_ 
            comm_inst.platform = platform
            comm_inst.worker_id = workerid

            comm_inst.save()
            comment_success = 1
            if test_permission:
                test_success = -1
                if test_permission == 2:
                    test_success =2 

            else:
                test_success = 0


        elif proaform.is_bound and proaform.is_valid():
            proaid = request.POST.get('id')
            url = proaform.cleaned_data['spoofer_url']
            usr_ = Usrmodel.objects.get(ip_address=usr.ip_address, asn = usr.asn, network = usr.network, 
                            devicetype = usr.devicetype, devicefamily = usr.devicefamily,browser= usr.browser,os= usr.os,platform=usr.platform)
            promodel = Proamodel.objects.get(pro_id=proaid)
            uid = proaform.cleaned_data['participantID']
            promodel.worker_id = uid
            promodel.url = url
            promodel.save()

            try:
                    usr_ = Usrmodel.objects.get(ip_address=usr.ip_address, asn = usr.asn, network = usr.network, 
                            devicetype = usr.devicetype, devicefamily = usr.devicefamily,browser= usr.browser,os= usr.os, platform=usr.platform)
                    
                    page = validate_url_test(url)
                    if page:
                        test_info =getInfoFromPage(page)


                        test_asn = test_info[1]
                        test_network = getNetwork(test_info[0])

                        if canSubmitURL(usr_,test_network,test_asn,platform): 
                            # Save completed test 
                            comp_test.user = usr_
                            comp_test.asn = test_asn
                            comp_test.ip_network = test_network
                            comp_test.spoofer_url = url
                            comp_test.save()
                            test_success = 2

                        else:
                            test_success = 0

                    else:
                        #print("page does not exits or wrong url")
                        # Save invalid URLs
                        obj, created = Invalidurlmodel.objects.get_or_create(user=usr_, url=url)

                        test_success = -2
            except  Exception as inst:


                    usr_ = Usrmodel.objects.get(ip_address=usr.ip_address, asn = usr.asn, network = usr.network, 
                            devicetype = usr.devicetype, devicefamily = usr.devicefamily,browser= usr.browser,os= usr.os, platform=usr.platform)

                    inst = inst + "exception in submit"
                    #print(inst)

                    obj, created = Exceptionsmodel.objects.get_or_create(user=usr_, exception=inst)
                    test_success = -3





        
        


            # Process bform and render response
        args = getpostArguments (request,test_success, comment_success, no_of_online,usr_.id,url,submitbonus) 

        response = self.render_to_response(args)   
        
        #response = self.render_to_response({'aform': aform, 'bform': bform,'test_success' :test_success, 'comment_success' : comment_success,})
        response['x-frame-options'] = 'this_can_be_anything'
        return response



def getpostArguments (request,test, comment, no_of_online,usrid,url_,submitbonus):

    post_args = {'aform': submitUrlForm.SubmitUrlForm(prefix='aform_pre', initial={'spoofer_url': '',}), 
    'bform': submitCommentForm.SubmitCommentsForm(prefix='bform_pre',initial={'comments': '',} ), 
    'mnbform': mturkForm_nobonus.SubmitMturkFormNB(prefix='mnbform'), 
    'test_success' : test, 'comment_success' : comment, 'no_online':no_of_online, 'submit_bonus':submitbonus }



    if test == 2 and url_:
        code = url_.split("=")[-1]
        post_args['validation_code'] = code
        #raise()
        
    
    # Check platform 
    if getPlatform(request) == "MTURK":
        post_args['platform'] = "MTURK"
        post_args ['userid']  = usrid
        post_args["assignmentId"] =request.GET.get("assignmentId", "").strip()
        #post_args['AMAZON_HOST'] = 'https://workersandbox.mturk.com/mturk/externalSubmit'
        post_args['AMAZON_HOST'] = "https://www.mturk.com/mturk/externalSubmit"
        post_args["worker_id"] =  request.GET.get("workerId", "").strip()
        post_args["assignment_id"] =   request.GET.get("assignmentId", "").strip()
        post_args["hit_id"] =   request.GET.get("hitId", "").strip()
        #update_qual = UpdataQual()
        workerid = request.GET.get("workerId", "").strip()

        #update_qual = UpdateQualification()

        if workerid:
            add_qual(workerid)
         #   update_qual.add_qual(workerid)
       # Check if it prolific 
    if getPlatform(request) =="ProA":
        post_args['platform'] = "ProA"
        post_args['userid'] = usrid
        post_args['proaform'] = submitProAForm.SubmitProAForm(prefix='proaform', initial={'spoofer_url': '','participant id': '',})
        post_args['pnbform'] = proAForm_nobonus.SubmitProAFormNB(prefix='pnbform', initial={'participant id': '',})

        # In get create an object if id does not exist or send a new object 
        if request.method == 'GET':
            prmodel = Proamodel()
            # Get user
            usr_ = Usrmodel.objects.get(id=usrid)
            prmodel.user = usr_
            prmodel.save()
            post_args['promodel_id'] = prmodel.pro_id
        else:
            post_args['promodel_id'] = request.POST.get('id')
       

    


    post_args["worker_id"] =  request.get_full_path()

    return post_args







    # First find the platform, if it is amazon then in get variable we will find value for 


def getPlatform(request):

    if request.method == 'GET':
        if request.GET.get("assignmentId", ""): 
            return "MTURK"
    platform = request.GET.get("platform", "")
    if platform:
        return platform
    else:
        return "WebBrowser"




def canSubmitURL(usr,network,asn_,platform_):
    if CompletedTestsmodel.objects.filter(ip_network=network, asn=asn_).exists():

        # How many tests 
        comp_tests = CompletedTestsmodel.objects.filter(ip_network=network, asn=asn_).count()

        # # Look at the table first, if we find the count take that,
        # # else create entry and check if the number of tests are larger or smaller
        no_of_tests = AsnStatsmodel.objects.get(asn=asn_).tests_req

        if not CompletedTestsmodel.objects.filter(ip_network=usr.network).exists():
            if comp_tests < no_of_tests :
                return True
            else: # Add to table of rejected tests 
                rejuser_model = RejectedUsersmodel ()
                rejuser_model.user= usr
                rejuser_model.asn = asn_
                rejuser_model.platform = platform_
                rejuser_model.ip_network = network
                rejuser_model.deny_on_sub = True
                rejuser_model.save()
                return False
            


        # else:
        #     # calculate number of /11 for this network 
        #     # Add to database and send true 
        #     no_of_tests = getasnsize(asn_)
        #     asn_stats = AsnStatsmodel ()
        #     asn_stats.asn = asn_
        #     asn_stats.tests_req = no_of_tests
        #     #obj, created = AsnStatsmodel.objects.get_or_create( asn = asn_, tests_req= no_of_tests)
        #     if comp_tests < no_of_tests :
        #         return True
        #     else: # Add to table of rejected tests 
        #         rejuser_model = RejectedUsersmodel ()
        #         rejuser_model.user= usr
        #         rejuser_model.asn = asn_
        #         rejuser_model.ip_network = network
        #         rejuser_model.save()
        #         return False
    else:
        return True


def canPerformTest(usr,request):


    platform_ = getPlatform(request)
    if not platform_:
        platform_ ='WebBrowser'

 
    # Check if IP is part of database, change to ASN 
    # Check how many of them are there already, check with the file, if the test is there
    # if the number of tests performed by ASN is under limit, show accepted else send false 

    # Get the results for my IP address, 
    #no_of_ips = IPmodel.objects.filter(ip_address=ip_add).count()
    
    #asn_ = getASN(ip_add)



    
    if CompletedTestsmodel.objects.filter(ip_network=usr.network, asn=usr.asn).exists():

        # How many tests 
        comp_tests = CompletedTestsmodel.objects.filter(ip_network=usr.network, asn=usr.asn).count()
        # Look at the table first, if we find the count take that,
        # else create entry and check if the number of tests are larger or smaller
        

        usr_ = Usrmodel.objects.get(ip_address=usr.ip_address, asn = usr.asn, network = usr.network, 
            devicetype = usr.devicetype, devicefamily = usr.devicefamily,browser= usr.browser,os= usr.os, platform=usr.platform)


        no_of_tests = AsnStatsmodel.objects.get(asn=usr.asn).tests_req
        

        if not CompletedTestsmodel.objects.filter(ip_network=usr.network).exists():
            if comp_tests < no_of_tests :
                return True
        else: # Add to table of rejected tests 
                # Get user 
            rejuser_model = RejectedUsersmodel ()
            rejuser_model.user= usr_
            rejuser_model.asn = usr.asn
            rejuser_model.ip_network = usr.network
            rejuser_model.platform = platform_
            rejuser_model.save()
            return False
        

            #return True


            


    else:# add logic if we have less or more then allowed.  #Check if the user is from Aamzon 
        return True

    # read file and get all ASNs after test start date 
    # Convert test start date to epoch 
    #test_start_date =  '15-02-2016'
    #pattern = '%d-%m-%Y'
    #epoch = int(time.mktime(time.strptime(test_start_date, pattern)))
    # search if asn is available with test 
    #return findreportedASN(asn_,epoch)





    # if no_of_ips == 1:
    #     return False
    # else:
    #     return True

def getasnsize (asn):
    db = pyasn.pyasn('/data/db.rviews/ipasn_20170207.dat')
    all_prefixes = db.get_as_prefixes_effective(asn)
    size = 0
    if all_prefixes:
        for prefix in all_prefixes:
            pref = prefix.split("/")[1]
            size = size + (2**(32-int(pref)))
    #asn_size = `asn`+","+`size`
    
    return size

def getDataPoints_asn (asn):
    db = pyasn.pyasn('/data/db.rviews/ipasn_20170207.dat')
    all_prefixes = db.get_as_prefixes_effective(asn)
    size = 0
    if all_prefixes:
        for prefix in all_prefixes:
            pref = prefix.split("/")[1]
            size = size + (2**(32-int(pref)))

    dt_points = math.ceil(size/2097152)

    #asn_size = `asn`+","+`size`
    
    return dt_points




def getNetwork(ip_add):
    ip_add = "%s/11" %(ip_add)
    n = ipaddress.ip_network(ip_add, strict=False)
    network = str(n.network_address)
    return network


def findreportedASN(asn,start_date):
    # find all tests for ASNs
    # read file 
    with open(os.path.join(st.BASE_DIR,'spoofer-crowdsourcing.txt')) as fd: 
        for line in fd: 
            asn_,nat, n_nat = line.strip().split()
            if asn == asn_ and (int(nat)>=start_date or int(n_nat) >= start_date):
                return False
    return True



def getASN (ip_addr):
    asndb = pyasn.pyasn('/data/db.rviews/ipasn_20170207.dat')
    asn_size = asndb.lookup(ip_addr)
    asn = asn_size[0]
    # Check if ASN Count is in the database, if yes get it otherwise calculate the size of AS and 
    # get the number of points required, add this to database. 
    if not asn:
        UnresolvedIPmodel.objects.get_or_create(ip_address = ip_address)

    return asn 





def get_client_ip(request):
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip


def save_onload(ip_addr):
    get_ip= ip() #imported  class from model
    get_ip.ip_address=ip_addr
    get_ip.pub_date = datetime.date.today()#import datetim
    get_ip.status = 0
    get_ip.save()



def get_amazon_properties(request):
    amazon = Amazonmodel()
    amazon.assignment_id = request.GET.get("assignmentId", "").strip()
    amazon.worker_id     =  request.GET.get("workerId", "").strip()
    amazon.hit_id        =   request.GET.get("hitId", "").strip()
    return amazon


def getWorkerId(request):
    platform = getPlatform(request)
    if platform == "MTURK":
        workerid = request.GET.get("workerId", "").strip()
    elif platform == "ProA":
        usrid = request.POST.get("id")
        if Proamodel.objects.filter(pro_id=usrid).exists():
            workerid = Proamodel.objects.get(pro_id=usrid).pro_id
        else:
            workerid = 0
    else:
        workerid = 0
    return workerid



def get_client_properties (request,asn):

    usr = Usrmodel()
    ip_addr = get_client_ip(request)
    usr.ip_address = ip_addr
    device_type = ''
    if request.user_agent.is_mobile:
        device_type = "1,"
    else:
        device_type ="0,"
    if request.user_agent.is_tablet:
        device_type = device_type + "1,"
    else:
        device_type = device_type + "0,"
    if request.user_agent.is_touch_capable:
        device_type = device_type + "1,"
    else:
        device_type = device_type + "0,"
    
    if request.user_agent.is_pc:
        device_type = device_type + "1,"
    else:
        device_type = device_type + "0,"

    if request.user_agent.is_bot:
        device_type = device_type + "1"
    else:
        device_type = device_type + "0"


    usr.devicetype = device_type
    usr.browser = request.user_agent.browser.family
    usr.os = request.user_agent.os.family + "," + request.user_agent.os.version_string
    usr.devicefamily = request.user_agent.device.family
    usr.asn = asn
    usr.network = getNetwork(ip_addr)
    usr.platform = getPlatform(request)

    #workerid = request.GET.get("workerId", "")
    #if workerid: 
    #    usr.worker_id = workderid 

    #assignmentId = request.GET.get("assignmentId", "")
    #if assignmentId:
    #    usr.assignment_id = assignmentId 

   # hitid = request.GET.get("hitId", "")
    
    #if hitid:
     #   usr.hit_id = hitid 





    return usr





def validate_url_test(url):
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
        parsed_page = validate_testExists(page)
        if not parsed_page:
            print("Not valid key")
            return False
    


    

    return parsed_page        # Test for domain
        

    # The first thing to test is if it is in correct format
    
    #if page.status_code == 200:
    #   print('Web site exists')

def validate_testExists(page):
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




def getInfoFromPage(parsed_page):
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
    #print()
    #print("time", time  )
    #ip,asn =parsed_page[0].xpath('//div[@id="content"]/p/a/text()')
    #asn = asn.split()[0]
    result_value = parsed_page[0].xpath('//div[@id="content"]/p/a/text()')
    ip = result_value[0].strip()
    asn = result_value[1].split()[0].strip()

    return [ip,asn,epoch_time ]

def get_qualTypeID():
    mturk = boto3.client(service_name = 'mturk',region_name='us-east-1', aws_access_key_id='YOURKEY', aws_secret_access_key='YOURSECRETKEY')
    response = mturk.list_qualification_types(
                Query='Auto',
                MustBeRequestable=True,
                MustBeOwnedByCaller=True,
    )
    return response['QualificationTypes'][0]['QualificationTypeId']

def add_qual(worker):
    mturk = boto3.client(service_name = 'mturk',region_name='us-east-1', aws_access_key_id='YOURAMAZONKEY', aws_secret_access_key='YOURAMAZONACCESSID')
    qual = get_qualTypeID()
    response = mturk.associate_qualification_with_worker(
            QualificationTypeId=qual,
            WorkerId=worker,
            IntegerValue=1,
            SendNotification=False
    )





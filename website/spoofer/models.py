from django.core.validators import URLValidator
from django.db import models
import re
import django
from unixtimestampfield.fields import UnixTimeStampField


# Create your models here.

class SpooferUser(models.Model):
    asn = models.IntegerField()
    ip_address = models.GenericIPAddressField()
    network = models.GenericIPAddressField()
    devicetype = models.CharField( max_length=10)
    browser = models.CharField(max_length=60)
    os = models.CharField(max_length=20)
    devicefamily = models.CharField(max_length=20)
    platform =  models.CharField( max_length=10, default ='')
    #canPerformTest = models.IntegerField()
    
    class Meta:
        unique_together = ("ip_address", "devicetype", "browser", "os","platform")



class UnresolvedIP(models.Model):
    ip_address = models.GenericIPAddressField()

	# We define type of machine by a coma seperated string 
	# for instance 1,0,1,0,0 means that the user was on mobile with touch screen 




	#print("is mobile", request.user_agent.is_mobile) # returns True
    #print("is tablet", request.user_agent.is_tablet) # returns False
    #print("is touch capable", request.user_agent.is_touch_capable )# returns True
    #print("is pc ", request.user_agent.is_pc) # returns False
    #print("is bot ", request.user_agent.is_bot) # returns False

    

    # Accessing user agent's browser attributes
    

    #print("browser",request.user_agent.browser  )# returns Browser(family=u'Mobile Safari', version=(5, 1), version_string='5.1')
    #print("browser family" , request.user_agent.browser.family)  # returns 'Mobile Safari'
    #request.user_agent.browser.version  # returns (5, 1)
    #request.user_agent.browser.version_string   # returns '5.1'

    



    # Operating System properties
    #print("OS", request.user_agent.os ) # returns OperatingSystem(family=u'iOS', version=(5, 1), version_string='5.1')
    #print("OS Family ", request.user_agent.os.family)  # returns 'iOS'
    #print("OS Version", request.user_agent.os.version)  # returns (5, 1)
    #print("OS Version string", request.user_agent.os.version_string)  # returns '5.1'
    



    # Device properties
    #print("device", request.user_agent.device)  # returns Device(family='iPhone')
    #print("device family", request.user_agent.device.family)  # returns 'iPhone'

class AmazonResults(models.Model):
    user = models.ForeignKey(SpooferUser)
    worker_id = models.CharField( max_length=50, default ='')
    assignment_id = models.CharField( max_length=50, default ='')
    hit_id = models.CharField( max_length=50,default ='')
    accepted = models.BooleanField(default=False)
    url = models.URLField(default ='')


class AmazonNoBonus(models.Model):
    user = models.ForeignKey(SpooferUser)
    worker_id = models.CharField( max_length=50, default ='')
    date = UnixTimeStampField(auto_now_add=True,default ='2017-05-07 00:00:00')
  

class ProA(models.Model):
    pro_id = models.AutoField(primary_key=True)
    user = models.ForeignKey(SpooferUser)
    worker_id = models.CharField( max_length=50, default ='')
    url = models.URLField(default ='')
    class Meta:
        unique_together = ('pro_id','user')

class GenericPlatforms(models.Model):
    user = models.ForeignKey(SpooferUser)
    url = models.URLField(default ='')
    platform =  models.CharField( max_length=10, default ='')



class ProANoBonus(models.Model):
    pro_id = models.AutoField(primary_key=True)
    user = models.ForeignKey(SpooferUser)
    worker_id = models.CharField( max_length=50, default ='')
    date = UnixTimeStampField(auto_now_add=True)
    class Meta:
        unique_together = ('pro_id','user')

    
class Asn_Stats(models.Model):
    asn = models.IntegerField()
    tests_req = models.IntegerField()

class CompletedTests(models.Model):
    user = models.ForeignKey(SpooferUser)
    asn = models.IntegerField()
    ip_network = models.GenericIPAddressField()
    spoofer_url = models.URLField(default ='')
    date = UnixTimeStampField(auto_now_add=True)

class RejectedUsers(models.Model):
    user = models.ForeignKey(SpooferUser)
    asn = models.IntegerField()
    ip_network = models.GenericIPAddressField()
    date = UnixTimeStampField(auto_now_add=True)
    user = models.ForeignKey(SpooferUser)
    comments = models.CharField(max_length=200,default ='')
    date = UnixTimeStampField(auto_now_add=True)
    platform  = models.CharField( max_length=10, default ='')
    deny_on_sub = models.BooleanField(default=False)



class Actions(models.Model):
	user = models.ForeignKey(SpooferUser)
	date = UnixTimeStampField(auto_now_add=True)
	status = models.IntegerField(default=0) #0 = page load, 1 = submit URL, 2 = Comment submitted


class SpooferUrl(models.Model):
    user = models.ForeignKey(SpooferUser)
    spoofer_url = models.URLField(default ='')
    date = UnixTimeStampField(auto_now_add=True)


class InvalidURLs(models.Model):
    user = models.ForeignKey(SpooferUser)
    url = models.URLField(default ='')

class Exceptions(models.Model):
    user = models.ForeignKey(SpooferUser)
    exception = models.CharField(max_length=100)




class Comments(models.Model):
    user = models.ForeignKey(SpooferUser)
    comments = models.CharField(max_length=200,default ='')
    date = UnixTimeStampField(auto_now_add=True)
    platform  = models.CharField( max_length=10, default ='')
    worker_id = models.IntegerField(default =0)
    class Meta:
        unique_together = ("user", "comments", "date")







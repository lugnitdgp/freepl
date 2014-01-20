from django.shortcuts import render
from django.http import HttpResponse,HttpResponseRedirect
import json
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.models import User
from freepl.models import fplUser,fixtures,fixtureCricketPlayers,CricketPlayer,fixtureTeams
from django.core.validators import validate_email
from fplcustomtests import istheteamvalid

def chkkey(dic,li):
	flag=1
	for l in li:
		if not dic.has_key(l):
			flag=0
			break
	return flag


"""
makes the player object list from a given teamconfig
"""
def make_playerlist_from_config(teamconfig):
	tmp=teamconfig.split(',')
	del tmp[len(tmp)-1]
	playerlist=[]
	for i in range(0,len(tmp)):
		playerlist.append(CricketPlayer.objects.get(playerid=tmp[i]))
	return playerlist
	
def user_verify(request,activation_key):
	flag=0
	pwd=""
	#print "82ghzsF8itjyckjm9tVNbGLItbcFPckIxOhVbqtQFCI="
	print User.objects.all().filter(username="tutogaya")[0].password
	activation_key=activation_key.decode("hex")
	for user in User.objects.all():
		pwd=user.password
		tmp=pwd.split('$')
		if tmp[3]==activation_key:
			if user.is_active:
				return HttpResponse("Stop being silly, after activating yourself!")
			user.is_active=True
			user.save()
			return render(request,'startpage/start.html',{'alert':"activated"})
	return HttpResponse("Invalid confirmation link!")
	
	
# Create your views here.
def init(request):

	if request.user.is_authenticated():
		return mainpage(request)#,'main/logged.html',{"username":request.user.username})	
	else:
		return render(request,'startpage/start.html')
from django.contrib.auth.decorators import login_required

def loginit(request):
	tmp=request.POST
	print tmp
	response_dict={'server_response': "no" }
	print "jhg"
	if chkkey(tmp,['username','password']):
		print tmp['username']
		user=authenticate(username=tmp['username'],password=tmp['password'])
		print user
		if user is not None and user.is_active:
			login(request,user)
			response_dict.update({'server_response': "yes" })                                                                  
	return HttpResponse(json.dumps(response_dict), mimetype='application/javascript')

def registerit(request):
	tmp=request.POST
	response_dict={"server_reponse":"no","server_message":"Data recieved was incomplete, check for errors!"}
	print "jh"
	if chkkey(tmp,['email','username','phone','password','passwordagain']):
		#check if user already exists
		if User.objects.filter(username=tmp['username']):
			response_dict.update({"server_message":"username already exists"})
			return HttpResponse(json.dumps(response_dict),mimetype='application/javascript')
		#check if the phone number is valid
		if len(tmp['phone'])!=10:
			response_dict.update({"server_message":"Wrong Mobile Number"})
			return HttpResponse(json.dumps(response_dict),mimetype='application/javascript')			
		#check if the password is not blank
		if tmp['password']=="":
			response_dict.update({"server_message":"Password is blank"})
			return HttpResponse(json.dumps(response_dict),mimetype='application/javascript')			
		#check if the password is matching the previous one
		if tmp['passwordagain']!=tmp['password']:
			response_dict.update({"server_message":"Retyped password does not match"})
			return HttpResponse(json.dumps(response_dict),mimetype='application/javascript')			
		#check if the email is unique 
		#if not validate_email("mayankgmail.com"):
		#	print "fucke "
		try:
			validate_email(tmp['email'])
		except:
			response_dict.update({"server_message":"Email is invalid"})
			return HttpResponse(json.dumps(response_dict),mimetype='application/javascript')			
		if fplUser.objects.filter(email=tmp['email']):
			response_dict.update({"server_message":"Email is already registered"})
			return HttpResponse(json.dumps(response_dict),mimetype='application/javascript')						
		#creating the User object
		user = User.objects.create_user(tmp['username'], tmp['email'],tmp['password'])
		user.is_active = False
		print user.password+" ee "
		user.save()
		hexkey=(user.password.split('$')[3]).encode("hex")
		activation_url="http://<domain-name>/activate/"+hexkey
		
		"""
		we send email of the activation_url to the user email address here
		"""
		
		#creating the fplUser object
		
		fpluser=fplUser(username=tmp['username'],email=tmp['email'],phonenumber=tmp['phone'],\
		cumulativescore=0,recentscore=0)
		fpluser.save()
		#userd=authenticate(username=tmp['username'],password=tmp['password'])
		#login(request,userd)
		response_dict.update({"server_response":"yes","server_message":"Registration Successful"})
		return HttpResponse(json.dumps(response_dict),mimetype='application/javascript')
	return HttpResponse(json.dumps(response_dict),mimetype='application/javascript')

@login_required
def mainpage(request):
	"""
	here we need to add the various context parameters needed for 
	the template logged.html template which includes really the entire 
	content of the site 
	"""
	allfixtures=fixtures.objects.all()
	teamlists=[]
	powerpids=[]
	teamnames=[]
	tt=fixtureTeams.objects.filter(username=request.user.username)
	myresults=list(tt)
	print myresults
	print "fd"
	for fix in allfixtures:
		userfixtured=[]
		if tt:
			print tt			
			userfixtured=tt.filter(fixtureid=fix.fixtureid)
			if userfixtured:
				teamlists.append(make_playerlist_from_config(userfixtured[0].teamconfig))
				powerpids.append(userfixtured[0].powerpid)
				teamnames.append(userfixtured[0].teamname)
			else:
				teamlists.append([])
				powerpids.append("")
				teamnames.append("")
		else:
			teamlists.append([])
			powerpids.append("")
	playerlist=CricketPlayer.objects.all()
	allcricketplayers=CricketPlayer.objects.all()
	"""
	following is a three-in-one list zipped into one.
	"""
	fixnteamsnpowname=zip(allfixtures,teamlists,powerpids,teamnames)
	fixtureresults=fixtureTeams.objects.all().order_by('score')
	cumusers=fplUser.objects.all().order_by('cumulativescore')
	recentusers=fplUser.objects.all().order_by('recentscore')
	return render(request,'main/logged.html',{"username":request.user.username,\
	"playerlist":playerlist,"fixnteamsnpowname":fixnteamsnpowname,"fixtureresults":fixtureresults,\
	"cumusers":cumusers,"myresults":myresults,"allfixtures":allfixtures,"allcricketplayers":allcricketplayers})

def logoutit(request):
	logout(request)
	response_dict={'server_response':'yes'}
	return HttpResponse(json.dumps(response_dict),mimetype='application/javascript')

@login_required
def locktheteamit(request):
	"""
	returns whether the team is lockable if not return the error
	and if lockable then lock it modify the dbs and return the successful
	team
	"""
	response_dict={'server_response':"yes","server_message":"Data recieved was incomplete, check for errors!"};
	tmp=request.POST
	if chkkey(tmp,["teamconfig","teamname","fixtureid","powerpid"]):
		print tmp["teamconfig"],tmp["fixtureid"],tmp["teamname"]
		tmp2=tmp["teamconfig"].split(',')
		#pretest
		fixt=fixtures.objects.get(fixtureid=tmp["fixtureid"]
		"""
		very very important check!!!!!!!
		"""
		if fixt.nomoreteams or not fixt.isactive or fixt.isover:
			response_dict={"server_response":"no","server_message":"Fixture either inactive, closed or over."}
			return HttpResponse(json.dumps(response_dict),mimetype='application/javascript')			
		if tmp["teamconfig"]=="" or tmp["teamname"]=="" or len(tmp2)!=12:
			response_dict={"server_response":"no","server_message":"Improper team name or configuration."}
			return HttpResponse(json.dumps(response_dict),mimetype='application/javascript')
		allfixteams=fixtureTeams.objects.filter(teamname=tmp["teamname"],fixtureid=tmp["fixtureid"])
		if not (allfixteams.filter(username=request.user.username)) and allfixteams:
			response_dict={"server_response":"no","server_message":"someone already took the team name for the fixture."}
			return HttpResponse(json.dumps(response_dict),mimetype='application/javascript')			
		
		rivals=[]
		rivals.append(fixtures.objects.get(fixtureid=tmp["fixtureid"]).teamA)
		rivals.append(fixtures.objects.get(fixtureid=tmp["fixtureid"]).teamB)
		teamrcvd=make_playerlist_from_config(tmp["teamconfig"])
		resobj=istheteamvalid(teamrcvd,rivals,tmp["powerpid"])
		res=resobj.evaluate()
		if res!="yes":
			response_dict.update({"server_response":"no","server_message":res})
			return HttpResponse(json.dumps(response_dict),mimetype='application/javascript')
		else:
			"""
			which means that the team is valid and is ready to be written
			in the fixtureteams db
			"""
			#print ftdobj
			#deleting any old teams
			fixtureTeams.objects.filter(fixtureid=tmp["fixtureid"],username=request.user.username).delete()			
			ftdbobj=fixtureTeams(teamname=tmp["teamname"],username=request.user.username,\
			fixtureid=tmp["fixtureid"],teamconfig=tmp["teamconfig"],powerpid=tmp["powerpid"],score=0)
			ftdbobj.save()
			print "Team Successfully saved"
			response_dict.update({"server_message":"congos"})
			return HttpResponse(json.dumps(response_dict),mimetype='application/javascript')
	return HttpResponse(json.dumps(response_dict),mimetype='application/javascript')


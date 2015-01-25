from django.shortcuts import render
from django.http import HttpResponse,HttpResponseRedirect
import json
from django.contrib.auth import authenticate,login,logout

from django.db.models import Q

from django.contrib.auth.models import User
from freepl.models import fplUser,fixtures,players,fixtureTeams
from django.core.validators import validate_email
from django.core.mail import send_mail

from mysite.settings import SEND_MAIL

def chkkey(dic,li):
	flag=1
	for l in li:
		if not dic.has_key(l):
			flag=0
			break
	return flag


def validate_team(teamconfig,teamname,fixtureid):
    try:
	fixture = fixtures.objects.get(id=fixtureid)
	teamconfig_list = map(int,teamconfig.split(','))
	teamconfig_list.pop()
	playersinfixture = player.filter(Q(country=teamA)|Q(country=teamB)).order_by('netperformance')
	
	#constraint parameters
	cons = {'bat': 0,'bowl':0,'wk':0,'allround':0, fixture.teamA:0,fixture.teamB:0,'price':0,'power':0}
	low_limits = {'bat':4,'bowl':2,'wk':1,'allround':2,fixture.teamA:0,fixture.teamB:0,'price':0,'power':1}
	up_limits = {'bat':11,'bowl':11,'wk':1,'allround':11,fixture.teamA:6,fixture.teamB:6,'price':850,'power':1}
	error_messages = {'bat':'Batsmen insufficient!','bowl':'Bowlers insufficient!','wk':'You must keep only one wicketkeeper!','allround':'Allrounders insufficient!',fixture.teamA:'aximum players from a single team exceeded!',fixture.teamB:'aximum players from a single team exceeded!','price':'Total Budget Exceeded!','power':'Must have one power player'}


	for i in xrange(len(teamconfig_list)):
	    cons[playersinfixture[i].role]+=1
	    cons['price']+=playersinfixture[i].price
	    cons[playersinfixture[i].country]+=1
	    if p[i]==2:
		cons['power']+=1
	    for key in cons:
		if (cons[key]>=low_limits[key] and cons[key]<=up_limits[key]) or key=='power':
		    continue
		else:
		    return error_messages[key]
	
	if cons['power']!=1:
	    return error_messages['power']
	
	return 'yes'
    except:
	return 'bad request'

def user_verify(request,activation_key):
	flag=0
	pwd=""
	#print "82ghzsF8itjyckjm9tVNbGLItbcFPckIxOhVbqtQFCI="
	#print User.objects.all().filter(username="tutogaya")[0].password
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
def home(request):
	if request.method=='GET':
	    #if logged in
	    if request.user.is_authenticated():
		"""
		here we need to add the various context parameters needed for 
		the template logged.html template which includes really the entire 
		content of the site 
		"""
		allfixtures = fixtures.objects.all()
		teamlists = []
		player_fixture = []
		teams = []

		playerlist = players.objects.order_by('netperformance')
		userfixtureteams = fixtureTeams.objects.filter(user=request.user)

		for fixture in allfixtures:
			teamA = fixture.teamA
			teamB = fixture.teamB
			playersinfixture = playerlist.filter(Q(country=teamA)|Q(country=teamB))
			#print playersinfixture
			#If the user made any fixture team
			teamconfig = []
			try:
			    userfixtureteam = fixtureTeams.objects.get(fixture=fixture,user=request.user)
			    s = userfixtureteam.teamconfig
			    teamconfig = map(int,s.split(','))
			    teamconfig.pop()
			    teams.append(userfixtureteam)
			
			#Complete new team
			except fixtureTeams.DoesNotExist:
			    #teamconfig 0-not selected, 1-selected, 2-powerplayer
			    n = len(playersinfixture)
			    s = '0,'*n
			    newfixtureteam = fixtureTeams()
			    newfixtureteam.user = fplUser.objects.get(id=request.user.id)#.objects.get(id = request.user.id)
			    newfixtureteam.fixture = fixture
			    newfixtureteam.teamname = ''
			    newfixtureteam.teamconfig = s[:-1]
			    newfixtureteam.save()

			    teamconfig = map(int,s[:-1].split(','))
			    teamconfig.pop()
			    teams.append(newfixtureteam)
			player_fixture.append(zip(teamconfig,playersinfixture))
			
		"""
		for obj in fplUser.objects.all():
			eachscore=0
			for team in fixtureTeams.objects.all():
			    if team.username==obj.username:
					eachscore+=team.score
			obj.cumulativescore=eachscore
			obj.save()
		"""
		
		"""
		following is a three-in-one list zipped into one.
		"""
		
		fixturewiseteams = zip(allfixtures,teams,player_fixture)
		return render(request,'main/logged.html',{"username":request.user.username,"fixturewiseteams":fixturewiseteams,"fixtures":allfixtures,"fplUsers":fplUser.objects.all(),"players":players.objects.all()})

	    else:
		return render(request,'startpage/start.html')

from django.contrib.auth.decorators import login_required

def login_(request):
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


def register(request):
	tmp=request.POST
	response_dict={"server_reponse":"no","server_message":"Data recieved was incomplete, check for errors!"}
	print "jh"
	if chkkey(tmp,['email','username','phone','password','passwordagain']):
		#check if user already exists
		"""
		to prevent the sending of large size data
		"""
		
		if len(tmp['username'])>30 or len(tmp['email'])>30 or len(tmp['password'])>30:
			response_dict.update({"server_message":"You have exceeded the limit for text entry. MaxLength: 30 chars "})
		elif fplUser.objects.filter(username=tmp['username']):
			response_dict.update({"server_message":"username already exists"})
		#check if the phone number is valid
		elif len(tmp['phone'])!=10:
			response_dict.update({"server_message":"Wrong Mobile Number"})
		#check if the password is not blank
		elif tmp['password']=="":
			response_dict.update({"server_message":"Password is blank"})
		#check if the password is matching the previous one
		elif tmp['passwordagain']!=tmp['password']:
			response_dict.update({"server_message":"Retyped password does not match"})
		#check if the email is unique 
		#if not validate_email("mayankgmail.com"):
		#	print "fucke "
		else:
		    try:
			validate_email(tmp['email'])
		    except:
			response_dict.update({"server_message":"Email is invalid"})
		    if fplUser.objects.filter(email=tmp['email']):
			response_dict.update({"server_message":"Email is already registered"})
		    else:
			#creating the User object
			user = fplUser.objects.create_user(tmp['username'], tmp['email'],tmp['password'])
			user.is_active = False
			user.phone = tmp['phonenumber']
			#print user.password+" ee "
			user.save()
			hexkey=(user.password.split('$')[3]).encode("hex")
			activation_url = "http://freepl.mkti.in/activate/"+hexkey    
			test_url = "http://localhost:8000/activate/"+hexkey
			"""
			we send email of the activation_url to the user email address here
			"""
			#creating the fplUser object
			if SEND_MAIL:
			    send_mail("Congratulations! You have been registered for FreePL 2014" , activation_url , 'freepl@mkti.com', [user.email], fail_silently = False)	
			else:#Testing
			    print "Activation Url ",test_url
			#userd=authenticate(username=tmp['username'],password=tmp['password'])
			#login(request,userd)
			response_dict.update({"server_response":"yes","server_message":"Registration Successful"})

	return HttpResponse(json.dumps(response_dict),mimetype='application/javascript')


def logout_(request):
	logout(request)
	response_dict={}
	return HttpResponse(json.dumps(response_dict),mimetype='application/javascript')

@login_required
def locktheteam(request):
	"""
	returns whether the team is lockable if not return the error
	and if lockable then lock it modify the dbs and return the successful
	team
	"""
	response_dict={'server_response':"no","server_message":"Bad Request!"}
	tmp=request.POST

	#Checking if the request has the desired keys.
	if chkkey(tmp,["teamconfig","teamname","fixtureid"]):
		print tmp["teamconfig"],tmp["fixtureid"],tmp["teamname"]
		tmp2=tmp["teamconfig"].split(',')
		
		val = validate_team(tmp["teamconfig"],tmp["fixtureid"],tmp["teamname"])
		if val=='yes':

		    if fixtureTeams.objects.filter(teamname = tmp["teamname"]):
			response_dict.update({"server_message":"Team name already exists!"})
		    else:
			fixture = fixtures.objects.get(id = tmp["fixtureid"])
			try:
			    alreadythere = fixtureTeams.objects.get(user=request.user,fixture = fixture)
			    alreadythere.teamconfig = tmp["teamconfig"]
			    alreadythere.teamname = tmp["teamname"]
			    alreadythere.save()

			except fixtures.DoesNotExist:
			    newfixtureteam = fixtureTeams()
			    newfixtureteam.teamconfig = tmp["teamconfig"]
			    newfixtureteam.teamname = tmp["teamname"]
			    newfixtureteam.user= request.user
			    newfixtureteam.fixture= fixture
			    newfixtureteam.save()

			response_dict.update({"server_message":"congos"})
			response_dict.update({"server_response":"yes"})
		else:
		    response_dict.update({"server_message":val})

	return HttpResponse(json.dumps(response_dict),mimetype='application/javascript')


from django.shortcuts import render
from django.http import HttpResponse,HttpResponseRedirect
import json
#from django.contrib.auth import authenticate,login,logout

from django.db.models import Q

from django.contrib.auth.models import User
from freepl.models import fplUser,fixtures,players,fixtureTeams
from django.core.validators import validate_email
from django.core.mail import send_mail
from fandjango.decorators import facebook_authorization_required



def chkkey(dic,li):
	flag=1
	for l in li:
		if not dic.has_key(l):
			flag=0
			break
	return flag


def validate_team(teamconfig,fixtureid,teamname):
    if teamname=='':
	return 'Team Name cannot be blank.'
    try:
	fixture = fixtures.objects.get(id=fixtureid)
	#print fixture
	teamconfig_list = map(int,teamconfig[:-1].split(','))
	playersinfixture = players.objects.filter(Q(country=fixture.teamA)|Q(country=fixture.teamB)).order_by('netperformance')
	if len(playersinfixture)!=len(teamconfig_list):
	    return 'lolwa'
	#constraint parameters
	cons = {'bat': 0,'bowl':0,'wk':0,'allround':0, fixture.teamA:0,fixture.teamB:0,'price':0,'power':0}
	low_limits = {'bat':4,'bowl':2,'wk':1,'allround':2,fixture.teamA:0,fixture.teamB:0,'price':0,'power':1}
	up_limits = {'bat':11,'bowl':11,'wk':1,'allround':11,fixture.teamA:6,fixture.teamB:6,'price':900,'power':1}
	error_messages = {'bat':'Batsmen insufficient!','bowl':'Bowlers insufficient!','wk':'You must keep only one wicketkeeper!','allround':'Allrounders insufficient!',fixture.teamA:'Maximum players from a single team exceeded!',fixture.teamB:'aximum players from a single team exceeded!','price':'Total Budget Exceeded!','power':'Must have one power player'}

	for i in xrange(len(teamconfig_list)):
	    if teamconfig_list[i]>0:
		#print playersinfixture[i].role
		cons[playersinfixture[i].role]+=1
		cons['price']+=playersinfixture[i].price
		cons[playersinfixture[i].country]+=1
		if teamconfig_list[i]==2:
		    cons['power']+=1

	for key in cons:
	    if (cons[key]>=low_limits[key] and cons[key]<=up_limits[key]) or key=='power':
		continue
	    else:
		return error_messages[key]+'Budget '+str(cons['price'])
	
	if cons['power']!=1:
	    return error_messages['power']
	return 'yes'
    except Exception as e:
	#print e
	return str(e)+' badrequest'
	
# Create your views here.
#@facebook_authorization_required
def home(request):
    if request.method=='GET':
	#if logged in
	if request.facebook:
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
	    userfixtureteams = fixtureTeams.objects.filter(user=request.facebook.user)
	    username = request.facebook.user.first_name
	    for fixture in allfixtures:
		teamA = fixture.teamA
		teamB = fixture.teamB
		playersinfixture = playerlist.filter(Q(country=teamA)|Q(country=teamB))
		#print playersinfixture
		#If the user made any fixture team
		teamconfig = []
		#print fixture
		obj, created = fixtureTeams.objects.get_or_create(user=fplUser.objects.get(user=request.facebook.user),fixture = fixture)
		if created:
		    #print obj,"new"
		    obj.user = fplUser.objects.get(user=request.facebook.user)
		    obj.fixture = fixture
		    obj.teamname = ''
		    obj.teamconfig = '0,'*len(playersinfixture)
		    obj.save()

		    teamconfig = map(int,obj.teamconfig[:-1].split(','))
		    teams.append(obj)

		else:
		    #print obj,"created"
		    s = obj.teamconfig		    
		    teams.append(obj)
		    teamconfig = map(int,s[:-1].split(','))
		    """
		    following is a three-in-one list zipped into one.
		    """
		player_fixture.append(zip(teamconfig,playersinfixture))
	    fixturewiseteams = zip(allfixtures,teams,player_fixture)
	    return render(request,'main/logged.html',{"name":username,"fixturewiseteams":fixturewiseteams,"fixtures":allfixtures,"fplUsers":fplUser.objects.all(),"players":players.objects.all()})

	else:
	    return render(request,'startpage/start.html')


@facebook_authorization_required
def authorize(request):
    response_dict={'server_response': "no" }
    try:
	ui = fplUser.objects.get(user = request.facebook.user)
	response_dict={'server_response': "yes" }
    except:
	user = fplUser(user = request.facebook.user, cumulativescore = 0)
	user.save()
    return HttpResponseRedirect('/')

def logout_(request):
	request.facebook = None
	return HttpResponseRedirect('/')

#@facebook_authorization_required
def locktheteam(request):
	"""
	#returns whether the team is lockable if not return the error
	#and if lockable then lock it modify the dbs and return the successful
	#team
	"""
	response_dict={'server_response':"no","server_message":"Bad Request!"}
	tmp=request.POST
	if request.facebook:
	    #Checking if the request has the desired keys.
	    print tmp
	    if chkkey(tmp,["teamconfig","teamname","fixtureid"]):
		    #print tmp["teamconfig"],tmp["fixtureid"],tmp["teamname"]
		    val = validate_team(tmp["teamconfig"],tmp["fixtureid"],tmp["teamname"])
		    if val=='yes':
			tm = None
			try:
			    tmp = fixtureTeams.objects.get(teamname = tmp["teamname"])
			    if tmp.user.user != request.facebook.user:
				response_dict.update({"server_message":"Team name already exists!"})
			except:
			    pass
			fixture = fixtures.objects.get(id = tmp["fixtureid"])
			#print 'finally'
			team_  = None
			try:
			    team_ = fixtureTeams.objects.get(user=request.facebook.user,fixture = fixture)
			except fixtures.DoesNotExist:
			team_ = fixtureTeams()
			team_.teamconfig = tmp["teamconfig"]
			team_.teamname = tmp["teamname"]
			team_.user= fplUser.objects.get(user=request.facebook.user)
			team_.fixture= fixture
			team_.save()

			response_dict.update({"server_message":"congos"})
			response_dict.update({"server_response":"yes"})
		    else:
			response_dict.update({"server_message":val})

	return HttpResponse(json.dumps(response_dict),mimetype='application/javascript')


from django.contrib import admin
from freepl.models import fplUser,fixtures,fixtureCricketPlayers,\
CricketPlayer,fixtureTeams
from scoreeval import mainscore


"""
update action for the fixtureTeams class. 
What does it do ? It takes data from the fixtureCricketPlayers table
and calculates the score of each team for each fixture.
"""
def update_scores_of_fixture_teams(modeladmin, request, queryset):
	allfixCP=fixtureCricketPlayers.objects.all().order_by('fixtureid')

	for fixture in fixtures.objects.all():
		curfixCP=allfixCP.filter(fixtureid=fixture.fixtureid)
		curfixteams=queryset.filter(fixtureid=fixture.fixtureid)
		for team in curfixteams:
			plyrids=team.teamconfig.split(',')
			teamname=team.teamname
			username=team.username
			del plyrids[11]
			points=0
			tmp=0
			for plyrid in plyrids:
				#print curfixCP.get(playerid=plyrid).funscore
				try:
					tmp=curfixCP.get(playerid=plyrid).funscore
				except:
					tmp=0
				points+=tmp
			
			try:
				points+=curfixCP.get(playerid=powerpid).funscore
			except:
				points+=0
			queryset.filter(fixtureid=fixture.fixtureid).filter(teamname=teamname).update(score=points)
			#fplUser.objects.all().filter(username=username).update(cumulativescore=cumulativescore+points)
			fu=fplUser.objects.filter(username=username)
			print fu
			print points
			fu[0].cumulativescore+=points
			fu[0].save()
"""
this updates the funscore field for each entry in the 
fixtureCricketPlayer table.
"""
def update_scores_of_cricket_plys(modeladmin, request, queryset):
	cal=mainscore()
	queryset.update(funscore=cal.do(runsmade,wickets,ballsfaced,fours,\
	sixes,oversbowled,maidenovers,runsgiven,catches,stumpings,runouts,dotsbowled,mom,dnb))
	
	
class fplUserAdmin(admin.ModelAdmin):
	list_display=('username','email','recentscore','cumulativescore','phonenumber')
	list_display_links=['username']
	list_editable=('email','recentscore','cumulativescore','phonenumber')

class CricketPlayerAdmin(admin.ModelAdmin):
	list_display=('firstname','lastname','playerid','country','role','netperformance','price')
	list_display_links=['playerid']
	list_editable=('firstname','lastname','country','role','netperformance','price')


class fixturesAdmin(admin.ModelAdmin):
	list_display=('fixtureid','teamA','teamB','isactive','isover')
	list_display_links=['fixtureid']
	list_editable=('teamA','teamB','isactive','isover')

class fixtureTeamsAdmin(admin.ModelAdmin):
	list_display=('fixtureid','username','teamname','teamconfig','powerpid','score')
	list_display_links=['fixtureid']
	list_editable=('username','teamname','score')
	actions=[update_scores_of_fixture_teams]

class fixtureCricketPlayersAdmin(admin.ModelAdmin):
	list_display=('fixtureid','playerid','runsmade','wickets','ballsfaced','fours',\
	'sixes','oversbowled','maidenovers','runsgiven','catches','stumpings','runouts','dotsbowled','mom','funscore')
	list_display_links=['fixtureid','playerid']
	list_editable=('runsmade','wickets','ballsfaced','fours',\
	'sixes','oversbowled','maidenovers','runsgiven','catches','stumpings','runouts','dotsbowled','mom','funscore')
	#actions=[update_scores_of_cricket_plys]

	
admin.site.register(fplUser,fplUserAdmin)
admin.site.register(fixtures,fixturesAdmin)
admin.site.register(fixtureTeams,fixtureTeamsAdmin)
admin.site.register(fixtureCricketPlayers,fixtureCricketPlayersAdmin)
admin.site.register(CricketPlayer,CricketPlayerAdmin)
# Register your models here.

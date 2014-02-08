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
		print "dsdsd"
		print curfixteams
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
	for b in queryset:
		b.funscore=cal.do(b.runsmade,b.wickets,b.ballsfaced,b.fours,\
		b.sixes,b.oversbowled,b.maidenovers,b.runsgiven,b.catches,b.stumpings,b.runouts,b.dotsbowled,b.mom,b.dnb)
		print b.funscore
		b.save()
	
class fplUserAdmin(admin.ModelAdmin):
	list_display=('username','email','recentscore','cumulativescore','phonenumber')
	list_display_links=['username']
	list_editable=('email','recentscore','cumulativescore','phonenumber')

class CricketPlayerAdmin(admin.ModelAdmin):
	list_display=('firstname','lastname','playerid','country','role','netperformance','price')
	list_display_links=['playerid']
	list_editable=('firstname','lastname','country','role','netperformance','price')
	
	actions=['really_delete_selected','export_to_FixtureCricketPlayer']
	def get_actions(self, request):
	    actions = super(CricketPlayerAdmin, self).get_actions(request)
	    del actions['delete_selected']
	    return actions

	def really_delete_selected(self, request, queryset):
	    for obj in queryset:
		fixtureCricketPlayers.objects.filter(playerid=obj.playerid).delete()
		print "playerid",obj.id
		obj.delete()

	    if queryset.count() == 1:
		message_bit = "1 photoblog entry was"
	    else:
		message_bit = "%s photoblog entries were" % queryset.count()
	    self.message_user(request, "%s successfully deleted." % message_bit)
	really_delete_selected.short_description = "Delete selected entries"
	
	def export_to_FixtureCricketPlayer(self, request, queryset):
	    for fixture in fixtures.objects.all():
		for obj in queryset:
		    if obj.country==fixture.teamA or obj.country==fixture.teamB:
			fcp=fixtureCricketPlayers(firstname=obj.firstname,lastname=obj.lastname,playerid=obj.playerid,fixtureid=fixture.fixtureid,\
			country=obj.country,mom=False,runsmade=0,wickets=0,ballsfaced=0,fours=0,sixes=0,oversbowled=0,\
			maidenovers=0,runsgiven=0,catches=0,stumpings=0,runouts=0,dotsbowled=0,\
			funscore=0,dnb=True)
			fcp.save()


class fixturesAdmin(admin.ModelAdmin):
	list_display=('fixtureid','teamA','teamB','isactive','isover','nomoreteams','date')
	list_display_links=['fixtureid']
	list_editable=('teamA','teamB','isactive','isover','nomoreteams')
	
	actions=['really_delete_selected']
	def get_actions(self, request):
	    actions = super(fixturesAdmin, self).get_actions(request)
	    del actions['delete_selected']
	    return actions

	def really_delete_selected(self, request, queryset):
	    for obj in queryset:
		obj.delete()

	    if queryset.count() == 1:
		message_bit = "1 photoblog entry was"
	    else:
		message_bit = "%s photoblog entries were" % queryset.count()
	    self.message_user(request, "%s successfully deleted." % message_bit)
	really_delete_selected.short_description = "Delete selected entries"


class fixtureTeamsAdmin(admin.ModelAdmin):
	list_display=('fixtureid','username','teamname','teamconfig','powerpid','score')
	list_display_links=['fixtureid']
	list_editable=('username','teamname','score')
	actions=[update_scores_of_fixture_teams]

class fixtureCricketPlayersAdmin(admin.ModelAdmin):
	list_display=('fixtureid','playerid','firstname','lastname','country','dnb','runsmade','ballsfaced','fours',\
	'sixes','oversbowled','wickets','maidenovers','runsgiven','catches','stumpings','runouts','dotsbowled','mom','funscore')
	list_display_links=['fixtureid','playerid']
	list_editable=('dnb','runsmade','ballsfaced','fours',\
	'sixes','oversbowled','wickets','maidenovers','runsgiven','catches','stumpings','runouts','dotsbowled','mom','funscore')
	actions=[update_scores_of_cricket_plys]

	
admin.site.register(fplUser,fplUserAdmin)
admin.site.register(fixtures,fixturesAdmin)
admin.site.register(fixtureTeams,fixtureTeamsAdmin)
admin.site.register(fixtureCricketPlayers,fixtureCricketPlayersAdmin)
admin.site.register(CricketPlayer,CricketPlayerAdmin)
# Register your models here.

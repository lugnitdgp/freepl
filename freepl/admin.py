from django.contrib import admin
from freepl.models import fplUser,fixtures,playerstats,fixtureTeams,players,teams
from django.db.models import Q


"""
update action for the fixtureTeams class. 
What does it do ? It takes data from the fixtureCricketPlayers table
and calculates the score of each team for each fixture.
"""

def calculate_fun_score(playerstats):
    base_bat_score = playerstats.runsmade
    impact_bat_score = -5 if (playerstats.runsmade==0) and (not playerstats.dnb) else 0
    impact_bat_score += 2*playerstats.sixes
    milestone_bat_score = 0 if playerstats.runsmade<0 else int(playerstats.runsmade/25)*10
    pace_bat_score = playerstats.runsmade -playerstats.ballsfaced 
    
    ballsb = int(playerstats.oversbowled)
    ballsbowled = int((playerstats.oversbowled-ballsb)*10) + ballsb*6
    base_bowl_score = 20*playerstats.wickets
    #print base_bowl_score,"bowl"
    impact_bowl_score = playerstats.dotsbowled+20*playerstats.maidenovers
    #print impact_bowl_score,"impact"
    milestone_bowl_score = 10*(playerstats.wickets-1) if playerstats.wickets>0 else 0
    #print milestone_bowl_score,"milestone"
    pace_bowl_score = 2*(ballsbowled-playerstats.runsgiven) if ballsbowled-playerstats.runsgiven>0 \
    else ballsbowled-playerstats.runsgiven
    #print pace_bowl_score,"pace"
    #print base_bowl_score+impact_bowl_score+milestone_bowl_score+pace_bowl_score,"bowl"
    
    field = playerstats.catches*10+playerstats.stumpings*15+playerstats.runouts*10
    mom = int(playerstats.mom)*25

    return base_bat_score+base_bowl_score+impact_bat_score+impact_bowl_score+\
    milestone_bowl_score+milestone_bat_score+pace_bowl_score+pace_bat_score+mom+field


class PlayerStatsListFilter(admin.SimpleListFilter):
    # Human-readable title which will be displayed in the
    # right admin sidebar just above the filter options.
    title = ('Fixture Filter')

    # Parameter for the filter that will be used in the URL query.
    parameter_name = 'fixture'
    allfixtures = fixtures.objects.all()
    
    def lookups(self, request, model_admin):
        """
        Returns a list of tuples. The first element in each
        tuple is the coded value for the option that will
        appear in the URL query. The second element is the
        human-readable name for the option that will appear
        in the right sidebar.
        """
        tup=[]
        for fixture in self.allfixtures:
	    tup.append((fixture.id,fixture.teamA.country+' '+fixture.teamB.country+str(fixture.date)))
        return tuple(tup)

    def queryset(self, request, queryset):
        """
        Returns the filtered queryset based on the value
        provided in the query string and retrievable via
        `self.value()`.
        """
        # Compare the requested value (either '80s' or '90s')
        # to decide how to filter the queryset.
        if self.value()!=None:
	    return queryset.filter(fixture = fixtures.objects.get(id = self.value()))
	return queryset

class FixtureTeamsListFilter(admin.SimpleListFilter):
    # Human-readable title which will be displayed in the
    # right admin sidebar just above the filter options.
    title = ('Fixture Filter')

    # Parameter for the filter that will be used in the URL query.
    parameter_name = 'fixture'
    allfixtures = fixtures.objects.all()
    
    def lookups(self, request, model_admin):
        """
        Returns a list of tuples. The first element in each
        tuple is the coded value for the option that will
        appear in the URL query. The second element is the
        human-readable name for the option that will appear
        in the right sidebar.
        """
        tup=[]
        for fixture in self.allfixtures:
	    tup.append((fixture.id,fixture.teamA.country+' '+fixture.teamB.country+str(fixture.date)))
        return tuple(tup)

    def queryset(self, request, queryset):
        """
        Returns the filtered queryset based on the value
        provided in the query string and retrievable via
        `self.value()`.
        """
        # Compare the requested value (either '80s' or '90s')
        # to decide how to filter the queryset.
        # to decide how to filter the queryset.
        if self.value()!=None:
	    return queryset.filter(fixture = fixtures.objects.get(id = self.value()))
	return queryset

def fixtureteamscoreupdate(modeladmin,request,queryset):
    n=len(queryset)
    for i in xrange(n):
	fixtureteam = queryset[i]
	l = map(int,fixtureteam.teamconfig[:-1].split(','))
	playerlist = players.objects.order_by('netperformance')
	score = 0
	playersinfixture = list(playerlist.filter(Q(country=fixtureteam.fixture.teamA)|Q(country=fixtureteam.fixture.teamB)))

	for i in xrange(len(l)):
	    player = playersinfixture[i]#.objects.get(id=playersinfixture[i].id)
	    try:
		playerstats_ = playerstats.objects.get(player=player,fixture = fixtureteam.fixture)
		funscore = playerstats_.funscore
	    except:
		funscore = 0
	    print player.firstname,player.lastname,l[i]
	    score += funscore * l[i]
	fixtureteam.score = score
	fixtureteam.save()

def playerstatsupdate(modeladmin,request,queryset):
    n=len(queryset)
    for i in xrange(n):
	playerstats = queryset[i]
	playerstats.funscore = calculate_fun_score(playerstats)
	playerstats.save()

def playerstatsentry(modeladmin,request,queryset):
    n=len(queryset)
    for i in xrange(n):
	fixture = queryset[i]
	playersinfixture = players.objects.filter(Q(country=fixtureteam.fixture.teamA)|Q(country=fixtureteam.fixture.teamB))
	url = fixture.url
	playerstats = scorecard_getter(url)
	'save each stat'
	for key in playerstats:
	    space = key.find(' ')
	    firstname = key[:space]
	    lastname = key[space+1:]
	    player=None
	    try:
		player = playersinfixture.objects.get(firstname = firstname,lastname = lastname)
	    except:
		raise Exception('Player '+firstname+lastname+' could not be found in database!')
	    ps = playerstats(fixture = fixture,player = player,**playerstats[key])
	    ps.save()

def cumulativescoreupdate(modeladmin,request,queryset):
    n=len(queryset)
    for i in xrange(n):
	user = queryset[i]
	allfixtureteamsofuser = fixtureTeams.objects.filter(user=user)
	m = len(allfixtureteamsofuser)
	cums = 0
	for j in xrange(m):
	    cums += allfixtureteamsofuser[j].score
	user.cumulativescore = cums
	user.save()

def netperformanceupdate(modeladmin,request,queryset):
    n=len(queryset)
    for i in xrange(n):
	player = queryset[i]
	allmatches = playerstats.objects.filter(player=player)
	m = len(allmatches)
	cums = 0
	for j in xrange(m):
	    cums += allmatches[j].score
	player.cumulativescore = cums
	player.save()

class fplUserAdmin(admin.ModelAdmin):
    list_display = ('user','cumulativescore')
    list_display_links = ['user']
    list_editable = ('cumulativescore',)
    actions = [cumulativescoreupdate]

class playersAdmin(admin.ModelAdmin):
    list_display = ('id','firstname','lastname','country','role','netperformance','price')
    list_display_links = ['id']
    list_editable = ('firstname','lastname','country','role','netperformance','price')
    actions = [netperformanceupdate]


class fixturesAdmin(admin.ModelAdmin):
    list_display = ('id','teamA','teamB','active','locked','date')
    list_display_links = ['id']
    list_editable = ('teamA','teamB','active','locked','date')
    actions = [playerstatsentry]

class fixtureTeamsAdmin(admin.ModelAdmin):
    list_display = ('user','teamname','score')
    list_display_links = ['user']
    list_editable = ('teamname','score')
    list_filter = (FixtureTeamsListFilter,)
    actions = [fixtureteamscoreupdate] 


class playerstatsAdmin(admin.ModelAdmin):
    list_display = ('player','fixture','runsmade','wickets' ,'ballsfaced' ,'fours' ,'sixes' ,'oversbowled','maidenovers' ,'runsgiven' ,'catches' ,'stumpings' ,'runouts' ,'dotsbowled' ,'mom','dnb' ,'funscore') 
    list_display_links = ['player']
    list_editable = ('fixture','runsmade','wickets' ,'ballsfaced' ,'fours' ,'sixes' ,'oversbowled','maidenovers' ,'runsgiven' ,'catches' ,'stumpings' ,'runouts' ,'dotsbowled' ,'mom','dnb' ,'funscore') 
    list_filter = (PlayerStatsListFilter,)
    actions = [playerstatsupdate]

admin.site.register(fplUser,fplUserAdmin)
admin.site.register(fixtures,fixturesAdmin)
admin.site.register(fixtureTeams,fixtureTeamsAdmin)
admin.site.register(players,playersAdmin)
admin.site.register(playerstats,playerstatsAdmin)
admin.site.register(teams)

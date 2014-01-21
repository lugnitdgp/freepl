from django.db import models
from django.db.models import Q

"""
**************
#we must note that the team name and configuration are valid only for
#one fixture and becomes invalid outside that fixture
**************
"""

# Create your models here.

#used for storing phone numbers and cumulative standings of each username
class fplUser(models.Model):
	username=models.CharField(max_length=100)
	email=models.EmailField(max_length=100)
	phonenumber=models.CharField(max_length=20)
	cumulativescore=models.PositiveSmallIntegerField()	
	recentscore=models.PositiveSmallIntegerField()	

	def __unicode__(self):
		return (self.username)

#to be used in per fixture standings
class fixtureTeams(models.Model):
	fixtureid=models.CharField(max_length=5,blank=True)	
	username=models.CharField(max_length=100)
	teamname=models.CharField(max_length=100)
	teamconfig=models.CharField(max_length=700)
	createdon = models.DateTimeField(auto_now_add=True)
	powerpid=models.CharField(max_length=5)	
	score=models.PositiveSmallIntegerField()
	
	def __unicode__(self):
		return '%s %s ' % (self.username,self.teamname)

class CricketPlayer(models.Model):
	playerid=models.CharField(max_length=5,blank=True)
	firstname=models.CharField(max_length=30)
	lastname=models.CharField(max_length=30)
	country=models.CharField(max_length=50)
	role=models.CharField(max_length=50)
	netperformance=models.PositiveSmallIntegerField()
	price=models.PositiveSmallIntegerField()

	def __unicode__(self):
		return '%s %s' % (self.firstname,self.lastname)

	def save(self, *args, **kwargs):
		super(CricketPlayer, self).save(*args, **kwargs) # Call the "real" save() method.
		self.playerid="p"+str(self.id)
		print "new player added"
		super(CricketPlayer, self).save(*args, **kwargs) # Call the "real" save() method.
		for fixture in fixtures.objects.all():
			if(fixture.teamA==self.country or fixture.teamB==self.country):
				if fixtureCricketPlayers.objects.filter(playerid=self.playerid,fixtureid=fixture.fixtureid):
					print "fixtureid and playerid, already exist, hence insertion skipped"
				else:
					print self.playerid,fixture.fixtureid
					fcp=fixtureCricketPlayers(playerid=self.playerid,fixtureid=fixture.fixtureid,\
					mom=False,runsmade=0,wickets=0,ballsfaced=0,fours=0,sixes=0,oversbowled=0,\
					maidenovers=0,runsgiven=0,catches=0,stumpings=0,runouts=0,dotsbowled=0,\
					funscore=0,dnb=0)
					fcp.save()
#table is useless for displaying purpose in django admin
#But is heavily used for calculating scores for each team in a fixture

class fixtureCricketPlayers(models.Model):
	playerid=models.CharField(max_length=5,blank=True)	
	fixtureid=models.CharField(max_length=5,blank=True)
	firstname=models.CharField(max_length=30)
	lastname=models.CharField(max_length=30)
	runsmade=models.PositiveSmallIntegerField()
	wickets=models.PositiveSmallIntegerField()
	ballsfaced=models.PositiveSmallIntegerField()
	fours=models.PositiveSmallIntegerField()
	sixes=models.PositiveSmallIntegerField()
	oversbowled=models.PositiveSmallIntegerField()
	maidenovers=models.PositiveSmallIntegerField()
	runsgiven=models.PositiveSmallIntegerField()
	catches=models.PositiveSmallIntegerField()
	stumpings=models.PositiveSmallIntegerField()
	runouts=models.PositiveSmallIntegerField()
	dotsbowled=models.PositiveSmallIntegerField()
	mom=models.BooleanField()
	dnb=models.BooleanField()
	funscore=models.PositiveSmallIntegerField()
	
	def __unicode__(self):
		return u'%s %s' % (self.playerid,self.fixtureid)


class fixtures(models.Model):
	fixtureid=models.CharField(max_length=5,blank=True)
	isactive=models.BooleanField()
	isover=models.BooleanField()
	nomoreteams=models.BooleanField()
	teamA=models.CharField(max_length=100)
	teamB=models.CharField(max_length=100)
	date=models.CharField(max_length=20)
	
	def __unicode__(self):
		return u'%s %s'%(self.teamA,self.teamB)

	def save(self, *args, **kwargs):
		super(fixtures, self).save(*args, **kwargs) # Call the "real" save() method.
		self.fixtureid="f"+str(self.id)
		super(fixtures, self).save(*args, **kwargs) # Call the "real" save() method.
		"""
		updating the fixtureCricketPlayers, using this and CricketPlayer
		"""
		tobeinsert=CricketPlayer.objects.filter(Q(country=self.teamA)|Q(country=self.teamB))
		tobeinsert=list(tobeinsert)
		"""
		inserting the players as soon as the fixture is made
		"""
		for c in tobeinsert:
			if fixtureCricketPlayers.objects.filter(playerid=c.playerid,fixtureid=self.fixtureid):
				 print "fixtureid and playerid, already exist, hence insertion skipped"
			else:
				  fcp=fixtureCricketPlayers(playerid=c.playerid,fixtureid=self.fixtureid,\
				  mom=False,runsmade=0,wickets=0,ballsfaced=0,fours=0,sixes=0,oversbowled=0,\
				  maidenovers=0,runsgiven=0,catches=0,stumpings=0,runouts=0,dotsbowled=0,\
				  funscore=0,dnb=0)
				  fcp.save()

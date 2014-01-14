from django.db import models

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
		super(CricketPlayer, self).save(*args, **kwargs) # Call the "real" save() method.

#table is useless for displaying purpose in django admin
#But is heavily used for calculating scores for each team in a fixture
#we must note that the team name and configuration are valid only for
#one fixture and becomes invalid outside that fixture
class fixtureCricketPlayers(models.Model):
	playerid=models.CharField(max_length=5,blank=True)	
	fixtureid=models.CharField(max_length=5,blank=True)
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
	funscore=models.PositiveSmallIntegerField()
	
	def __unicode__(self):
		return u'%s %s' % (self.playerid,self.fixtureid)
		
	
	def save(self, *args, **kwargs):
		self.playerid="p"+str(self.id)
		self.fixtureid="f"+str(self.id)
		super(fixtureCricketPlayers, self).save(*args, **kwargs) # Call the "real" save() method.

class fixtures(models.Model):
	fixtureid=models.CharField(max_length=5,blank=True)
	isactive=models.BooleanField()
	isover=models.BooleanField()
	teamA=models.CharField(max_length=100)
	teamB=models.CharField(max_length=100)
	date=models.CharField(max_length=20)
	
	def __unicode__(self):
		return u'%s %s'%(self.teamA,self.teamB)

	def save(self, *args, **kwargs):
		self.fixtureid="f"+str(self.id)
		super(fixtures, self).save(*args, **kwargs) # Call the "real" save() method.

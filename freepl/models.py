from django.db import models
from django.db.models import Q

from fandjango.models import User

from django.core.exceptions import ValidationError
"""
**************
#we must note that the team name and configuration are valid only for
#one fixture and becomes invalid outside that fixture
**************
"""

# Create your models here.

#used for storing phone numbers and cumulative standings of each username
class FplUser(models.Model):
    user = models.ForeignKey(User)
    cumulativescore = models.IntegerField(default=0)

    def __unicode__(self):
	return (self.user.first_name+' '+self.user.last_name)

class Teams(models.Model):
    country = models.CharField(max_length=20)
    flag = models.ImageField(upload_to='countries/')
    def __unicode__(self):
	return self.country

class Fixtures(models.Model):
    active = models.BooleanField(default=False)
    locked = models.BooleanField(default=False)
    teamA = models.ForeignKey(teams,related_name='teamA')
    teamB = models.ForeignKey(teams,related_name='teamB')
    date = models.DateTimeField()
    url = models.CharField(max_length=500,default='')

    def __unicode__(self):
	return '%s %s %s' % (self.teamA.country,self.teamB.country,self.date)

    def save(self,*args,**kwargs):
	if self.teamA==self.teamB:
	    raise ValidationError('Team A and Team B cannot be the same!')
	else:
	    super(fixtures,self).save(*args,**kwargs)

class FixtureTeams(models.Model):
    fixture = models.ForeignKey(fixtures)
    user = models.ForeignKey(fplUser)
    teamname = models.CharField(max_length=100)
    teamconfig = models.CharField(max_length=700)
    createdon = models.DateTimeField(auto_now_add=True)
    updatedon = models.DateTimeField(auto_now=True)
    score=models.IntegerField(default=0)

    def __unicode__(self):
	return '%s %s %s %s' % (self.user.user.first_name+' '+self.user.user.last_name,self.teamname,self.fixture.teamA.country,self.fixture.teamB.country)


class Players(models.Model):
    ROLES = (('bat', 'Batsmen'),('bowl','Bowler'),('wk','Wicket Keeper'),('allround','All Rounder'))
    firstname = models.CharField(max_length=50)
    lastname = models.CharField(max_length=50)
    country = models.ForeignKey(teams)
    role = models.CharField(max_length=8, choices=ROLES)
    netperformance = models.IntegerField(default=0)
    price = models.PositiveSmallIntegerField()

    def __unicode__(self):
	return '%s %s %s' % (self.firstname,self.lastname,self.role)

#table is useless for displaying purpose in django admin
#But is heavily used for calculating scores for each team in a fixture

class Playerstats(models.Model):
    player = models.ForeignKey(players)
    fixture = models.ForeignKey(fixtures)
    runsmade = models.PositiveSmallIntegerField(default=0)
    wickets = models.PositiveSmallIntegerField(default=0)
    ballsfaced = models.PositiveSmallIntegerField(default=0)
    fours = models.PositiveSmallIntegerField(default=0)
    sixes = models.PositiveSmallIntegerField(default=0)
    oversbowled = models.DecimalField(max_digits=3,decimal_places=1,default=0)
    maidenovers = models.PositiveSmallIntegerField(default=0)
    runsgiven = models.PositiveSmallIntegerField(default=0)
    catches = models.PositiveSmallIntegerField(default=0)
    stumpings = models.PositiveSmallIntegerField(default=0)
    runouts = models.PositiveSmallIntegerField(default=0)
    dotsbowled = models.PositiveSmallIntegerField(default=0)
    mom = models.BooleanField(default=False)
    dnb = models.BooleanField(default=True)
    funscore = models.IntegerField(default=-1)

    def __unicode__(self):
	return '%s %s' % (self.player.firstname+' '+self.player.lastname,self.fixture.teamA.country+' '+self.fixture.teamB.country)

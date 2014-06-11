from django.db import models
#from geography.models import ZipCode

# Create your models here.
class Person(models.Model):
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)
    born = models.DateField(null=True, blank=True)
    nationality = models.CharField(max_length=30, null=True, blank=True)

    def __unicode__(self):  # Python 3: def __str__(self):
        return '%s %s' % (self.first_name, self.last_name)

    def _get_full_name(self):
        "Returns the person's full name."
        return '%s %s' % (self.first_name, self.last_name)

class Team(models.Model):
    name = models.CharField(max_length=30)
    category = models.CharField(max_length=30)
    players = models.ManyToManyField(Person, through='Player')

    def __unicode__(self):  # Python 3: def __str__(self):
        return self.name

class Player(models.Model):
    person = models.ForeignKey(Person)
    team = models.ForeignKey(Team)
    number = models.PositiveIntegerField(null=True, blank=True)

    def __unicode__(self):  # Python 3: def __str__(self):
        return unicode(self.person)

class Tournament(models.Model):
    name = models.CharField(max_length=50)
    country = models.CharField(max_length=30)
    city = models.CharField(max_length=30)
#   zip_code = models.ForeignKey(ZipCode)
    address = models.CharField(max_length=100, null=True, blank=True)
    date = models.DateField(null=True, blank=True)
    teams = models.ManyToManyField(Team)

    def __unicode__(self):  # Python 3: def __str__(self):
        return '%s (%s, %s)' % (self.name, self.city, self.country)

class Round(models.Model):
    number = models.PositiveIntegerField()
    teams = models.PositiveIntegerField()
    clase = models.PositiveIntegerField()

    def __unicode__(self):  # Python 3: def __str__(self):
        return '%s %s %s' % (self.number, self.teams, self.clase)

class Game(models.Model):
    local = models.ForeignKey(Team, related_name="local")
    visitor = models.ForeignKey(Team, related_name="visitor")
    local_score = models.SmallIntegerField()
    visitor_score = models.SmallIntegerField()
    #player_stadistics = models.ManyToManyField(Stadictic)
    tournament = models.ForeignKey(Tournament)
    round = models.ForeignKey(Round)

    def __unicode__(self):  # Python 3: def __str__(self):
        return '%s %s - %s %s' % (self.local, self.local_score, self.visitor_score, self.visitor)

class PlayerStadistic(models.Model):
    game = models.ForeignKey(Game)
    player = models.ForeignKey(Player)
    points = models.PositiveIntegerField(null=True, blank=True, default=0)
    assistances = models.PositiveIntegerField(null=True, blank=True, default=0)

    def __unicode__(self):  # Python 3: def __str__(self):
        return unicode(self.player)

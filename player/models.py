from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
#from geography.models import ZipCode

MIXED_OPEN = 'MX'
MENS_OPEN = 'MO'
WOMENS_OPEN = 'WO'
SENIOR_MIX = 'SMX'
SENIOR_MENS = 'SMO'
SENIOR_WOMENS = 'SWO'
TOUCH_DIVISION_CHOICES = (
    (MIXED_OPEN, 'Mixed Open'),
    (MENS_OPEN, 'Mens Open'),
    (WOMENS_OPEN, 'Womens Open'),
    (SENIOR_MIX, 'Senior Mix Open'),
    (SENIOR_MENS, 'Senior Mens Open'),
    (SENIOR_WOMENS, 'Senior Womes Open'),
    )

MALE = 'M'
FEMALE = 'F'
GENDER_CHOICES = (
    (MALE, 'Male'),
    (FEMALE, 'Female'),
    )

# Create your models here.
class Person(models.Model):
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)
    born = models.DateField(null=True, blank=True)
    nationality = models.CharField(max_length=30, null=True, blank=True)
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES, default = MALE)

    def __unicode__(self):  # Python 3: def __str__(self):
        return '%s %s' % (self.first_name, self.last_name)

    def _get_full_name(self):
        "Returns the person's full name."
        return '%s %s' % (self.first_name, self.last_name)

#class Category(models.Model):

class Team(models.Model):
    name = models.CharField(max_length=30)
    players = models.ManyToManyField(Person, through='Player')
    division = models.CharField(max_length=3, choices=TOUCH_DIVISION_CHOICES, default=MIXED_OPEN)    

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
    division = models.CharField(max_length=3, choices=TOUCH_DIVISION_CHOICES)

    def __unicode__(self):  # Python 3: def __str__(self):
        return '%s (%s, %s)' % (self.name, self.city, self.country)

class Phase(models.Model):
    name = models.CharField(default='Pool', max_length=20, null=True, blank=True)
    phase = models.PositiveIntegerField(default=1, validators=[MinValueValidator(0), MaxValueValidator(10)])
    teams = models.PositiveIntegerField(default=1, validators=[MinValueValidator(0), MaxValueValidator(20)])
    clase = models.PositiveIntegerField(default=1, validators=[MinValueValidator(0), MaxValueValidator(10)])

    def __unicode__(self):  # Python 3: def __str__(self):
        return '%s %s %s' % (self.number, self.teams, self.clase)

class Game(models.Model):
    local = models.ForeignKey(Team, related_name="local")
    visitor = models.ForeignKey(Team, related_name="visitor")
    local_score = models.SmallIntegerField()
    visitor_score = models.SmallIntegerField()
    #player_stadistics = models.ManyToManyField(Stadictic)
    tournament = models.ForeignKey(Tournament)
    phase = models.ForeignKey(Phase)

    def __unicode__(self):  # Python 3: def __str__(self):
        return '%s %s - %s %s' % (self.local, self.local_score, self.visitor_score, self.visitor)

class PlayerStadistic(models.Model):
    game = models.ForeignKey(Game)
    player = models.ForeignKey(Player)
    points = models.PositiveIntegerField(null=True, blank=True, default=0)
    assistances = models.PositiveIntegerField(null=True, blank=True, default=0)

    def __unicode__(self):  # Python 3: def __str__(self):
        return unicode(self.player)

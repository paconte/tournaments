from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
#from geography.models import ZipCode

MIXED_OPEN = 'Mixed Open'
MENS_OPEN = 'Mens Open'
WOMENS_OPEN = 'Womens Open'
SENIOR_MIX = 'Senior Mix Open'
SENIOR_MENS = 'Senior Mens Open'
SENIOR_WOMENS = 'Senior Womes Open'
TOUCH_DIVISION_CHOICES = (
    ('MXO', MIXED_OPEN),
    ('MO', MENS_OPEN),
    ('WO', WOMENS_OPEN),
    ('SMX', SENIOR_MIX),
    ('SMO', SENIOR_MENS),
    ('SWO', SENIOR_WOMENS),
    )

# Create your models here.
class Person(models.Model):
    MALE = 'M'
    FEMALE = 'F'
    GENDER_CHOICES = (
        (MALE, 'Male'),
        (FEMALE, 'Female'),
        )

    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)
    born = models.DateField(null=True, blank=True)
    nationality = models.CharField(max_length=30, null=True, blank=True)
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES, default = MALE)

    def __unicode__(self):  # Python 3: def __str__(self):
        return '%s - %s %s' % (self.gender, self.first_name, self.last_name)

    def _get_full_name(self):
        "Returns the person's full name."
        return '%s %s' % (self.first_name, self.last_name)

class Team(models.Model):
    name = models.CharField(max_length=30)
    players = models.ManyToManyField(Person, through='Player')
    division = models.CharField(max_length=3, choices=TOUCH_DIVISION_CHOICES)

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
        return '%s - %s (%s, %s)' % (self.division, self.name, self.city, self.country)

class GameRound(models.Model):
    FINAL = 'Final'
    SEMI = 'Semifinal'
    QUARTER = '1/4'
    EIGHTH = '1/8'
    SIXTEENTH = '1/16'
    THIRD_PLACE = 'Third position'
    FITH_PLACE = 'Fith position'
    SIXTH_PLACE = 'Sixth position'
    SEVENTH_PLACE = 'Seventh position'
    POOL_A = 'Pool A'
    POOL_B = 'Pool B'
    POOL_C = 'Pool C'
    POOL_D = 'Pool D'
    LIGA = 'Liga'

    GAME_ROUND_CHOICES = (
        (FINAL, FINAL),
        (SEMI, SEMI),
        (QUARTER, QUARTER),
        (EIGHTH, EIGHTH),
        (SIXTEENTH, SIXTEENTH),
        (THIRD_PLACE, THIRD_PLACE),
        (FITH_PLACE, FITH_PLACE),
        (SIXTH_PLACE, SIXTH_PLACE),
        (SEVENTH_PLACE, SEVENTH_PLACE),
        (POOL_A, POOL_A),
        (POOL_B, POOL_B),
        (POOL_C, POOL_C),
        (POOL_D, POOL_D),
        (LIGA, LIGA),
        )
    
    GOLD = 'Gold'
    SILVER = 'Silver'
    BRONZE = 'Bronze'

    CATEGORY_ROUND_CHOICES = (
        (GOLD, GOLD),
        (SILVER, SILVER),
        (BRONZE, BRONZE),
        )
    
    round = models.CharField(default=POOL_A, max_length=16, null=False, blank=False, choices=GAME_ROUND_CHOICES)
    number_teams = models.PositiveIntegerField(default=2, validators=[MinValueValidator(0), MaxValueValidator(20)])
    category = models.CharField(default=GOLD, max_length=6, null=False, blank=False, choices=CATEGORY_ROUND_CHOICES)

    def __unicode__(self):  # Python 3: def __str__(self):
        return '%s %s %s' % (self.round, self.number_teams, self.category)


class Game(models.Model):
    local = models.ForeignKey(Team, related_name="local")
    visitor = models.ForeignKey(Team, related_name="visitor")
    local_score = models.SmallIntegerField()
    visitor_score = models.SmallIntegerField()
    #player_stadistics = models.ManyToManyField(Stadictic)
    tournament = models.ForeignKey(Tournament)
    phase = models.ForeignKey(GameRound)

    def __unicode__(self):  # Python 3: def __str__(self):
        return '%s %s - %s %s' % (self.local, self.local_score, self.visitor_score, self.visitor)



class PlayerStadistic(models.Model):
    game = models.ForeignKey(Game)
    player = models.ForeignKey(Player)
    points = models.PositiveIntegerField(null=True, blank=True, default=0)
    assistances = models.PositiveIntegerField(null=True, blank=True, default=0)

    def __unicode__(self):  # Python 3: def __str__(self):
        return unicode(self.player)

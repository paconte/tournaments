from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator

DATA_FILES = './data_files/'

MIXED_OPEN = 'Mixed Open'
MEN_OPEN = 'Mens Open'
WOMEN_OPEN = 'Womens Open'
SENIOR_MIX = 'Senior Mix Open'
SENIOR_MEN = 'Senior Mens Open'
SENIOR_WOMEN = 'Senior Womes Open'
TOUCH_DIVISION_CHOICES = (
    ('MXO', MIXED_OPEN),
    ('MO', MEN_OPEN),
    ('WO', WOMEN_OPEN),
    ('SMX', SENIOR_MIX),
    ('SMO', SENIOR_MEN),
    ('SWO', SENIOR_WOMEN),
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
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES, default=MALE)

    def __str__(self):
        return '{:s} {:s} - {:s}'.format(self.first_name, self.last_name, self.gender)

    def _get_full_name(self):
        """Returns the person's full name."""
        return '{:s} {:s}'.format(self.first_name, self.last_name)


class Team(models.Model):
    name = models.CharField(max_length=30)
    players = models.ManyToManyField(Person, through='Player')
    division = models.CharField(max_length=3, choices=TOUCH_DIVISION_CHOICES)

    def __str__(self):
        return self.division + ' - ' + self.name


class Tournament(models.Model):
    name = models.CharField(max_length=50)
    country = models.CharField(max_length=30)
    city = models.CharField(max_length=30)
    #   zip_code = models.ForeignKey(ZipCode)
    address = models.CharField(max_length=100, null=True, blank=True)
    date = models.DateField(null=True, blank=True)
    teams = models.ManyToManyField(Team)
    division = models.CharField(max_length=3, choices=TOUCH_DIVISION_CHOICES)

    def __str__(self):
        if self.country and self.city:
            result = '{:s} - {:s} ({:s}, {:s})'.format(self.division, self.name, self.city, self.country)
        elif self.country:
            result = '{:s} - {:s} ({:s})'.format(self.division, self.name, self.country)
        elif self.city:
            result = '{:s} - {:s} ({:s})'.format(self.division, self.name, self.city)
        else:
            result = '{:s} - {:s}'.format(self.division, self.name)
        return result

    def get_division_name(self):
        for x in TOUCH_DIVISION_CHOICES:
            if self.division == x[0]:
                if 'MO' == x[0]:
                    return MEN_OPEN
                elif 'WO' == x[0]:
                    return WOMEN_OPEN
                elif 'MXO' == x[0]:
                    return MIXED_OPEN
                elif 'SMO' == x[0]:
                    return SENIOR_MEN
                elif 'SWO' == x[0]:
                    return SENIOR_WOMEN
                elif 'SMX' == x[0]:
                    return SENIOR_MIX
        assert "A name for the division: %s could not be found." % self.division


class Player(models.Model):
    person = models.ForeignKey(Person)
    team = models.ForeignKey(Team)
    number = models.PositiveIntegerField(null=True, blank=True)
    tournaments_played = models.ManyToManyField(Tournament, null=True, blank=True)

    def __str__(self):
        return '{:s},  {:s} {:s}'.format(str(self.team), str(self.number), str(self.person))


class GameRound(models.Model):
    FINAL = 'Final'
    SEMI = 'Semifinal'
    QUARTER = '1/4'
    EIGHTH = '1/8'
    SIXTEENTH = '1/16'
    THIRD_POSITION = 'Third position'
    FIFTH_POSITION = 'Fifth position'
    SIXTH_POSITION = 'Sixth position'
    SEVENTH_POSITION = 'Seventh position'
    EIGHTH_POSITION = 'Eighth position'
    NINTH_POSITION = 'Ninth position'
    TENTH_POSITION = 'Tenth position'
    ELEVENTH_POSITION = 'Eleventh position'
    TWELFTH_POSITION = 'Twelfth position'
    THIRTEENTH_POSITION = 'Thirteenth position'
    FOURTEENTH_POSITION = 'Fourteenth position'
    FIFTEENTH_POSITION = 'Fifteenth position'
    SIXTEENTH_POSITION = 'Sixteenth position'
    EIGHTEENTH_POSITION = 'Eighteenth position'
    TWENTIETH_POSITION = 'Nineteenth position'
    DIVISION = 'Division'
    POOL_A = 'Pool A'
    POOL_B = 'Pool B'
    POOL_C = 'Pool C'
    POOL_D = 'Pool D'
    LIGA = 'Liga'

    ordered_rounds = [FINAL, THIRD_POSITION, SEMI, FIFTH_POSITION, QUARTER, SIXTH_POSITION,
                      SEVENTH_POSITION, EIGHTH_POSITION, NINTH_POSITION, TENTH_POSITION,
                      ELEVENTH_POSITION, TWELFTH_POSITION, THIRTEENTH_POSITION, FOURTEENTH_POSITION,
                      FIFTEENTH_POSITION, SIXTEENTH_POSITION, EIGHTEENTH_POSITION, TWENTIETH_POSITION]

    GAME_ROUND_CHOICES = (
        (FINAL, FINAL),
        (SEMI, SEMI),
        (QUARTER, QUARTER),
        (EIGHTH, EIGHTH),
        (SIXTEENTH, SIXTEENTH),
        (THIRD_POSITION, THIRD_POSITION),
        (FIFTH_POSITION, FIFTH_POSITION),
        (SIXTH_POSITION, SIXTH_POSITION),
        (SEVENTH_POSITION, SEVENTH_POSITION),
        (EIGHTH_POSITION, EIGHTH_POSITION),
        (NINTH_POSITION, NINTH_POSITION),
        (TENTH_POSITION, TENTH_POSITION),
        (ELEVENTH_POSITION, ELEVENTH_POSITION),
        (TWELFTH_POSITION, TWELFTH_POSITION),
        (THIRTEENTH_POSITION, THIRTEENTH_POSITION),
        (FIFTEENTH_POSITION, FIFTEENTH_POSITION),
        (SIXTEENTH_POSITION, SIXTEENTH_POSITION),
        (EIGHTEENTH_POSITION, EIGHTEENTH_POSITION),
        (TWENTIETH_POSITION, TWENTIETH_POSITION),
        (DIVISION, DIVISION),
        (POOL_A, POOL_A),
        (POOL_B, POOL_B),
        (POOL_C, POOL_C),
        (POOL_D, POOL_D),
        (LIGA, LIGA),
    )

    GOLD = 'Gold'
    SILVER = 'Silver'
    BRONZE = 'Bronze'
    WOOD = 'Wood'

    CATEGORY_ROUND_CHOICES = (
        (GOLD, GOLD),
        (SILVER, SILVER),
        (BRONZE, BRONZE),
        (WOOD, WOOD),
    )

    round = models.CharField(default=POOL_A, max_length=20, null=False, blank=False, choices=GAME_ROUND_CHOICES)
    number_teams = models.PositiveIntegerField(default=2, validators=[MinValueValidator(0), MaxValueValidator(20)])
    category = models.CharField(default=GOLD, max_length=6, null=False, blank=False, choices=CATEGORY_ROUND_CHOICES)

    def __str__(self):
        return '{:s} {:d} {:s}'.format(str(self.round), self.number_teams, self.category)

    def is_pool(self):
        return self.round == self.POOL_A or self.round == self.POOL_B or self.round == self.POOL_C or self.round == self.POOL_D

    def __lt__(self, other):
        #        print('self = %s, other = %s' %(self, other))
        if self.category == other.category:
            if self.round == other.round:
                result = self.number_teams.__lt__(other.number_teams)
            else:
                if self.round == self.FINAL:
                    result = False
                elif other.round == self.FINAL:
                    result = True
                elif self.round == self.THIRD_POSITION:
                    result = False
                elif other.round == self.THIRD_POSITION:
                    result = True
                elif self.round == self.SEMI:
                    result = False
                elif other.round == self.SEMI:
                    result = True
                elif self.round == self.FIFTH_POSITION:
                    result = False
                elif other.round == self.FIFTH_POSITION:
                    result = True
                elif self.round == self.SIXTH_POSITION:
                    result = False
                elif other.round == self.SIXTH_POSITION:
                    result = True
                elif self.round == self.SEVENTH_POSITION:
                    result = False
                elif other.round == self.SEVENTH_POSITION:
                    result = True
                elif self.round == self.EIGHTH_POSITION:
                    result = False
                elif other.round == self.EIGHTH_POSITION:
                    result = True
                elif self.round == self.QUARTER:
                    result = False
                elif other.round == self.QUARTER:
                    result = True
                elif self.round == self.NINTH_POSITION:
                    result = False
                elif other.round == self.NINTH_POSITION:
                    result = True
                elif self.round == self.TENTH_POSITION:
                    result = False
                elif other.round == self.TENTH_POSITION:
                    result = True
                elif self.round == self.ELEVENTH_POSITION:
                    result = False
                elif other.round == self.ELEVENTH_POSITION:
                    result = True
                elif self.round == self.TWELFTH_POSITION:
                    result = False
                elif other.round == self.TWELFTH_POSITION:
                    result = True
                elif self.round == self.THIRTEENTH_POSITION:
                    result = False
                elif other.round == self.THIRTEENTH_POSITION:
                    result = True
                elif self.round == self.FIFTEENTH_POSITION:
                    result = False
                elif other.round == self.FIFTEENTH_POSITION:
                    result = True
                elif self.round == self.SIXTEENTH_POSITION:
                    result = False
                elif other.round == self.SIXTEENTH_POSITION:
                    result = True
                elif self.round == self.SIXTEENTH:
                    result = False
                elif other.round == self.SIXTEENTH:
                    result = True
                else:
                    raise Exception('Problem comparing values: %s and  %s' % (self.round, other.round))
        else:
            if self.category == self.GOLD:
                result = False
            elif other.category == self.GOLD:
                result = True
            elif self.category == self.SILVER:
                result = False
            elif other.category == self.SILVER:
                result = True
            elif self.category == self.BRONZE:
                result = False
            elif other.category == self.BRONZE:
                result = True
            elif self.category == self.WOOD:
                result = False
            else:
                raise Exception('Problem comparing values: %s and  %s' % (self.category, other.category))
        return result

    def __cmp__(self, other):
        #        print('self = %s, other = %s' %(self, other))
        if self.category == other.category:
            if self.round == other.round:
                result = self.number_teams.__cmp__(other.number_teams)
            else:
                if self.round == self.FINAL:
                    result = 1
                elif other.round == self.FINAL:
                    result = -1
                elif self.round == self.THIRD_POSITION:
                    result = 1
                elif other.round == self.THIRD_POSITION:
                    result = -1
                elif self.round == self.SEMI:
                    result = 1
                elif other.round == self.SEMI:
                    result = -1
                elif self.round == self.FIFTH_POSITION:
                    result = 1
                elif other.round == self.FIFTH_POSITION:
                    result = -1
                elif self.round == self.SIXTH_POSITION:
                    result = 1
                elif other.round == self.SIXTH_POSITION:
                    result = -1
                elif self.round == self.SEVENTH_POSITION:
                    result = 1
                elif other.round == self.SEVENTH_POSITION:
                    result = -1
                elif self.round == self.QUARTER:
                    result = 1
                elif other.round == self.QUARTER:
                    result = -1
                elif self.round == self.NINTH_POSITION:
                    result = 1
                elif other.round == self.NINTH_POSITION:
                    result = -1
                elif self.round == self.TENTH_POSITION:
                    result = 1
                elif other.round == self.TENTH_POSITION:
                    result = -1
                elif self.round == self.ELEVENTH_POSITION:
                    result = 1
                elif other.round == self.ELEVENTH_POSITION:
                    result = -1
                elif self.round == self.TWELFTH_POSITION:
                    result = 1
                elif other.round == self.TWELFTH_POSITION:
                    result = -1
                elif self.round == self.THIRTEENTH_POSITION:
                    result = 1
                elif other.round == self.THIRTEENTH_POSITION:
                    result = -1
                elif self.round == self.FIFTEENTH_POSITION:
                    result = 1
                elif other.round == self.FIFTEENTH_POSITION:
                    result = -1
                elif self.round == self.SIXTEENTH_POSITION:
                    result = 1
                elif other.round == self.SIXTEENTH_POSITION:
                    result = -1
                elif self.round == self.SIXTEENTH:
                    result = 1
                elif other.round == self.SIXTEENTH:
                    result = -1
                elif self.round == self.EIGHTEENTH_POSITION:
                    result = 1
                elif other.round == self.EIGHTEENTH_POSITION:
                    result = -1
                elif self.round == self.TWENTIETH_POSITION:
                    result = 1
                elif other.round == self.TWENTIETH_POSITION:
                    result = -1
                else:
                    raise Exception('Problem comparing values: %s and  %s' % (self.round, other.round))
        else:
            if self.category == self.GOLD:
                result = 1
            elif other.category == self.GOLD:
                result = -1
            elif self.category == self.SILVER:
                result = 1
            elif other.category == self.SILVER:
                result = -1
            elif self.category == self.BRONZE:
                result = 1
            elif other.category == self.BRONZE:
                result = -1
            elif self.category == self.WOOD:
                result = 1
            else:
                raise Exception('Problem comparing values: %s and  %s' % (self.category, other.category))
        return result


class GameField(models.Model):
    name = models.CharField(max_length=50, null=False, blank=False)

    def __str__(self):  # Python 3: def __str__(self):
        return '{}'.format(self.name)


class Game(models.Model):
    field = models.ForeignKey(GameField, blank=True, null=True)
    time = models.TimeField(blank=True, null=True)
    local = models.ForeignKey(Team, related_name="local", null=True, blank=True)
    visitor = models.ForeignKey(Team, related_name="visitor", null=True, blank=True)
    local_score = models.SmallIntegerField(null=True, blank=True)
    visitor_score = models.SmallIntegerField(null=True, blank=True)
    # player_stadistics = models.ManyToManyField(Stadictic)
    tournament = models.ForeignKey(Tournament)
    phase = models.ForeignKey(GameRound)

    def __str__(self):
        return '{} - {} - {} {} - {} {}'.format(
            self.tournament, self.phase, self.local, self.local_score, self.visitor_score, self.visitor)

    def __lt__(self, other):
        return self.phase.__lt__(other.phase)

    def __cmp__(self, other):
        return self.phase.__cmp__(other.phase)


class PlayerStadistic(models.Model):
    game = models.ForeignKey(Game)
    player = models.ForeignKey(Player)
    points = models.PositiveIntegerField(null=True, blank=True, default=0)
    assistances = models.PositiveIntegerField(null=True, blank=True, default=0)

    def __str__(self):
        return '{} - {} - touchdowns: {}'.format(self.game, self.player, self.points)


class Contact(models.Model):
    name = models.CharField(max_length=40, null=False, blank=False)
    email = models.EmailField(max_length=50, null=False, blank=False)
    where = models.CharField(max_length=20, null=True, blank=True)
    message = models.TextField(null=False, blank=False)

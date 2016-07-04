from django.core.exceptions import ValidationError
from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from django.utils.translation import ugettext_lazy as _

DATA_FILES = './data_files/'

MIXED_OPEN = 'Mixed Open'
MEN_OPEN = 'Mens Open'
WOMEN_OPEN = 'Womens Open'
SENIOR_MIX = 'Senior Mix Open'
MEN_30 = 'Mens 30'
MEN_40 = 'Mens 40'
SENIOR_WOMEN = 'Senior Womes Open'
WOMEN_27 = 'Women 27'
MXO = 'MXO'
MO = 'MO'
WO = 'WO'
SMX = 'SMX'
W27 = 'W27'
M30 = 'M30'
M40 = 'M40'
TOUCH_DIVISION_CHOICES = (
    (MXO, MIXED_OPEN),
    (MO, MEN_OPEN),
    (WO, WOMEN_OPEN),
    (SMX, SENIOR_MIX),
    (M30, MEN_30),
    (M40, MEN_40),
    (W27, WOMEN_27)
)


def get_player_gender(division):
    if division in [WO, W27]:
        result = Person.FEMALE
    elif division in [MO, M30, M40]:
        result = Person.MALE
    elif division in [MXO, SMX]:
        result = Person.UNKNOWN
    else:
        raise Exception("Division %s is not supported." % division)
    return result


# Create your models here.
class Person(models.Model):
    MALE = 'M'
    FEMALE = 'F'
    UNKNOWN = 'U'
    GENDER_CHOICES = (
        (MALE, 'Male'),
        (FEMALE, 'Female'),
        (UNKNOWN, None)
    )

    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)
    born = models.DateField(null=True, blank=True)
    nationality = models.CharField(max_length=30, null=True, blank=True)
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES, default=UNKNOWN, null=True)

    class Meta:
        ordering = ['gender', 'last_name', 'first_name']

    def __str__(self):
        return '{:s} {:s} - {:s}'.format(self.first_name, self.last_name, self.gender)

    def get_full_name(self):
        """Returns the person's full name."""
        return '{:s} {:s}'.format(self.first_name, self.last_name)

    def compare_name(self, other):
        """Returns True if both persons have the same full name otherwise False."""
        return self.get_full_name() == other.get_full_name()


class Team(models.Model):
    name = models.CharField(max_length=40)
    players = models.ManyToManyField(Person, through='Player')
    division = models.CharField(max_length=3, choices=TOUCH_DIVISION_CHOICES)

    def __str__(self):
        return self.division + ' - ' + self.name


class Tournament(models.Model):
    name = models.CharField(max_length=50)
    country = models.CharField(max_length=30)
    city = models.CharField(max_length=30)
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
                elif 'M30' == x[0]:
                    return MEN_30
                elif 'M40' == x[0]:
                    return MEN_40
                elif 'SMX' == x[0]:
                    return SENIOR_MIX
                elif 'W27' == x[0]:
                    return WOMEN_27

        assert "A name for the division: %s could not be found." % self.division

    def __lt__(self, other):
        if self.name >= other.name:
            result = False
        else:
            result = True
        return result


class Player(models.Model):
    person = models.ForeignKey(Person)
    team = models.ForeignKey(Team)
    number = models.PositiveSmallIntegerField(null=True, blank=True)
    tournaments_played = models.ManyToManyField(Tournament, null=True, blank=True)

    class Meta:
        ordering = ["person"]

    def __str__(self):
        return '{:s},  {:s} {:s}'.format(str(self.team), str(self.number), str(self.person))


class GameRound(models.Model):
    FINAL = 'Final'
    SEMI = 'Semifinal'
    QUARTER = '1/4'
    EIGHTH = 'Eighthfinals'
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
    TWENTIETH_POSITION = 'Twentieth position'
    DIVISION = 'Division'
    POOL_A = 'Pool A'
    POOL_B = 'Pool B'
    POOL_C = 'Pool C'
    POOL_D = 'Pool D'
    POOL_E = 'Pool E'
    POOL_F = 'Pool F'
    LIGA = 'Liga'

    ordered_rounds = [FINAL, THIRD_POSITION, SEMI, FIFTH_POSITION, QUARTER, SIXTH_POSITION,
                      SEVENTH_POSITION, EIGHTH_POSITION, EIGHTH, NINTH_POSITION, TENTH_POSITION,
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
        (POOL_E, POOL_E),
        (POOL_F, POOL_F),
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

    round = models.CharField(default=POOL_A, max_length=32, null=False, blank=False, choices=GAME_ROUND_CHOICES)
    number_teams = models.PositiveIntegerField(default=2, validators=[MinValueValidator(0), MaxValueValidator(20)])
    category = models.CharField(default=GOLD, max_length=6, null=False, blank=False, choices=CATEGORY_ROUND_CHOICES)

    def __str__(self):
        return '{:s} {:s} {:s}'.format(str(self.round), str(self.number_teams), str(self.category))

    def is_pool(self):
        return self.round == self.POOL_A or self.round == self.POOL_B or self.round == self.POOL_C or \
               self.round == self.POOL_D or self.round == self.POOL_E or self.round == self.POOL_F

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
                elif self.round == self.EIGHTEENTH_POSITION:
                    result = False
                elif other.round == self.EIGHTEENTH_POSITION:
                    result = True
                elif self.round == self.TWENTIETH_POSITION:
                    result = False
                elif other.round == self.TWENTIETH_POSITION:
                    result = True
                elif self.round == self.DIVISION:
                    result = False
                elif other.round == self.DIVISION:
                    result = True
                elif self.round in {self.POOL_A, self.POOL_B, self.POOL_C, self.POOL_D, self.POOL_E, self.POOL_F}:
                    result = False
                elif other.round in {self.POOL_A, self.POOL_B, self.POOL_C, self.POOL_D, self.POOL_E, self.POOL_F}:
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
    player = models.ForeignKey(Player)
    points = models.PositiveSmallIntegerField(null=True, blank=True, default=0)
    mvp = models.PositiveSmallIntegerField(null=True, blank=True, default=0)
    played = models.PositiveSmallIntegerField(null=True, blank=True, default=0)
    game = models.ForeignKey(Game, null=True)
    tournament = models.ForeignKey(Tournament, null=True)

    def clean(self):
        if not self.game or not self.tournament:
            raise ValidationError(_('PlayerStatistic must be related either to a game or to a tournament.'))

    def is_game_stat(self):
        return True if self.game else False

    def is_tournament_stat(self):
        return not self.is_game_stat()

    def __str__(self):
        if self.is_game_stat():
            return '{} - {} - touchdowns: {}'.format(self.game, self.player, self.points)
        else:
            return '{} - {} - touchdowns: {} - played: {} - mvp: {}'.format(self.tournament, self.player, self.points,
                                                                            self.played, self.mvp)


class Contact(models.Model):
    name = models.CharField(max_length=40, null=False, blank=False)
    email = models.EmailField(max_length=50, null=False, blank=False)
    where = models.CharField(max_length=20, null=True, blank=True)
    message = models.TextField(null=False, blank=False)

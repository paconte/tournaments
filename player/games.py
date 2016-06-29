import crypt
from time import strftime

from player import csvdata


def hashing():
    return crypt.crypt();


class DrawError(Exception):
    def __init__(self, value):
        self.value = value

    def __str__(self):
        return repr(self.value)


class Result:
    (TOUCH, TENNIS) = (0, 1)

    def __init__(self, local_score=None, visitor_score=None, kind=TOUCH):
        if kind == self.TOUCH:
            if not isinstance(local_score, int):
                raise ValueError("local_score must be an integer.")
            if isinstance(visitor_score, int):
                raise ValueError("visitor_score must be an integer.")
        elif kind == self.TENNIS:
            if isinstance(local_score, list):
                raise ValueError("visitor_score must be an list of integers.")
            if isinstance(visitor_score, list):
                raise ValueError("visitor_score list of integers.")
            if len(local_score != visitor_score):
                raise ValueError("local_score and visitor_score must have the same length.")
        else:
            raise ValueError("Wrong type argument")

        self.kind = kind
        self.local_score = local_score
        self.visitor_score = visitor_score

    def is_draw(self):
        try:
            self.get_winner()
        except DrawError:
            return True
        return False

    def get_winner(self):
        if self.kind == self.TOUCH:
            if self.local_score > self.visitor_score:
                return self.local
            elif self.local_score < self.visitor_score:
                return self.visitor
            else:
                raise DrawError("The game is a draw.")
        elif self.kind == self.TENNIS:
            local_sets, visitor_sets = 0
            for x in range(0, len(self.local_score)):
                if self.local_score[x] > self.visitor_score[x]:
                    local_sets += 1
                elif self.local_score[x] < self.visitor_score[x]:
                    visitor_sets += 1
            if local_sets > visitor_sets:
                return self.local
            elif local_sets < visitor_sets:
                return self.visitor
            else:
                raise DrawError("The game is a draw.")
            return local_sets == visitor_sets


class Game:
    def __init__(self):
        self.local = self.visitor = self.result = None
        self.round = self.category = self.n_teams = None
        self.t_name = self.division = None
        self.time_date = self.field = None

    def get_winner(self):
        return self.result.get_winner()

    def is_draw(self):
        return self.is_draw()

    def get_time(self):
        return strftime("%m/%d/%y", self.time_date)

    def get_date(self):
        return strftime("%H:%M", self.time_date)

    def get_touch_csv_list(self):
        result = list(range(13))
        result[csvdata.TG_TOURNAMENT_INDEX] = self.t_name
        result[csvdata.TG_DIVISION_INDEX] = self.division
        result[csvdata.TG_DATE_INDEX] = self.date
        result[csvdata.TG_TIME_INDEX] = self.time
        result[csvdata.TG_FIELD_INDEX] = self.field
        result[csvdata.TG_PHASE_INDEX] = self.round
        result[csvdata.TG_CATEGORY_INDEX] = self.category
        result[csvdata.TG_PHASE_TEAMS_INDEX] = self.n_teams
        result[8] = 'xx'
        result[csvdata.TG_LOCAL_TEAM_INDEX] = self.local
        result[csvdata.TG_LOCAL_TEAM_SCORE_INDEX] = self.local_score
        result[csvdata.TG_VISITOR_TEAM_SCORE_INDEX] = self.visitor_score
        result[csvdata.TG_VISITOR_TEAM_INDEX] = self.visitor
        return result

import csv
import os.path

from django.test import TestCase
from django.core import management

from player import csvWriter
from player import csvdata
from player import csvReader
from player import models
from player import games


# Create your tests here.
class CsvFileTest(TestCase):
    # fixtures = ['player.GameRound.json']

    def tearDown(self):
        directory = csvdata.RAW_STATS_FILES
        if os.path.exists(directory) and os.path.isdir(directory):
            for filename in os.listdir(directory):
                if filename.endswith('.csv.test'):
                    os.remove(filename)

    def setUp(self):
        # pass
        reader = csvReader.CsvReader(csvReader.CsvReader.PHASE)
        reader.read_file('./player/data_files/csv/TPhases.csv')

    def test_fox_tournament_WC_2015_WO_FOX(self):
        tournament = csvdata.WC_2015_WO_GAMES_FOX
        self.csv_fox_tournament(tournament)

    def test_fox_tournament_WC_2015_MO_FOX(self):
        tournament = csvdata.WC_2015_MO_GAMES_FOX
        self.csv_fox_tournament(tournament)

    def test_fox_tournament_WC_2015_MXO_FOX(self):
        tournament = csvdata.WC_2015_MXO_GAMES_FOX
        self.csv_fox_tournament(tournament)

    def test_fox_tournament_WC_2015_SMX_FOX(self):
        tournament = csvdata.WC_2015_SMX_GAMES_FOX
        self.csv_fox_tournament(tournament)

    def test_fox_tournament_WC_2015_W27_FOX(self):
        tournament = csvdata.WC_2015_W27_GAMES_FOX
        self.csv_fox_tournament(tournament)

    def test_fox_tournament_WC_2015_M30_FOX(self):
        tournament = csvdata.WC_2015_M30_GAMES_FOX
        self.csv_fox_tournament(tournament)

    def test_fox_tournament_NTL_2016_MO_FOX(self):
        tournament = csvdata.NTL_2016_MO_GAMES_FOX
        self.csv_fox_tournament(tournament)

    def test_fox_tournament_NTL_2016_WO_FOX(self):
        tournament = csvdata.NTL_2016_WO_GAMES_FOX
        self.csv_fox_tournament(tournament)

    def test_fit_euros_2014(self):
        self._test_fit_tournament_Euros_2014_MO()
        #self._test_fit_tournament_Euros_2014_M40()
        #self._test_fit_tournament_Euros_2014_WO()
        #self._test_fit_tournament_Euros_2014_W27()
        #self._test_fit_tournament_Euros_2014_MXO()
        #self._test_fit_tournament_Euros_2014_SMX()

    def test_padel_hamburg_2016(self):
        file = './player/data_files/csv/PADEL_HAMBURG_2016.csv'
        reader = csvReader.CsvReader(csvReader.CsvReader.PADEL_GAME)
        reader.read_file(file)

    def _test_fit_tournament_Euros_2014_MO(self):
        tournament = csvdata.EUROS_2014_MO
        self.csv_fit_tournament(tournament)
        self._test_fit_stats_Euros_2014(tournament)

    def _test_fit_tournament_Euros_2014_M40(self):
        tournament = csvdata.EUROS_2014_M40
        self.csv_fit_tournament(tournament)

    def _test_fit_tournament_Euros_2014_WO(self):
        tournament = csvdata.EUROS_2014_WO
        self.csv_fit_tournament(tournament)

    def _test_fit_tournament_Euros_2014_W27(self):
        tournament = csvdata.EUROS_2014_W27
        self.csv_fit_tournament(tournament)

    def _test_fit_tournament_Euros_2014_MXO(self):
        tournament = csvdata.EUROS_2014_MXO
        self.csv_fit_tournament(tournament)

    def _test_fit_tournament_Euros_2014_SMX(self):
        tournament = csvdata.EUROS_2014_SMX
        self.csv_fit_tournament(tournament)

    def _test_fit_stats_Euros_2014(self, tournament):
        #csvWriter.FitGamesManager.download_stats_html()
        manager = csvWriter.FitGamesManager(tournament)
        stats = manager.get_csv_statistics()

        writer = csvWriter.CsvWriter(tournament, True, True)
        writer.delete_filename_path()
        writer.write_csv(stats)
        reader = csvReader.CsvReader(csvReader.CsvReader.FIT_STATISTIC)
        reader.read_file(writer.get_filename_path())

    def Atest_NTS_stats(self):
        management.call_command('loaddata', './player/data_files/player.dumpdata.json', verbosity=0)
        filename = csvdata.CSV_FILES + 'NTS-player-statistics.csv'
        reader = csvReader.CsvReader(csvReader.CsvReader.NTS_STATISTIC)
        reader.read_file(filename)
        # management.call_command('flush', interactive=False, verbosity=0)

    def csv_fit_tournament(self, tournament):
        manager = csvWriter.FitGamesManager(tournament)
        manager.download_games_html()

        writer = csvWriter.CsvWriter(tournament, False, True)
        writer.delete_filename_path()
        writer.write_csv(manager.get_fit_games())

        reader = csvReader.CsvReader(csvReader.CsvReader.TOURNAMENT)
        reader.read_file(writer.get_filename_path())

    def csv_fox_tournament(self, tournament, games_download=False, stats_download=False):
        fox_manager = csvWriter.FoxGamesManager(tournament)
        if games_download:
            fox_manager.download_games_html()
        fox_manager.get_fox_games()
        if stats_download:
            fox_manager.download_statistics_html()
        fox_manager.get_csv_statistics()

        writer = csvWriter.CsvWriter(tournament, False)
        writer.delete_filename_path()
        writer.write_csv(fox_manager.get_fox_games())
        self.assertTrue(os.path.isfile(writer.get_filename_path()))

        reader = csvReader.CsvReader(csvReader.CsvReader.TOURNAMENT)
        reader.read_file(writer.get_filename_path())

        writer = csvWriter.CsvWriter(tournament, True)
        writer.delete_filename_path()
        writer.write_csv(fox_manager.get_csv_statistics())
        self.assertTrue(os.path.isfile(writer.get_filename_path()))

        reader = csvReader.CsvReader(csvReader.CsvReader.NTS_STATISTIC)
        reader.read_file(writer.get_filename_path())


class DbChecks(TestCase):
    fixtures = ['touch.db_dump.json']

    def test_find_conflicting_players(self):
        players = models.Player.objects.all()
        enum_players = list(enumerate(players))
        conflict_players = []
        discarded_players = []
        same_sex_conflicts = []
        different_sex_conflicts = []
        conflict_teams = dict()
        conflict_set = dict()

        for player1 in enum_players:
            add_player1 = False
            add_discard_player1 = False
            player1_add_same_sex = False
            player1_add_different_sex = False
            for player2 in enum_players[player1[0] + 1:]:
                if player1[1].person.compare_name(player2[1].person):
                    if player1[1].team == player2[1].team and player1[1].person.gender == player2[1].person.gender:
                        discarded_players.append(player2[1])
                        add_discard_player1 = True
                    else:
                        conflict_teams[player2[1].team] = True
                        conflict_players.append(player2[1])
                        if player1[1].person.gender == player2[1].person.gender:
                            same_sex_conflicts.append(player2[1])
                            player1_add_same_sex = True
                        else:
                            different_sex_conflicts.append(player2[1])
                            player1_add_different_sex = True
                        try:
                            new_value = conflict_set[player2[1].person.get_full_name()]
                            if player2[1] not in new_value:
                                new_value.append(player2[1])
                        except KeyError:
                            new_value = [player2[1]]
                        conflict_set[player2[1].person.get_full_name()] = new_value
                        add_player1 = True

            if add_player1:
                conflict_players.append(player1[1])
                new_value2 = conflict_set[player1[1].person.get_full_name()]
                if player1[1] not in new_value2:
                    new_value2.append(player1[1])
                conflict_set[player1[1].person.get_full_name()] = new_value2
                conflict_teams[player1[1].team] = True
            if add_discard_player1:
                discarded_players.append(player1[1])
            if player1_add_different_sex:
                different_sex_conflicts.append(player1[1])
            if player1_add_same_sex:
                same_sex_conflicts.append(player1[1])

        males = 0
        females = 0
        unks = 0

        for item in same_sex_conflicts:
            if item.person.gender == 'M':
                males += 1
            elif item.person.gender == 'F':
                females += 1
            elif item.person.gender == 'U':
                unks += 1
            else:
                Exception('Gender not allowed: %s' % item.person.gender)

        print('players=%s' % len(conflict_players))
        print('teams=%s' % len(conflict_teams))
        # for k in conflict_teams.keys():
        #    print(k)
        print('different_sex=%s' % len(different_sex_conflicts))
        # print(conflict_players)
        print('same_sex=%s, m=%s, f=%s, u=%s' % (len(same_sex_conflicts), males, females, unks))
        print('conflict_set=%s' % len(conflict_set))
        for k, v in conflict_set.items():
            print('####### %s #######\n' % k)
            for val in v:
                print('%s, person_id=%s, player_id=%s\n' % (val, str(val.person.id), str(val.id)))

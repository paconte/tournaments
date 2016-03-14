import os.path

from django.test import TestCase

from player import csvWriter
from player import csvdata
from player import csvReader


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
        reader = csvReader.CsvReader(csvReader.CsvReader.PHASE)
        reader.read_file('./player/data_files/csv/TPhases.csv', csvdata.CsvPhase)

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


    def csv_fox_tournament(self, tournament, games_download=False, stats_download=False):
        fox_manager = csvWriter.FoxGamesManager(tournament)
        if games_download:
            fox_manager.download_games_files()
        fox_manager.extract_raw_games()
        if stats_download:
            fox_manager.download_games_statistics()
        fox_manager.extract_statistics()

        writer = csvWriter.CsvWriter(tournament, False)
        writer.delete_filename_path()
        writer.write_csv(fox_manager.get_fox_games())
        self.assertTrue(os.path.isfile(writer.get_filename_path()))

        reader = csvReader.CsvReader(csvReader.CsvReader.TOURNAMENT)
        reader.read_file(writer.get_filename_path(), csvdata.CsvGame)

        writer = csvWriter.CsvWriter(tournament, True)
        writer.delete_filename_path()
        writer.write_csv(fox_manager.get_csv_statistics())
        self.assertTrue(os.path.isfile(writer.get_filename_path()))

        reader = csvReader.CsvReader(csvReader.CsvReader.NTS_STADISTIC)
        reader.read_file(writer.get_filename_path(), csvdata.CsvNTSStadistic)


        # class kkk(TestCase):
        #    pass

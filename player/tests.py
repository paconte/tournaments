import unittest
import os.path

from django.test import TestCase

from player import csvWriter
from player import csvdata
from player import csvReader


# Create your tests here.
class CsvFileTest(TestCase):
    def tearDown(self):
        pass

    #def setUp(self):
    #    reader = csvReader.CsvReader(csvReader.CsvReader.PHASE)
    #    reader.read_file('./player/data_files/csv/TPhases.csv', csvdata.CsvPhase)

    def test_csv_fox_tournament(self):
        tournament = csvWriter.FoxGamesManager.WC_2015_WO_FOX
        self.csv_fox_tournament(tournament)

    def csv_fox_tournament(self, tournament):
        fox_manager = csvWriter.FoxGamesManager(tournament)
        fox_manager.extract_raw_games()
        fox_manager.convert_fox_games_to_csv_games()
        #fox_manager.download_games_statistics()
        fox_manager.extract_statistics()

        writer = csvWriter.CsvWriter(tournament, False)
        writer.delete_path()
        writer.write_csv(fox_manager.get_csv_games())
        self.assertTrue(os.path.isfile(writer.get_path()))

        reader = csvReader.CsvReader(csvReader.CsvReader.PHASE)
        reader.read_file('./player/data_files/csv/TPhases.csv', csvdata.CsvPhase)

        reader = csvReader.CsvReader(csvReader.CsvReader.TOURNAMENT)
        reader.read_file(writer.get_path(), csvdata.CsvGame)

        writer = csvWriter.CsvWriter(tournament, True)
        writer.delete_path()
        writer.write_csv(fox_manager.get_csv_statistics())
        self.assertTrue(os.path.isfile(writer.get_path()))


#class kkk(TestCase):
#    pass
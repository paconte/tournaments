import argparse

from django.core.management.base import BaseCommand, CommandError

from player import csvdata
from player import csvReader


class Command(BaseCommand):
    help = 'Add csv data to the database.'

    def add_arguments(self, parser):
        parser.add_argument('type', choices=['games', 'phases', 'stats_game', 'stats_tournament'])
        parser.add_argument('file_path', nargs='+')

    def handle(self, *args, **options):
        csv_type = options['type']
        file_path = options['file_path'][0]

        self.stdout.write(self.style.SUCCESS('Read csv file: "%s"' % file_path))

        if csv_type == 'stats_game':
            reader = csvReader.CsvReader(csvReader.CsvReader.NTS_STATISTIC)
            reader.read_file(file_path, csvdata.CsvNTSStatistic)
        elif csv_type == 'stats_tournament':
            reader = csvReader.CsvReader(csvReader.CsvReader.FIT_STATISTIC)
            reader.read_file(file_path, csvdata.FitStatistic)
        elif csv_type == 'games':
            reader = csvReader.CsvReader(csvReader.CsvReader.TOURNAMENT)
            reader.read_file(file_path, csvdata.CsvGame)
        elif csv_type == 'phases':
            reader = csvReader.CsvReader(csvReader.CsvReader.PHASE)
            reader.read_file(file_path, csvdata.CsvPhase)
        else:
            raise Exception('Argument %s not supported.' % csv_type)

        self.stdout.write(self.style.SUCCESS('Successfully read csv file: "%s"' % file_path))

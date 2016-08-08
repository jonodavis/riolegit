from django.core.management import BaseCommand
import csv

from olympics import models


class Command(BaseCommand):
    def handle(self, *args, **options):
        with open('countries.csv', 'r') as f:
            reader = csv.DictReader(f)
            for row in reader:
                print("Loading country: %s, %s" % (row['Code'], row['Name']))
                models.Country.objects.create(code=row['Code'], name=row['Name'])

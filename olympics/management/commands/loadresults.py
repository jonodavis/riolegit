from django.core.management import BaseCommand

from ._resultparser import get_results


class Command(BaseCommand):
    def handle(self, *args, **options):
        get_results()

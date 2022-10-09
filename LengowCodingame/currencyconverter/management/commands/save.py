from django.core.management.base import BaseCommand
from currencyconverter.handler import CurrencyConverterInstance


class Command(BaseCommand):
    help = 'Save fetching result it into DB'

    def add_arguments(self, parser):
        parser.add_argument('conf', nargs='?')

    def handle(self, *args, **options):
        CurrencyConverterInstance.handle_save_source()

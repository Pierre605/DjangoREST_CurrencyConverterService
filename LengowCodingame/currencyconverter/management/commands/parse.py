from django.core.management.base import BaseCommand
from currencyconverter.handler import CurrencyConverterInstance


class Command(BaseCommand):
    help = 'Parse HTTP XML response'

    def add_arguments(self, parser):
        parser.add_argument('conf', nargs='?')

    def handle(self, *args, **options):
        CurrencyConverterInstance.handle_parse()

from currencyconverter.models import EuroRates, Source, Convert
from rest_framework import serializers


class SourceSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Source
        fields = ['content']

class EuroRatesSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = EuroRates
        fields = ['currency_name', 'rate', 'created_at']

class ConvertSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Convert
        fields = ['cur_in', 'cur_out', 'amount', 'res', 'answer', 'created_at']
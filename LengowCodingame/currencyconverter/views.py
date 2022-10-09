from currencyconverter.models import EuroRates
from currencyconverter.serializers import EuroRatesSerializer
from rest_framework.response import Response
from rest_framework import viewsets, permissions, status
from django_filters.rest_framework import DjangoFilterBackend
from currencyconverter.data_handler import data_handler
import json


class ConvertView(viewsets.ModelViewSet):
    queryset = EuroRates.objects.all()
    serializer_class = EuroRatesSerializer
    permission_classes = [permissions.AllowAny]
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['currency_name']

    def create(self, request, *args, **kwargs):
        if request.method == 'POST':
            if request.data.get('cur_in'):
                cur_in = request.data.get('cur_in')
                cur_out = request.data.get('cur_out')
                amount = request.data.get('amount')
                answer = data_handler(cur_in, cur_out, amount)
                print(answer)
                return Response(answer)
            else:
                data = json.dumps(request.data, indent=4)
                print(data)
                return Response(request.data, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

from currencyconverter.models import EuroRates
from currencyconverter.serializers import EuroRatesSerializer
from django.http import HttpResponse, JsonResponse
from rest_framework.response import Response
from rest_framework import viewsets, permissions, status
from django_filters.rest_framework import DjangoFilterBackend
from currencyconverter.data_handler import data_handler
import json



# class EuroRatesViewSet(viewsets.ModelViewSet):
# 	"""
# 	API endpoint that allows currencies to be viewed
# 	"""
# 	queryset = EuroRates.objects.all()
# 	serializer_class = EuroRatesSerializer
# 	filter_backends = [DjangoFilterBackend]
# 	filterset_fields = ['currency_name']


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
			
			# serializer_class = self.get_serializer_class()
			# serializer = serializer_class(data=request.data, context={'request': request})
			# serializer.is_valid(raise_exception=True)
			# data = {"status": True}
			# return Response(data)

			# print('HELLLOOO')
			# print(request.data)
			# serializer = self.get_serializer(data=request.data)
			# serializer.is_valid(raise_exception=True)
			# if serializer.is_valid():
			# 	print('post here')
			# 	print("serial_data:", serializer.data)
				# print("request_data:", request.data)
				# serializer.save()
			# 	return JsonResponse(serializer.data, status=status.HTTP_201_CREATED) 
			# return JsonResponse(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
		# if request.user.is_authenticated:
		# 	self.perform_create(serializer)
		# else:
		# 	raise PermissionDenied('Cannot post anonymously')

		# headers = self.get_success_headers(serializer.data)
		# return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)
		
		
		

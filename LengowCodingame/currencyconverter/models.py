from cgitb import lookup
from django.db import models
from django.conf import settings
from django.db.models import Q

User = settings.AUTH_USER_MODEL

class Source(models.Model):
	content = models.TextField(max_length=2000)
	created_at = models.DateTimeField('created_at')
	url = models.URLField(max_length=200)
	code = models.CharField(max_length=4)
	name = models.CharField(max_length=200)


class EuroRates(models.Model):
	currency_name = models.CharField(max_length=20, null=True)
	rate = models.DecimalField(max_digits=50, decimal_places=2, null=True)
	created_at = models.DateTimeField('created_at')


class Convert(models.Model):
	cur_in = models.CharField(max_length=20, null=True)
	cur_out = models.CharField(max_length=20, null=True)
	amount = models.FloatField(null=True)
	res = models.DecimalField(max_digits=70, decimal_places=2, null=True)
	answer = models.CharField(max_length=50, null=True)
	created_at = models.DateTimeField('created_at')


# class ConvertToEuroQuerySet(models.QuerySet):
# 	def search(self, query, user=None):
# 		lookup = Q(currency_name__icontains=query)
# 		qs = self.filter(lookup)
# 		if user is not None:
# 			qs = qs.filter(user=user)

# 		return qs

# class ConvertToEuroManager(models.Manager):
# 	def get_queryset(self, *args, **kwargs):
# 			return ConvertToEuroQuerySet(self.model, using=self.db)

# 	def search(self, query, user=None):
# 		return self.get_queryset().search(query, user=user)


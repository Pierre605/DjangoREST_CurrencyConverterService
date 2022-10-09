from ..models import EuroRates, Source, Convert
from django.utils import timezone


class SourceSaver:
    def save(content, url, status, name):
        Source.objects.create(
                content=content,
                created_at=timezone.now(),
                url=url,
                code=status,
                name=name
        )


class CurrenciesSaver:
    def save(name, rate):
        EuroRates.objects.update_or_create(
            currency_name=name,
            defaults={
                'created_at': timezone.now(),
                'rate': rate
            }
        )


class ConvertSaver:
    def save(cur_in, cur_out, amount, res):
        Convert.objects.create(
                cur_in=cur_in,
                created_at=timezone.now(),
                cur_out=cur_out,
                amount=amount,
                res=res
        )

from currencyconverter.models import Source, EuroRates
import json
from django.utils.timezone import datetime
import re


def data_handler(cur_in, cur_out, amount):
    data_list = EuroRates.objects.all()
    devises = []
    devises.append('EUR')
    for data in data_list:
        devises.append(data.currency_name)

    if cur_in in devises:
        amount = float(amount)
        if cur_out in devises:
            if cur_in == 'EUR':
                for cur in data_list:
                    if cur_out == cur.currency_name:
                        res = round(float(int(amount) * cur.rate), 2)
                        answer = f"{amount} EUR = {res} {cur.currency_name}"

                        # print('HANDLER HERE')

                        return json.dumps({'answer': answer}, indent=4)
            else:
                if cur_out == 'EUR':
                    for cur in data_list:
                        if cur_in == cur.currency_name:
                            res = round(float(int(amount) / cur.rate), 2)
                            answer = f"{amount} {cur.currency_name} = {res} EUR"
                            return json.dumps({'answer': answer}, indent=4)
                else:
                    for cur in data_list:
                        if cur_in == cur.currency_name:
                            cur_entry = [cur.currency_name, cur.rate]
                        if cur_out == cur.currency_name:
                            cur_out = [cur.currency_name, cur.rate]
                    
                    t_cur_entry = 1/cur_entry[1]
                    t_cur_out = 1/cur_out[1]
                    res = round(float(t_cur_entry * (1 / t_cur_out)) * int(amount), 2)
                    answer = f"{amount} {cur_entry[0]} = {res} {cur_out[0]}"
                    return json.dumps({'answer': answer}, indent=4)
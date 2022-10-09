import requests
from xml import etree
from xml.etree import ElementTree as ET
from .sources.saver import SourceSaver, CurrenciesSaver, ConvertSaver
from currencyconverter.models import Source, EuroRates
from eurorates import String
from django.http import HttpResponse, JsonResponse
import json
from django.utils.timezone import datetime
import re

class CurrencyConverterHandler:
    def handle_fetch(self):
        try:
            url ='https://www.ecb.europa.eu/stats/eurofxref/eurofxref-daily.xml'
            name = 'XML RCB Euro Rates'
            req = requests.get(url)
            req = "'''''" + str(req.content)[2:-1] + "'''''"
            with open('eurorates.py', 'w') as f:
                print("String = " + req , file=f)
                f.close()
            print("Fetch succeed")
            return "Fetch succeed"

        except requests.exceptions.ConnectionError as e:
            self.logger.error(e)
            error_response = {
                "imprint-fetch-error": "Connection error when fetching",
                "error-message": str(e)
            }
            SourceSaver.save(
                content=(error_response),
                url=url,
                status='500',
                name=name
            )
            return "Connection error when fetching"

    def handle_save_source(self):
        url ='https://www.ecb.europa.eu/stats/eurofxref/eurofxref-daily.xml'
        name = 'XML RCB Euro Rates'
        clean_source = String[2:]
        print("Source saved in DB")
        SourceSaver.save(clean_source, url, '200', name)

    def handle_parse(self):
        data_list = []
        xml_all = Source.objects.all()
        last_xml = xml_all[len(xml_all) -1]
        root = ET.fromstring(last_xml.content)
        data = root[2][0]
        for child in data:
            data_list.append([child.attrib['currency'], child.attrib['rate']])
            
        for cur in data_list:
            CurrenciesSaver.save(cur[0], cur[1])
        print("Currencies data extracted and saved in DB")
        return data_list

    def handle_convert(self):
        
        django_url = "http://127.0.0.1:8000"
        suffixe = "/money/convert/"
        data_list = EuroRates.objects.all()
        devises = []
        devises.append('EUR')
        for data in data_list:
            devises.append(data.currency_name)

        input_query = input("Entrez votre requête (ex: '15 EUR en USD'): ")
        regex_currencies = r'[A-Z]{3}'
        regex_amount = r'\d*\.?\d+'

        cur_in = None
        cur_out = None
        amount = None
        find_cur = re.findall(regex_currencies, input_query)
        if len(find_cur) == 2:
            cur_in = find_cur[0]
            cur_out = find_cur[1]
        
        find_amount = re.findall(regex_amount, input_query)
        if find_amount:
            amount = find_amount[0]
        
        if cur_in and cur_out and amount:
            r = requests.post(django_url + suffixe, data={'cur_in': cur_in,'cur_out': cur_out, 'amount': amount})
            print(cur_in, cur_out, amount)
            print(r.status_code, r.reason)
        else:
             r = requests.post(django_url + suffixe, data=({'answer': "I' sorry Dav, I'm afraid. I can't do that."}))


        # while True:
        #     input_cur_entry = input("Quelle monnaie voulez vous convertir ? ")
        #     if input_cur_entry in devises:
        #         try:
        #             input_amount = float(input("Quelle somme voulez vous convertir ? "))
        #         except:
        #             print("⚠️ Erreur ! Entrez un chiffre !!! ")
        #             continue
        #         input_cur_out = input("En quelle monnaie voulez vous convertir ? ")
        #         if input_cur_out in devises:
        #             if input_cur_entry == 'EUR':
        #                 for cur in data_list:
        #                     if input_cur_out == cur.currency_name:

        #                         res = round(float(int(input_amount) * cur.rate), 2)
        #                         answer = f"{input_amount} EUR = {res} {cur.currency_name}"

        #                         r = requests.post(django_url + suffixe, data={'cur_in': input_cur_entry, 'cur_out': input_cur_out, 'amount': input_amount, 'res': res, 'answer': answer, 'created_at': datetime.now().strftime("%Y-%d-%m %H:%M:%S.%f")[:-1]})
        #                         print(r.status_code, r.reason)
        #                         r = json.loads(r.content)
        #                         print('answer:', r['answer'])

        #                         response = requests.get(django_url + suffixe + f"?answer={answer}")
        #                         print("GET:", response.content)

        #                         # ConvertSaver.save(input_cur_entry, input_cur_out, input_amount, res)
        #                         # print(f"{input_amount} EUR en {cur.currency_name}")
        #                         # print(f"{input_amount} EUR = {res} {cur.currency_name}")
        #                         return ''
        #             else:
        #                 if input_cur_out == 'EUR':
        #                     for cur in data_list:
        #                         if input_cur_entry == cur.currency_name:
        #                             # response = requests.get(django_url + suffixe + f"?answer={answer}")
        #                             # print(response.text)

        #                             res = round(float(int(input_amount) / cur.rate), 2)
        #                             answer = f"{input_amount} {cur.currency_name} = {res} EUR"

        #                             r = requests.post(django_url + suffixe, data={'cur_in': input_cur_entry, 'cur_out': input_cur_out, 'amount': input_amount, 'res': res, 'answer': answer, 'created_at': datetime.now().strftime("%Y-%d-%m %H:%M:%S.%f")[:-1]})
        #                             print(r.status_code, r.reason)
        #                             r = json.loads(r.content)
        #                             print('answer:', r['answer'])

        #                             # ConvertSaver.save(input_cur_entry, input_cur_out, input_amount, res)
        #                             # print(f"{input_amount} {cur.currency_name} en EUR")
        #                             # print(f"{input_amount} {cur.currency_name} = {res} EUR")
        #                             return ''
        #                 else:
        #                     for cur in data_list:
        #                         if input_cur_entry == cur.currency_name:
        #                             # response = requests.get(django_url + suffixe + f"?answer={answer}")
        #                             # print(response.text)
        #                             cur_entry = [cur.currency_name, cur.rate]
        #                         if input_cur_out == cur.currency_name:
        #                             # response = requests.get(django_url + suffixe + f"?answer={answer}")
        #                             # print(response.text)
        #                             cur_out = [cur.currency_name, cur.rate]
                            
        #                     t_cur_entry = 1/cur_entry[1]
        #                     t_cur_out = 1/cur_out[1]
        #                     res = round(float(t_cur_entry * (1 / t_cur_out)) * int(input_amount), 2)
        #                     answer = f"{input_amount} {cur_entry[0]} = {res} {cur_out[0]}"

        #                     r = requests.post(django_url + suffixe, data={'cur_in': input_cur_entry, 'cur_out': input_cur_out, 'amount': input_amount, 'res': res, 'answer': answer, 'created_at': datetime.now().strftime("%Y-%d-%m %H:%M:%S.%f")[:-1]})
        #                     print(r.status_code, r.reason)
        #                     r = json.loads(r.content)
        #                     print('answer:', r['answer'])

        #                     # ConvertSaver.save(input_cur_entry, input_cur_out, input_amount, res)
        #                     # print(f"{input_amount} {cur_entry[0]} en {cur_out[0]}")
        #                     # print(f"{input_amount} {cur_entry[0]} = {res} {cur_out[0]}")
        #                     return ''
        #         else:
        #             print('Erreur! rentrez une code devise valide, en 3 lettres majuscules')
        #     else:
        #         print('Erreur! rentrez une code devise valide, en 3 lettres majuscules')
                    



CurrencyConverterInstance = CurrencyConverterHandler()

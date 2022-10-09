import requests
from xml.etree import ElementTree as ET
from .sources.saver import SourceSaver, CurrenciesSaver
from currencyconverter.models import Source, EuroRates
from eurorates import String
import re


class CurrencyConverterHandler:
    def handle_fetch(self):
        try:
            url = 'https://www.ecb.europa.eu/stats/eurofxref/eurofxref-daily.xml'

            req = requests.get(url)
            req = "'''''" + str(req.content)[2:-1] + "'''''"
            with open('eurorates.py', 'w') as f:
                print("String = " + req, file=f)
                f.close()
            print("Fetch succeed")
            return "Fetch succeed"

        except requests.exceptions.ConnectionError as e:
            error_response = {
                "source-fetch-error": "Connection error when fetching",
                "error-message": str(e)
            }
            print(error_response)
            return error_response

    def handle_save_source(self):
        url = 'https://www.ecb.europa.eu/stats/eurofxref/eurofxref-daily.xml'
        name = 'XML RCB Euro Rates'
        if String:
            clean_source = String[2:]
            print("Source saved in DB")
            SourceSaver.save(clean_source, url, '200', name)
        else:
            print("Save fail. No formated data source found.")
            return "Save fail"

    def handle_parse(self):
        data_list = []
        xml_all = Source.objects.all()
        if xml_all:
            last_xml = xml_all[len(xml_all) - 1]
            root = ET.fromstring(last_xml.content)
            data = root[2][0]
            for child in data:
                data_list.append([child.attrib['currency'], child.attrib['rate']])

            for cur in data_list:
                CurrenciesSaver.save(cur[0], cur[1])
            print("Currencies data extracted and saved in DB")
            return data_list
        else:
            print("Error. No Source object found.")
            return "Parse fail"

    def handle_convert(self):

        django_url = "http://127.0.0.1:8000"
        suffixe = "/money/convert/"
        data_list = EuroRates.objects.all()
        if data_list:
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
                r = requests.post(django_url + suffixe, data={'cur_in': cur_in, 'cur_out': cur_out, 'amount': amount})
                print(cur_in, cur_out, amount)
                print(r.status_code, r.reason)
            else:
                r = requests.post(django_url + suffixe, data=({'answer': "I' sorry Dav, I'm afraid. I can't do that."}))
                print("500 INTERNAL SERVER ERROR")
        else:
            print("Error. No data found")
            return "Convert fail"


CurrencyConverterInstance = CurrencyConverterHandler()

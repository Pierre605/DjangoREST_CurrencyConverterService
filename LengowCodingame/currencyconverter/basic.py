import re

# dico = {'1': 'hello', '2': 'world'}

# print(dico[1])


# from django.utils.timezone import datetime
# import json

# date = datetime.now()
# print(datetime.now())
# print(type(datetime.now()))
# print('\n')
# date = datetime.now().strftime("%Y-%d-%m %H:%M:%S.%f")[:-1]
# print(date)
# print(type(date))
# print('\n')

stg = "10.52 EUR en USD"
regex_currencies = r'[A-Z]{3}'
regex_amount = r'\d*\.?\d+'

res_cur = re.findall(regex_currencies, stg)
res_amount = re.findall(regex_amount, stg)

print(res_cur)
print("\n")
print(res_amount)

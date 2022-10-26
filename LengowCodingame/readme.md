## Currency Converter web service

(Training)

Instuctions:

Create a Goggle-like currency converter service using Euro currency rates at *https://www.ecb.europa.eu/stats/eurofxref/eurofxref-daily.xml* using Django and DjangoREST framework.
- Use a parser to extract data, no regex
- store data in database
- create query service API at **/money/convert** url consumed with a POST query like "100 EUR en USD" or "100 USD en JPY"

The answer would be like:

    POST HTTP 200 OK

    {

            "answer": "100 EUR = 100.31 USD"

    }

    POST HTTP 200 OK

    {

            "answer": "100 USD = 14717,45 JPY"

    }

And for a query like "52 EUR", the answer would be like:

    POST HTTP 500 Internal Server Error

    {

            "answer": "I' sorry Dav, I'm afraid. I can't do that."

    }



I chose SQLite for database mangement

Before you install django and dependencies packages in **requirements.txt**, 
run the virtual environment `\Scripts\activate.bat` (for Windows)

Once installed, do not forget to run ``python manage.py migrate``

To initiate the app: 

>Run the shell script **initiate.sh** with ``sh initiate.sh`` for Linux, 
or copy paste the command in the console for Windows os.

To query the API to convert an amount of money:

>Run the shell script **query_service.sh** with ``sh query_service.sh`` for Linux, 
or copy paste the command in the console for Windows os.

The result of your query is displayed server console side, as requested in the test instructions.

***README***
This project needs to be run from CA3.py and will incorporate functions found in CA3newsapi.py, CA3covidapi.py, CA3weatherapi.py and time_conversions modules.

These modules contain functions that get top news headlines from newsapi.org source, latest weather inforomation from the openweathermap.org source and latest coronavirus updates from public health england.
In case the get urls cannot be called then the data will come from latest_covid_info.txt, latest_news.txt and latest_weather.txt
In order for these functions to work if the api source should crash for whatever reason then these backups should still allow the functions to be called at any time

The Json file config has data which can be incorporated into each of the modules. 
This config file contains api keys which could be changed provided they are valid from the api sources

Pre-requisites: these can be installed with the 'pip install' command
sched, flask, pyttsx3, requests, uk_covid19

sys.log contains the log for the CA3.py function while it runs

CA3.py will add alarms and display notifications on a local server which can be accessed on a web browser. 
There are options to add a weather and/or news briefing to each alarm you set which will be read aloud when the page refreshes during the set time.

Code and all files available on https://github.com/Deroz01/CA3/tree/main/CA3

First set of code developed by Luca de Rozairo at 4th December 2020





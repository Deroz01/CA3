#https://api.coronavirus.data.gov.uk/v1/data
#https://coronavirus.data.gov.uk/details/developers-guide
#https://publichealthengland.github.io/coronavirus-dashboard-api-python-sdk/pages/examples/general_use.html

from uk_covid19 import Cov19API

import json
with open('config.json') as json_data_file:
    data = json.load(json_data_file)
    region = data ["region"]

def covid_update(region = region):
    """
    This function takes in a region as argument and returns a string giving information about the latst coronavirus data
    """
    SouthWest = [
        "areaType=region",
        "areaName="+region
    ]

    cases_and_deaths = {
        "newCasesByPublishDate": "newCasesByPublishDate"
    }

    api = Cov19API(
        filters=SouthWest,
        structure=cases_and_deaths,
    )
    if api:
        f = open("latest_covid_info.txt", "w")
        f.write(str(api))
        f.close()
    else:
        f = open("latest_covid_info.txt")
        api = f.read()
        
    data = api.get_json()['data']
    latestCasesByPublishDate = data [0]['newCasesByPublishDate']
    rate = 1+(latestCasesByPublishDate - data[1]['newCasesByPublishDate'])/data[0]['newCasesByPublishDate']
    rate = int(rate*100)/100
    rate = str(rate)+'. '
    
    newCases = 'Latest data for new cases by publish date is '+str(latestCasesByPublishDate)+' cases in your region. '
    
    return rate+newCases
    
assert type(covid_update()) == str
#https://openweathermap.org/api

import requests, time, json

with open('config.json') as json_data_file:
    data = json.load(json_data_file)
    weather_api_key = data["weather_api_key"]
    location = data["location"]
    
def get_weather():
    """
    This function returns a decription of the current weather forecast from the open weather map api source
    """
    current_weather = requests.get('http://api.openweathermap.org/data/2.5/weather?q='+location+'&appid='+weather_api_key+'&units=metric', timeout = 2.5)
    if current_weather:
        
        
        current_weather = current_weather.json()
        
        f = open("latest_weather.txt", "w")
        f.write(str(current_weather))
        f.close()
        
    else:
        f = open("latest_weather.txt")
        current_weather = f.read()
        
    #general weather decription
    weather = current_weather['weather'][0]
    weather_description = 'The current weather conditions is %s. ' %(weather ['description'])
    
    #temperature decription
    temperatures = current_weather['main']
    temperature_description = 'Current temperature is %s degrees celsius but given overall weather conditions it will feel like %s degrees celsius. Expect a minimum temperature of %s degrees celsius and a maximum of %s degrees celsius. ' % (temperatures['temp'], temperatures['feels_like'], temperatures['temp_min'], temperatures['temp_max'])
    
    #visibility description
    visibility = current_weather['visibility']
    if visibility < 1000:
        visibility_description = 'Visibility is very poor'
    if 1000<=visibility<4000:
            visibility_description = 'Visibility is poor'
    if 4000<= visibility<10000:
        visibility_description = 'Visibility is moderate'
    if 10000<= visibility<20000:        
        visibility_description = 'Visibility is good'
    if 20000<= visibility<40000:
        visibility_description = 'Visibility is very good'    
    if 40000<= visibility:
        visibility_description = 'Visibility is excellent'
    visibility_description +=' at %s metres. ' %(visibility)
    
    #wind description
    wind = current_weather['wind']
    wind_speed  = wind['speed']
    wind_direction = int(wind ['deg'])
    if (315<wind_direction<360 or 0<=wind_direction<=45): wind_direction = 'northerly' 
    elif 45<wind_direction<=135: wind_direction = 'easterly' 
    elif 135<wind_direction<=225: wind_direction = 'southerly'
    elif 225<wind_direction<=315: wind_direction = 'westerly' 
    wind_description = 'Wind speed is currently %s metres per second in a %s direction.' % (wind_speed, wind_direction)
    
    #combining all decriptions into one
    description = 'The following is your most recent weather forecast. '+weather_description+temperature_description+visibility_description+wind_description
    
    return(description)

assert type(get_weather())==str
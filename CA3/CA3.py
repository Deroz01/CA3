import sched, time, requests, pyttsx3, CA3newsapi, CA3covidapi, CA3weatherapi, logging, threading, json
from flask import Flask, render_template, request
from datetime import datetime
from CA3newsapi import get_headlines
from CA3covidapi import covid_update
from CA3weatherapi import get_weather
from time_conversions import *

logging.basicConfig(filename='sys.log', encoding='utf-8')
with open('config.json') as json_data_file:
    data = json.load(json_data_file)
    image = data["image"]
    location = data["location"]+' '
    interval = data["minute_interval"]
    template = data["template"]

app = Flask(__name__)

s = sched.scheduler(time.time, time.sleep)
engine = pyttsx3.init()

"""live title"""
def title():
    now = datetime.now()
    date_time = now.strftime("%H:%M %d/%m/%Y")
    return location + date_time
    
"""announcement function"""    
def tts_request(announcement:str):

    try:
        engine.endLoop()
    except:
        pass
    engine.say(announcement)
    engine.runAndWait()

"""update latest files every ... minutes"""    
def fetch(interval_minutes = interval):
    threading.Timer(60*interval_minutes, fetch).start()
    get_weather()
    get_headlines()
    covid_update()
fetch()
       
"""creating the two lists for alarms and notifications"""
alarms = []
notifications = []

"""adding news to notifications list by default"""
news = get_headlines()
for headline in news:
    notifications.append({'title':'Breaking News - ' + headline['title'], 'content':headline['content']})

alarms_today = []

@app.route('/index')
def main():
    app.logger.info('Processing default request')
    s.run(blocking=False)    
    """closing notification boxes"""
    notif = request.args.get('notif')
    for item in notifications:
        if item['title'] == notif:
            notification_number = len(notifications)
            notifications.remove(item)
            assert len (notifications)+1 == notification_number
    
    """closing alarm boxes"""
     
    alarm_item = request.args.get('alarm_item')
    for item in alarms:
        if item['title'] == alarm_item:  
            alarm_number = len(alarms)
            alarms.remove(item)
            s.cancel(e1)
            assert len(alarms)+1 == alarm_number
    
    """creating the alarms"""    
    alarm_title = request.args.get('two')

    news_included = request.args.get('news')
    
    weather_included = request.args.get('weather')
    
    alarm_date_time = request.args.get('alarm')
    
    if alarm_date_time:
        alarm_date_time = alarm_date_time.split('T')
        alarm_date = alarm_date_time[0]
        alarm_time = alarm_date_time[1]
        
        alarm_content = 'Alarm set for ' + alarm_date + ' at ' + alarm_time
        announcement_content = 'You scheduled an alarm now called ' +alarm_title+'. ' 
        announcement_content+='This is your alarm coronavirus update. Your local r number is ' + covid_update()
        news = get_headlines()
        if news_included:
            alarm_content+= ' - News briefing included'
            news_briefing =''
            news_briefing+= 'The following is your alarm news briefing. '
            for x in news:
                txt = x['title']
                x['title'] = txt[:txt.rindex(' -')]
                news_briefing+=x['title']+'. '
            announcement_content+=news_briefing
            
        if weather_included:
            alarm_content+= ' - Weather briefing included'
            announcement_content+=get_weather()
            
        alarms.append({'title': alarm_title, 'content': alarm_content, 'date': alarm_date, 'time':alarm_time, 'announcements':announcement_content})

        if alarm_date:    
            alarm_hhmm = alarm_time[-5:-3] + ':' + alarm_time[-2:]
            delay = hhmm_to_seconds(alarm_hhmm) - hhmm_to_seconds(current_time_hhmm())
            e1 = s.enter(int(delay), 1, tts_request, [alarms[0]['announcements'],]) 
           
    return render_template(template, title=title(), alarms=alarms, notifications=notifications,image=image)

    
 
if __name__ == '__main__':
    app.run()
    

    

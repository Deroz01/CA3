#https://newsapi.org/docs/endpoints/top-headlines

import requests, json

with open('config.json') as json_data_file:
    data = json.load(json_data_file)
    api_key = data["news_api_key"]
    country = data["country"]

def get_headlines():
    """
    This function returns a list of dictionaries for the top headlines in the gb area from the newsapi source.
    """
    #The valid format of the url to get top headlines from the uk
    url = ('http://newsapi.org/v2/top-headlines?'
           'country='+country+'&'
           'apiKey='+api_key)
           
    response = requests.get(url)
    response = response.json()
    status = response["status"]
    #Checking if the url is valid
    if status == 'ok':
        
        articles = response["articles"]
        
        f = open("latest_news.txt", "w")
        f.write(str(articles))
        f.close()
        
    else:
        f = open("latest_news.txt")
        articles = f.read()
        
    headlines = []
    for article in articles:
        title = article["title"]
        description = article["description"]
        link = article ["url"]
        if (description == "") or (description == None):
            headlines.append({"title":title, "content": "No description - See "+ link + " for more..."})
        else:    
            headlines.append({"title": title, "content":description})
    return headlines

assert type(get_headlines())== list
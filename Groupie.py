import json, requests, random, os, re, time
from flask import Flask, request
from pymongo import MongoClient

app = Flask(__name__)

GROUPME_TOKEN = os.getenv('GROUPME_TOKEN')
GROUPID = os.getenv('GROUPME_GROUP_ID')
GROUPME_BOT_ID = os.getenv('GROUPME_BOT_ID')
WEATHER_API_KEY = os.getenv('WEATHER_API_KEY')
WEATHER_ZIP_CODE = os.getenv('WEATHER_ZIP_CODE')
DB_USER = os.getenv('DB_USER')
DB_PASSWORD = os.getenv('DB_PASSWORD')
DB_NAME = os.getenv('DB_NAME')


@app.route('/', methods=['POST'])
def webhook():
  data = request.get_json()
  print(data)
  time.sleep(1)

  # /help command
  if (re.match('^\/help$|^\/help +',data['text']) != None):
      Bot().postText(('I\'m Boonie! A chat bot designed to do stuff and things! Try one of my multiple commands:\n\n'
                        '/weather will get the current forcast in your area.\n\n'
                        '/all allows for all chat members to be tagged in the message that preceeds the command.\n\n'
                        '/quote will get a random quote by someone of influence...or something.\n\n'
                        '/rezzie will get a random quote by one of my residents. Who knows what might popup.\n\n'
                        '/wiki will provide the chat with a link to a random wikipedia article.\n\n'))
      return

  # /quote command
  if (re.match('^\/weather$|^\/weather +',data['text']) != None):
      Bot().postText(API().getWeather())
      return

  # /all command
  if (re.match('^\/all [a-zA-Z0-9]+',data['text']) != None):
      Bot().postTextAll(re.sub('^\/all ', '',data['text']))
      return

  # /quote command
  if (re.match('^\/quote$|^\/quote +',data['text']) != None):
      # Bot().postText(API().getQuote(API().loadJson(quotes)))
      Bot().postText(Mongo().getInspirationalQuote())
      return

  # /rezzie command
  if (re.match('^\/rezzie$|^\/rezzie +',data['text']) != None):
      Bot().postText(Mongo().getResidentQuote())
      return

  # /wiki command
  if (re.match('^\/wiki$|^\/wiki +',data['text']) != None):
      Bot().postText(Wikipedia_API().getRandomArticle())
      return

  # /search command
  if (re.match('^\/search [a-zA-Z0-9]+',data['text']) != None):
      searchResults = Wikipedia_API().search(re.sub('^\/search ', '',data['text']))
      Bot().postText(searchResults)
      return

  # We don't want to reply to ourselves!
  # if data['name'] != 'Boonie':
  #   msg = '@{}, you sent "{}".'.format(data['name'], data['text'])
  #   Bot().postText(msg)

  return "ok", 200

class API(object):
    def fetchJson(self,url):
        r = requests.get(url)
        return r.json()

    # def loadJson(self, str):
    #     data = json.loads(json.dumps(str))
    #     return data

    # def getQuote(self,jsonStr):
    #     choice = random.choice(jsonStr['quotes'])
    #     quote = choice['quote']
    #     quoteAuthor = choice['author']
    #     return "%s -%s" % (quote,quoteAuthor)

    def getMembers(self,groupID):
        members = []
        r = requests.get('https://api.groupme.com/v3/groups/' + str(groupID) + "?token=" + GROUPME_TOKEN)
        data = json.loads(json.dumps(r.json()))
        data = data['response']['members']
        for person in data:
            members.append(person['name'])
        members.sort()

        return members

    def getWeather(self):
        self.temp = ''
        self.tempHigh = ''
        self.tempLow = ''
        self.weather = ''
        self.weatherDes = ''
        self.humidity = ''
        self.cloudCov = ''

        url = 'http://api.openweathermap.org/data/2.5/weather?zip={}&units=imperial&APPID={}'.format(
        WEATHER_ZIP_CODE,WEATHER_API_KEY)

        data = self.loadJson(self.fetchJson(url))

        # Add items to the weatherName and weatherDes arrays
        if (len(data['weather']) > 1):
            for w in data['weather']:
                self.weather += '\n\t\t| ' + w['main'] + ' |'
                self.weatherDes += '\n\t\t| ' + w['description'] + ' |'
        else:
            self.weather = ' | ' + data['weather'][0]['main'] + ' |'
            self.weatherDes = ' | ' + data['weather'][0]['main'] + ' |'

        self.temp = data['main']['temp']
        self.tempHigh = data['main']['temp_max']
        self.tempLow = data['main']['temp_min']
        self.humidity = data['main']['humidity']
        self.cloudCov = data['clouds']['all']

        report = 'Condition: {}\nDescription: {}\nTemps:\n\t\t\tCurrent: {}℉\n\t\t\tHigh: {}℉\n\t\t\tLow: {}℉\nHumidity: {}%\nCloud Coverage: {}%'.format(self.weather,self.weatherDes,self.temp,self.tempHigh,self.tempLow,self.humidity,self.cloudCov)

        return report

class Bot(object):
    def postText(self, text):
        postJson = {
          "bot_id"  : GROUPME_BOT_ID,
          "text"    : text
        }
        print(postJson)
        r = requests.post('https://api.groupme.com/v3/bots/post', data = postJson)

    def postTextAll(self, text):
        members = API().getMembers(GROUPID)
        msg = ''
        for person in members:
            msg += '@' + person + ' '
        msg += text
        postJson = {
          "bot_id"  : GROUPME_BOT_ID,
          "text"    : msg
        }
        print(postJson)
        r = requests.post('https://api.groupme.com/v3/bots/post', data = postJson)

class Wikipedia_API(object):
    def __init__(self):
        self.baseURL = 'https://en.wikipedia.org/w/api.php'
        self.baseArticleURL = 'https://en.wikipedia.org/wiki/'
    # ?action=query&prop=revisions&rvprop=content&format=json&formatversion=2&pageids=10000000
    def getRandomArticle(self):
        articleNum = str(random.randint(0,10000000))
        payload = {'action': 'query',
                    'prop': 'revisions',
                    'rvprop' : 'content',
                    'format' : 'json',
                    'formatversion' : '2',
                    'pageids' : articleNum
                    }

        r = requests.get(self.baseURL, params=payload)

        jsonStr = r.json()
        print (r.url)

        try:
            title = jsonStr['query']['pages'][0]['title']

            if ('User_talk:' in title): #Prevents User Talk articles from being used
                return self.getRandomArticle()
            link = self.baseArticleURL + title.replace(' ', '_')

            return ('Title: {}\nArticle Link: {}'.format(title, link))

        except (KeyError):
             self.getRandomArticle()

    def search(self, query):
        if (query == ''):
            return 'No search query was provided.'

        payload = {'action': 'query',
                    'list': 'search',
                    'srsearch' : query,
                    'format' : 'json',
                    }

        r = requests.get(self.baseURL, params=payload)

        jsonStr = r.json()
        searchResults = 'I found the following results for {} on Wikipedia:\n'.format(query)
        results = jsonStr['query']['search']
        if (len(results) == 0):
            return 'No search results found for {}'.format(query)


        for result in results:
            title = result['title']
            link = self.baseArticleURL + title.replace(' ', '_')
            searchResults += 'Title: {}\n Link: {}\n\n'.format(title,link)
        return searchResults

class Mongo:
    def __init__(self):
        self.client = MongoClient('mongodb://{}:{}@ds155653.mlab.com:55653/groupie_bot_quotes'.format(DB_USER, DB_PASSWORD),
                             connectTimeoutMS=30000,
                             socketTimeoutMS=None,
                             socketKeepAlive=True)
        self.db = self.client[DB_NAME]
        self.inspirationalCollection = self.db.inspirational
        self.residentCollection = self.db.residents

    def getResidentQuote(self):
        quotes = self.residentCollection.find()
        index = random.randint(0, quotes.count() - 1)
        quote = quotes[index]['quote']
        quoteAuthor = quotes[index]['author']
        return "%s -%s" % (quote,quoteAuthor)

    def getInspirationalQuote(self):
        quotes = self.inspirationalCollection.find()
        index = random.randint(0, quotes.count() - 1)
        quote = quotes[index]['quote']
        quoteAuthor = quotes[index]['author']
        return "%s -%s" % (quote,quoteAuthor)

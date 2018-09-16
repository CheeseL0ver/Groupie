import json
import requests
import random
import os
from flask import Flask, request

app = Flask(__name__)

bot_id = os.getenv('GROUPME_BOT_ID')
# bot_id = 'af71124cae5174ba8998c0a95b'

@app.route('/', methods=['POST'])
def webhook():
  data = request.get_json()
  print(data)
  # We don't want to reply to ourselves!
  if data['name'] != 'Boonie':
    msg = '@{}, you sent "{}".'.format(data['name'], data['text'])
    Bot().postQuote(msg)

  return "ok", 200

class API(object):
    def loadJson(self, file):
        data = json.loads(open(file).read())
        return data
        # for d in data['quotes']:
            # print(d['quote'] + " " + d['author'])
        # print(data['quotes'][0])
    def getQuote(self,jsonStr):
        # print(jsonStr['quotes'][0])
        choice = random.choice(jsonStr['quotes'])
        quote = choice['quote']
        quoteAuthor = choice['author']
        return "%s -%s" % (quote,quoteAuthor)
        # print (quote + " " + quoteAuthor)

class Bot(object):
    def postQuote(self, quote):
        postJson = {
          "bot_id"  : bot_id,
          "text"    : quote
        }
        print(postJson)
        r = requests.post('https://api.groupme.com/v3/bots/post', data = postJson)


# api = API()
# bot = Bot()
# api.loadJson('quotes.json')
# bot.postQuote(api.getQuote(api.loadJson('quotes.json')))

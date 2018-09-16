import json
import requests
import random
import os
import re
from flask import Flask, request

app = Flask(__name__)

bot_id = os.getenv('GROUPME_BOT_ID')

@app.route('/', methods=['POST'])
def webhook():
  data = request.get_json()

  if (re.match('^\/quote$',data['text']) != None):
      Bot().postText(API().getQuote(API.loadJson('quotes.json')))
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

    def getQuote(self,jsonStr):
        choice = random.choice(jsonStr['quotes'])
        quote = choice['quote']
        quoteAuthor = choice['author']
        return "%s -%s" % (quote,quoteAuthor)

class Bot(object):
    def postText(self, text):
        postJson = {
          "bot_id"  : bot_id,
          "text"    : text
        }
        # print(postJson)
        r = requests.post('https://api.groupme.com/v3/bots/post', data = postJson)


# api = API()
# bot = Bot()
# api.loadJson('quotes.json')
# bot.postQuote(api.getQuote(api.loadJson('quotes.json')))

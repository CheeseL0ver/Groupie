# Groupie

* A bot that can be used in a [GroupMe](https://www.groupme.com "GroupMe Homepage") chat
* Supports a variety on useful commands

## Getting Started
### Locally
To run the bot locally you will first need to have all the required Python modules installed and the supported version of Python installed.  The required module versions can be found in the **requirments.txt** file and the current supported Python can be found in the **runtime.txt** file.

Next you will have to set your terminal application to use the correct application. To do this the **FLASK_APP** environment variable must be set. This is most commonly done by running the following command: **$ export FLASK_APP=Groupie.py**
If you are on windows you may need to use **set** instead of **export**

Now, the application can be started by running the following command: **$ flask run**
You can also use Python's **-m** switch with Flask i.e. **python -m flask run**
If you are experiencing issues taking a look at the [Flask Quickstart Docs](http://flask.pocoo.org/docs/0.12/quickstart/ "Flask Quickstart") might help.

## TODO

* [x] create [GitHub](https://www.github.com "GitHub Homepage") repo
* [x] Have the bot join a chat
* [x] Create a test chat for bot testing
* [ ] Add bot commands
  * [x] /quote
    * Displays a random quote from a JSON string
  * [x] /Quote
    * Displays a random quote from a JSON string comprised of quotes from residents
  * [x] /all
    * Causes the following message to ping all members in the group
  * [x] /weather
    * Displays details about the weather in the specified area code
  * [x] /wiki
    * Displays a random [Wikipedia](https://en.wikipedia.org/ "Wikipedia Homepage") article title and a link to that article
  * [ ] More ideas?
* [x] DEPLOY!
  * [x] Create Procfile file
  * [x] Create runtime.txt file
  * [x] Create requirements.txt file
  * [x] setup Heroku for deployment
  * [x] Setup Heroku config vars for needed fields
  * [x] Deploy to [Heroku](https://www.heroku.com "Heroku Homepage")

## Stretch Features
* [ ] Set timeouts to prevent command spamming
* [ ] Create white-list functionality for specific commands
* [ ] Move all JSON data to web host instead of being hard coded
* [ ] Add game functionality i.e. Group Trivia 

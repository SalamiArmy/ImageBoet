# ImageBoet
## A simple python bot for Telegram for idiots who laugh at memes.

### What is ImageBoet?
ImageBoet is a chat bot for telegram that is funny to watch fail!

### How does it work?
ImageBoet will listen for all messages in a given chat (either directly with him or in a chat room which you invite him to) starting with "/get".
tl;dr: Look at one of the existing commands, you must have a run(bot, chat_id, user, request_text, keyConfig, number_of_results) function.

### How do I make my own bot using this?
Go to https://console.developers.google.com and create a Google App Engine project. Then take that project id (it will be two random words and a number eg. gorilla-something-374635) and your Telegram Bot ID which the Bot Father gave you and do the following:

1. Copy app.yaml.template and rename the copy to to app.yaml.
2. Update {GOOGLE APP ENGINE PROJECT ID} in app.yaml.
3. Copy keys.ini.template and rename the copy to keys.ini.
4. Update {Your Telegram Bot ID here} in keys.ini 
OPTIONAL:
5. Update the rest of keys.ini with keys for each command you want to use.
6. Copy pre-push to the .git\hooks folder.
7. In .git\hooks\pre-push change were it says [[PythonInstallation]] to your Python install location in bash notation (e.g. /C/Python27) and your 
8. In .git\hooks\pre-push change were it says [[GoogleCloudSDKInstallation]] to your Google Cloud SDK install locaiton in bash notation (e.g. /C/Program Files (x86))
9. Now when you push it will automagicly build and deploy ImageBoet to the cloud! To the hindenpeter!

In lib\SoundCloud\Client.py set enable_ssl = False (Unsupported by Google App Engine)
oh ja, /launch command needs a module called "dateutil" clone from https://github.com/dateutil/dateutil and copy the folder "dateutil" into lib.

Finally go to https://{GOOGLE APP ENGINE PROJECT ID}.appspot.com/set_webhook?url=https://{GOOGLE APP ENGINE PROJECT ID}.appspot.com/webhook (replace both {GOOGLE APP ENGINE PROJECT ID}s with the Google App Engine Project ID) to tell Telegram where to send web hooks. This is all that is required to setup web hooks, you do not need to tell the Bot Father anything about web hooks.

### Why the name ImageBoet?
Boet is Afrikaans for brother. This bot is funny, light hearted, talking to him is like joking around with your "boet".
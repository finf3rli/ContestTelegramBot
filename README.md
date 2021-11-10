# ContestTelegramBot
Telegram bot that register users to a DB, hence they will be sorted out for a prize

# Requirements

This telegram bot requires some python library(see `requirements.txt`) and somewhere to be hosted, in this case i used Heroku.
This is very important because using Heroku i achieved the possibility to run the bot via webhooks instead of polling(that is also another possibility, not today).

# `bot.py`

It contains mostly code that manages the overall bot functionalities, such as:
- webhook token binding
- /commands such welcome message, un/subscribe, etc.
- handlers to call functions defined in `func.py`

# `func.py`

Pure code that make the bot work. It is able to:
- check user subscription to a telegram channel
- connect to a database mysql
- print a list of people subscribed
- print a position in list
- add user to database
- remove user to database
- truncate table
- query user on database

import os
import logging

import emoji
import telegram

import func

from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import Updater, CommandHandler, CallbackQueryHandler, MessageHandler, Filters

PORT = int(os.environ.get('PORT', 5000))

# Enable logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)

logger = logging.getLogger(__name__)
TOKEN = "" #token bot telegram
bot = telegram.Bot(TOKEN)
# Define a few command handlers. These usually take the two arguments update and
# context. Error handlers also receive the raised TelegramError object in error.
def start(update, context):
    """Send a message when the command /start is issued."""
    #update.message.reply_text('Hi!')a
    keyboard = [
        [
            InlineKeyboardButton("Iscrivimi " + emoji.emojize(":pencil:", use_aliases = True), callback_data = '/iscrivimi'),
            InlineKeyboardButton("Disiscrivimi " + emoji.emojize(":x:", use_aliases = True), callback_data='/disiscrivimi'),
        ],
        [InlineKeyboardButton("Posizione " + emoji.emojize(":chart_with_upwards_trend:", use_aliases = True), callback_data='/posizione')],
    ]

    reply_markup = InlineKeyboardMarkup(keyboard)

    update.message.reply_text('Ehi! Ora puoi iscriverti alla lotteria \U0001F60E', reply_markup=reply_markup)

def iscrivimi(update, context):
    user = update.message.chat
    if func.addUser(user['id'], bot):
        bot.sendMessage(user['id'], emoji.emojize(":white_check_mark:", use_aliases=True) + " Sei iscritto al contest")
    else:
        bot.sendMessage(user['id'], emoji.emojize(":ghost:", use_aliases=True) + " Utente assente. Iscriviti a @ e poi /iscrivimi")

def disiscrivimi(update, context):
    user = update.message.chat
    if func.removeUser(user['id']):
        bot.sendMessage(user['id'], "Ti sei rimosso dalla lotteria")
    else:
        bot.sendMessage(user['id'], "Già non facevi parte della lotteria")

def posizione(update, context):
    user = update.message.chat
    bot.sendMessage(user['id'], func.printRank(user['id'], bot))

def button(update, context) -> None:
    query = update.callback_query
    # user = update.callback_query.message.chat
    # user["username"] e user["id" forniscono i rispettivi valori(id to str)
    user = update.callback_query.message.chat
    # CallbackQueries need to be answered, even if no notification to the user is needed
    # Some clients may have trouble otherwise. See https://core.telegram.org/bots/api#callbackquery
    query.answer()

    if query.data == '/iscrivimi':
        #query.edit_message_text('id: ' + str(user['id']))
        #bot.sendMessage(user['id'], str(user['id'])) #arriva l'id
        if func.addUser(user['id'], bot):
            query.edit_message_text(emoji.emojize(":white_check_mark:", use_aliases=True) + " Sei iscritto al contest")
        else:
            query.edit_message_text(emoji.emojize(":ghost:", use_aliases=True) + " Utente assente. Iscriviti a @ e poi /iscrivimi")
    elif query.data == '/disiscrivimi':
        if func.removeUser(user['id']):
            query.edit_message_text("Ti sei rimosso dalla lotteria")
        else:
            query.edit_message_text("Già non facevi parte della lotteria")
    elif query.data == '/posizione':
        query.edit_message_text(func.printRank(user['id'], bot))
    elif query.data == 'y':
        func.emptyTable()
        query.edit_message_text("Lista svuotata!")
    elif query.data == 'n':
        query.edit_message_text("Azione annullata")

def help(update, context):
    """Send a message when the command /help is issued."""
    update.message.reply_text('Help!')

def lista(update, context):
    user = update.message.chat
    member = bot.getChatMember("@id channel", user['id'])  # chat_id represents users' unique id
    if member["status"] in ["administrator", "creator"]:
        list = func.printList(user['id'], bot)
        if list == "":
            bot.sendMessage(user['id'], "La lista è vuota")
        else:
            bot.sendMessage(user['id'], func.printList(user['id'], bot))
    else:
        start(update, context)

def svuota(update, context):
    user = update.message.chat
    member = bot.getChatMember("@id channel", user['id'])  # chat_id represents users' unique id
    if member["status"] in ["administrator", "creator"]:
        keyboardYN = [
            [
                InlineKeyboardButton("Si", callback_data='y'),
                InlineKeyboardButton("No", callback_data='n'),
            ]
        ]

        reply_markup = InlineKeyboardMarkup(keyboardYN)
        update.message.reply_text('Vuoi veramente svuotare la lista?', reply_markup=reply_markup)
    else:
        start(update, context)

def printl(update, context):
    #update.message.reply_text(func.p())
    #user = update.message.from_user
    #bot.sendMessage(update.message.chat.id, "ciao")

    user = update.message.chat
    try:
        member = bot.getChatMember('@id channel', user['id'])
        if member["status"] in ["administrator", "creator", "member"]:
            update.message.reply_text('ci sei')
        else:
            update.message.reply_text('non ci sei')
    except:
        update.message.reply_text("Errore inaspettato. [user not found in channel]")

def echo(update, context):
    """Echo the user message."""
    start(update, context)

def error(update, context):
    """Log Errors caused by Updates."""
    logger.warning('Update "%s" caused error "%s"', update, context.error)

def main():
    """Start the bot."""
    # Create the Updater and pass it your bot's token.
    # Make sure to set use_context=True to use the new context based callbacks
    # Post version 12 this will no longer be necessary
    updater = Updater(TOKEN, use_context=True)
    # Get the dispatcher to register handlers
    dp = updater.dispatcher

    '''
    How to change /start message:
    1. Create variable to store wether the command has been called or not
    2. Create /edit command
    3. Create variable to store the message
    4. Also, check if is admin
    5. Inside echo(), check: if n == True ? message = "text" : start()
    '''

    # on different commands - answer in Telegram
    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(CommandHandler("iscrivimi", iscrivimi))
    dp.add_handler(CommandHandler("disiscrivimi", disiscrivimi))
    dp.add_handler(CommandHandler("posizione", posizione))
    dp.add_handler(CommandHandler("lista", lista))
    dp.add_handler(CommandHandler("svuota", svuota))
    dp.add_handler(CallbackQueryHandler(button))
    # on noncommand i.e message - echo the message on Telegram
    dp.add_handler(MessageHandler(Filters.text, echo))

    # log all errors
    dp.add_error_handler(error)

    # Start the Bot
    updater.start_webhook(listen="0.0.0.0",
                          port=int(PORT),
                          url_path=TOKEN)
    updater.bot.setWebhook('webhook url' + TOKEN)

    updater.idle()

if __name__ == '__main__':
    main()

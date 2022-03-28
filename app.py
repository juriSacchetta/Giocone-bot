from urllib import response
from telegram.ext.updater import Updater
from telegram.update import Update
from telegram.ext.callbackcontext import CallbackContext
from telegram.ext.commandhandler import CommandHandler
from telegram.ext.messagehandler import MessageHandler
from telegram.ext.filters import Filters

import re 
import json 
import logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                     level=logging.INFO)

updater = Updater("", use_context=True)

banned_words = []
players = []

COMMAND_ADD_BANNED_WORD = "/addword"
COMMAND_ADD_PLAYERS = "/addplayers"
COMMAND_GET_BANNED_WORDS = "/getwords"

def start(update: Update, context: CallbackContext):
	update.message.reply_text(
		"""Ok iniziamo una nuova partita!
        Inizia a registrare le nuove parole""")

def add_banned_word(update: Update, context: CallbackContext):
    word = update.message.text.removeprefix(COMMAND_ADD_BANNED_WORD).replace(' ', '').lower()
    if len(word) == 0:
        update.message.reply_text("La sintassi è" + COMMAND_ADD_BANNED_WORD +  "'parola da bannare'")
        return
    if banned_words.__contains__(word):
        update.message.reply_text("La parola è già bannata")
    else:
        banned_words.append(word)
        update.message.reply_text( '"' + word + '" è stata aggiunta')

def get_banned_word(update: Update, context: CallbackContext):
    if len(banned_words) == 0:
        update.message.reply_text("Non ci sono ancora parole registrate")
    else:
        resp = ""
        for word in banned_words:
            resp = resp + word + "\n"
        update.message.reply_text(resp)

def add_players(update: Update, context: CallbackContext):
    names = update.message.text.removeprefix(COMMAND_ADD_PLAYERS).replace(' ', '').split(',')
    print(names)
    if names.count == 0 or len(names[0]) == 0:
        update.message.reply_text("La sintassi è " + COMMAND_ADD_PLAYERS + " player1, player2,...")
        return
    duplicate = []
    added = []
    for name in names:
        name = name.capitalize()
        if players.__contains__(name):
            duplicate.append(name)
        else:
            players.append(name)
            added.append(name)
    if len(added) > 0:
        res = "I seguenti giocatori sono stati aggiunti:"
        for x in added:
            res = res + '\n' + x
        update.message.reply_text(res)
    if len(duplicate) > 0:
        res = "I seguenti giocatori non sono stati aggiunti perché duplicati:"
        for x in duplicate:
            res = res + '\n' + x
        update.message.reply_text(res)

def help(update: Update, context: CallbackContext):
	update.message.reply_text("""Available Commands :-
	/start - To start a new instance
    """ + COMMAND_ADD_BANNED_WORD + """ - To add a banned word
    """ + COMMAND_GET_BANNED_WORDS + """ - To get all banned words
    """ + COMMAND_ADD_PLAYERS + """ - To add a new player""")

def unknown(update: Update, context: CallbackContext):
	update.message.reply_text(
		"Sorry '%s' is not a valid command" % update.message.text)

updater.dispatcher.add_handler(CommandHandler('start', start))
updater.dispatcher.add_handler(CommandHandler('help', help))
updater.dispatcher.add_handler(CommandHandler(COMMAND_ADD_BANNED_WORD.replace('/', ''), add_banned_word))
updater.dispatcher.add_handler(CommandHandler(COMMAND_ADD_PLAYERS.replace('/', '')  , add_players))
updater.dispatcher.add_handler(CommandHandler(COMMAND_GET_BANNED_WORDS.replace('/', '')  , get_banned_word))
updater.dispatcher.add_handler(MessageHandler(Filters.command, unknown)) # Filters out unknown commands

updater.start_polling()

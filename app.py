from telegram.ext.updater import Updater
from telegram.update import Update
from telegram.ext.callbackcontext import CallbackContext
from telegram.ext.commandhandler import CommandHandler
from telegram.ext.messagehandler import MessageHandler
from telegram.ext.conversationhandler import ConversationHandler
from telegram.ext.filters import Filters
import logging
from Match import Match

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)

api_file = open("API_TOKEN.txt", "r")
token = api_file.readline()
print(token)
updater = Updater(token, use_context=True)

global match
match = None
COMMAND_NEW_MATCH = "/newmatch"
COMMAND_CLEAR_MATCH = "/ClearMatch"
COMMAND_ADD_BANNED_WORD = "/addword"
COMMAND_ADD_PLAYERS = "/addplayers"
COMMAND_GET_BANNED_WORDS = "/getwords"

def active_match(update: Update, context: CallbackContext):
    if match is None:
        update.message.reply_text("There is no active match, you have to start one firts")
        return False
    else:
        return True

def start(update: Update, context: CallbackContext):
    logging.info("A new match is starting...")
    context.bot.send_message(chat_id=update.effective_chat.id, text="I'm a bot, please talk to me!")

def new_match(update: Update, context: CallbackContext):
    if match is not None:
        update.message.reply_text("There is another match active.\nFirst you have to close the other one")
    match = Match()
    update.message.reply_text("""Ok a new match is started""")

def clear_match(update: Update, context: CallbackContext):
    del match
    match = Match()

def add_banned_word(update: Update, context: CallbackContext):
    if  active_match() == False: 
        return
    word = update.message.text.removeprefix(COMMAND_ADD_BANNED_WORD).replace(' ', '').lower()
    if len(word) == 0:
            update.message.reply_text("La sintassi è" + COMMAND_ADD_BANNED_WORD +  "'parola da bannare'")
            logging.debug("Received empty word")
            return
    update.message.reply_text(match.add_banned_word(word))

def get_banned_word(update: Update, context: CallbackContext):
    if  active_match() == False: 
        return
    update.message.reply_text(match.get_banned_word())
    logging.info("Sending banned words report")

def add_players(update: Update, context: CallbackContext):
    if  active_match() == False: 
        return
    names = update.message.text.removeprefix(COMMAND_ADD_PLAYERS).replace(' ', '').split(',')
    if names.count == 0 or len(names[0]) == 0:
        update.message.reply_text("La sintassi è " + COMMAND_ADD_PLAYERS + " player1, player2,...")
        logging.debug("Received a empty string")
        return
    # result = match.add_players(names)
    result = {"added": ['juri']}
    if len(result.get('added')) > 0:
        res = "I seguenti giocatori sono stati aggiunti:"
        for x in result.get("added"):
            res = res + '\n' + x
        update.message.reply_text(res)
        logging.info("Added: " + result.get("added").__str__())
    if len(result.get("duplicate")) > 0:
        res = "I seguenti giocatori non sono stati aggiunti perché duplicati:"
        for x in result.get("duplicate"):
            res = res + '\n' + x
        update.message.reply_text(res)
        logging.debug("Find duplicated player: " + result.get("duplicate").__str__())

def help(update: Update, context: CallbackContext):
    logging.debug("Sent a help message")
    update.message.reply_text(
"""Available Commands :-
""" + COMMAND_NEW_MATCH + """ - To start a new match 
""" + COMMAND_CLEAR_MATCH + """ - To clear the current match
""" + COMMAND_ADD_BANNED_WORD + """ - To add a banned word
""" + COMMAND_GET_BANNED_WORDS + """ - To get all banned words
""" + COMMAND_ADD_PLAYERS + """ - To add a new player""")

def unknown(update: Update, context: CallbackContext):
    logging.warn("Found a unknow command: " + update.message.text)
    update.message.reply_text(
		"Sorry '%s' is not a valid command" % update.message.text)

updater.dispatcher.add_handler(CommandHandler('start', start))
updater.dispatcher.add_handler(CommandHandler('help', help))
updater.dispatcher.add_handler(CommandHandler(COMMAND_NEW_MATCH.replace('/', ''), new_match))
updater.dispatcher.add_handler(CommandHandler(COMMAND_CLEAR_MATCH.replace('/', ''), clear_match))
updater.dispatcher.add_handler(CommandHandler(COMMAND_ADD_BANNED_WORD.replace('/', ''), add_banned_word))
updater.dispatcher.add_handler(CommandHandler(COMMAND_ADD_PLAYERS.replace('/', '')  , add_players))
updater.dispatcher.add_handler(CommandHandler(COMMAND_GET_BANNED_WORDS.replace('/', '')  , get_banned_word))
updater.dispatcher.add_handler(MessageHandler(Filters.command, unknown)) # Filters out unknown commands

updater.start_polling()
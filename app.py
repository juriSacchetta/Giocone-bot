from telegram.ext.updater import Updater
from telegram.update import Update
from telegram.ext.callbackcontext import CallbackContext
from telegram.ext.commandhandler import CommandHandler
from telegram.ext.messagehandler import MessageHandler
from telegram.ext.conversationhandler import ConversationHandler
from telegram.ext.filters import Filters
import logging
from Match import Match
from exceptions import *

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)

api_file = open("API_TOKEN.txt", "r")
token = api_file.readline()
updater = Updater(token, use_context=True)

COMMAND_INIT_MATCH = "/init"
COMMAND_ADD_PLAYERS = "/addplayers"
COMMAND_ADD_BANNED_WORD = "/addword"
COMMAND_START_MATCH = "/start"

COMMAND_RECORD_FAULT = "/fault"
COMMAND_END = "/end"

COMMAND_GET_BANNED_WORDS = "/words"
COMMAND_STATISTICS = "/stat"

def active_match(update: Update, context: CallbackContext) -> bool:
    if context.chat_data["match"] is None:
        update.message.reply_text("There is no active match, you have to start one first")
        return False
    else:
        return True

def start(update: Update, context: CallbackContext):
    if not active_match(update, context): 
        return
    context.bot.send_message(chat_id=update.effective_chat.id, text = "WELCOME TO THE JUNGLE")
    context.chat_data["match"].start()

def init_match(update: Update, context: CallbackContext):
    if "match" in context.chat_data.keys() and context.chat_data["match"] is not None:
        update.message.reply_text("Sorry, there is another match active.\nFirst you have to close the other one")
    context.chat_data["match"] = Match()
    context.bot.send_message(chat_id=update.effective_chat.id, text = "Ok a new match is init phase")

def end(update: Update, context: CallbackContext):
    context.chat_data["match"] = None

def add_banned_word(update: Update, context: CallbackContext):
    if  active_match(update, context) == False: 
        return
    word = update.message.text.removeprefix(COMMAND_ADD_BANNED_WORD).replace(' ', '').lower()
    if len(word) == 0:
            update.message.reply_text("La sintassi è" + COMMAND_ADD_BANNED_WORD +  "'parola da bannare'")
            logging.debug("Received empty word")
            return
    context.bot.send_message(chat_id=update.effective_chat.id, text=context.chat_data["match"].add_banned_word(word))

def get_banned_word(update: Update, context: CallbackContext):
    if not active_match(update, context): 
        return
    update.message.reply_text(context.get_banned_word())
    logging.info("Sending banned words report")

def add_players(update: Update, context: CallbackContext):
    if  active_match(update, context) == False: 
        return
    names = update.message.text.removeprefix(COMMAND_ADD_PLAYERS).replace(' ', '').split(',')
    if names.count == 0 or len(names[0]) == 0:
        update.message.reply_text("La sintassi è " + COMMAND_ADD_PLAYERS + " player1, player2,...")
        logging.debug("Received a empty string")
        return
    result = context.chat_data["match"].add_players(names)
    if len(result.get('added')) > 0:
        res = "I seguenti giocatori sono stati aggiunti:"
        for x in result.get("added"):
            res = res + '\n' + x
        context.bot.send_message(chat_id=update.effective_chat.id, text=res)
        logging.info("Added: " + result.get("added").__str__())
    if len(result.get("duplicate")) > 0:
        res = "I seguenti giocatori non sono stati aggiunti perché duplicati:"
        for x in result.get("duplicate"):
            res = res + '\n' + x
        update.message.reply_text(res)
        logging.debug("Find duplicated player: " + result.get("duplicate").__str__())

def report_fault(update: Update, context: CallbackContext):
    s = update.message.text.removeprefix(COMMAND_RECORD_FAULT)
    s = s.split(' ')
    s.remove('')
    try:
        context.chat_data["match"].report_fault(s[0], s[1])
    except NotStartedMatch as e:
        update.message.reply_text(e.message)

def help(update: Update, context: CallbackContext):
    logging.debug("Sent a help message")
    update.message.reply_text(
"""Available Commands :-
""" + COMMAND_INIT_MATCH + """ - To init a new match
""" + COMMAND_ADD_PLAYERS + """ - To add a new player
""" + COMMAND_ADD_BANNED_WORD + """ - To add a banned word
""" + COMMAND_START_MATCH + """ - To start the match
""" + COMMAND_RECORD_FAULT + """ - To record a fault, "player" "word"
""" + COMMAND_END + """ - To end the current match
""" + COMMAND_GET_BANNED_WORDS + """ - To get all banned words""")

def unknown(update: Update, context: CallbackContext):
    logging.warn("Found a unknow command: " + update.message.text)
    update.message.reply_text(
		"Sorry '%s' is not a valid command" % update.message.text)

def get_statistics(update: Update, context: CallbackContext):
    context.bot.send_message(chat_id=update.effective_chat.id, text=context.chat_data["match"].get_statistic())

updater.dispatcher.add_handler(CommandHandler('start', start))
updater.dispatcher.add_handler(CommandHandler('help', help))
updater.dispatcher.add_handler(CommandHandler(COMMAND_INIT_MATCH.replace('/', ''), init_match))
updater.dispatcher.add_handler(CommandHandler(COMMAND_ADD_BANNED_WORD.replace('/', ''), add_banned_word))
updater.dispatcher.add_handler(CommandHandler(COMMAND_ADD_PLAYERS.replace('/', '')  , add_players))
updater.dispatcher.add_handler(CommandHandler(COMMAND_START_MATCH.replace('/', ''), start))

updater.dispatcher.add_handler(CommandHandler(COMMAND_RECORD_FAULT.replace('/', ''), report_fault))
updater.dispatcher.add_handler(CommandHandler(COMMAND_STATISTICS.replace('/', ''), get_statistics))

updater.dispatcher.add_handler(CommandHandler(COMMAND_END.replace('/', ''), end))
updater.dispatcher.add_handler(CommandHandler(COMMAND_GET_BANNED_WORDS.replace('/', '')  , get_banned_word))
updater.dispatcher.add_handler(MessageHandler(Filters.command, unknown)) # Filters out unknown commands

updater.start_polling()
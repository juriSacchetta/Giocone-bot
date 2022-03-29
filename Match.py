import logging
import numpy as np
from exceptions import *


class Match():

    def __init__(self) -> None:
        self.started = False
        self.banned_words = []
        self.players = []
    
# ------------ INIT PHASE ------------------------
    def add_banned_word(self, word: list) -> str:
        if self.started == True: 
            return
        word = word.capitalize()
        if self.banned_words.__contains__(word):
            logging.debug("Received duplicate word")
            return "La parola è già bannata"
        else:
            self.banned_words.append(word)
            logging.info("Added banned word: " + word)
            return '"' + word + '" è stata aggiunta'

    def add_players(self, names: list[str]) -> dict:
        if self.started == True: 
            return
        duplicate = []
        added = []
        for name in names:
            name = name.capitalize()
            if self.players.__contains__(name):
                duplicate.append(name)
            else:
                self.players.append(name)
                added.append(name)
        return {"added": added, "duplicate": duplicate}

    def start(self):
        if self.started == True: 
            return
        assert(len(self.players) == len(self.banned_words))
        self.started = True
        self.fault_matrix = np.zeros((len(self.players), len(self.banned_words), 1), dtype=np.int16)
        logging.info("A new match is started")


# ------------ IN WHILE -----------------------------
    
    def report_fault(self, player: str, word: str):
        if not self.started:
            raise NotStartedMatch
        player = player.capitalize()
        word = word.capitalize()
        id_player = self.players.index(player)
        id_word = self.banned_words.index(word)
        self.fault_matrix[id_player, id_word] = self.fault_matrix[id_player, id_word] + 1
    
# ----------- UTILS ---------------------------------------

    def get_banned_word(self) -> str:
        if self.started == True: 
            return
        if len(self.banned_words) == 0:
            return "For now there aren't banned word"
        else:
            resp = ""
            for word in self.banned_words:
                resp = resp + word + "\n"
            return resp
    
    def get_statistic(self):
        if not self.started:
            raise NotStartedMatch
        if self.started == False:
            return
        s = ''
        for i in range(0, len(self.players)) :
            s = s + self.players[i] + ': ' + str(np.sum(self.fault_matrix[i])) + '\n'
        return s
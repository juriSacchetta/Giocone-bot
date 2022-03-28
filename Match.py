import logging

class Match():
    
    def __init__(self) -> None:
        self.active = False
        self.banned_words = []
        self.players = []

    def add_banned_word(self, word: str) -> str:
        if self.banned_words.__contains__(word):
            logging.debug("Received duplicate word")
            return "La parola è già bannata"
        else:
            self.banned_words.append(word)
            logging.info("Added banned word: " + word)
            return '"' + word + '" è stata aggiunta'

    def get_banned_word(self) -> str:
        if len(self.banned_words) == 0:
            return "For now there aren't banned word"
        else:
            resp = ""
            for word in self.banned_words:
                resp = resp + word + "\n"
            return resp

    def add_players(self, names: list[str]) -> dict:
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
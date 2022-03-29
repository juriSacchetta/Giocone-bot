class NotStartedMatch(Exception):
    
    def __init__(self):
        self.message = "The match is still in init phase,\nplease start it first"
        super().__init__(self.message)
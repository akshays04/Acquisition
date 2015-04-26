
class DataBean():
    
    def __init__(self):
        self.team1 = ""
        self.team2 = ""
        self.winner = ""
        self.margin = ""
        self.location = ""
        self.date = ""
        self.id = ""
        self.scorecard = ""
        
    def __str__(self):
        print self.team1 + " vs " + self.team2 + " was won by " + self.winner + " by " + self.margin + " at " + self.location + " on " + self.date + " for more information go to " + self.scorecard 
class Sentiment:
    def __init__(self, sentiment: dict):
        self.anger = sentiment["anger"]
        self.anticipation = sentiment["anticipation"]
        self.disgust = sentiment["disgust"]
        self.fear = sentiment["fear"]
        self.joy = sentiment["joy"]
        self.sadness = sentiment["sadness"]
        self.surprise = sentiment["surprise"]
        self.trust = sentiment["trust"]

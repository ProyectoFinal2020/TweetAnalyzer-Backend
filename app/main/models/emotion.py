class Emotion:
    def __init__(self, emotion: dict):
        self.anger = emotion["anger"]
        self.anticipation = emotion["anticipation"]
        self.disgust = emotion["disgust"]
        self.fear = emotion["fear"]
        self.joy = emotion["joy"]
        self.sadness = emotion["sadness"]
        self.surprise = emotion["surprise"]
        self.trust = emotion["trust"]

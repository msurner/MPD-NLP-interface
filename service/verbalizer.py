# verbalizer randomizes output
import random

okResponse = ["Ok. Here we go.", "Ok. Have fun!", "Ok. Let's go."]
dontPlayResponse = ["What else do you want to hear?"]
dontStopPauseResponse = ["Sure. Let's make some noise."]
dontResumeResponse = ["Sure. I'm ready."]

def getOkText():
    return okResponse[random.randint(0, len(okResponse)-1)]

def getDontPlayText():
    return dontPlayResponse[random.randint(0, len(dontPlayResponse)-1)]

def getDontStopPauseText():
    return dontStopPauseResponse[random.randint(0, len(dontPlayResponse)-1)]

def getDontResumeText():
    return dontResumeResponse[random.randint(0, len(dontPlayResponse)-1)]

def getAlternatePlaySuggestion(argument):
    return "Hmm.. I didn't get that. Should i play " + argument + "?"

def getConnectionError():
    return "Unfortunately i can't connect to the MPD Server."

def getQuestionForArtistSongGerneOrRandom():
    return "Tell me an artist, song or gerne. Or do you want me to play a random song?"

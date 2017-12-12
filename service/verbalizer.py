# verbalizer randomizes output
import random

okResponse = ["Ok. Here we go.", "Ok. Have fun!", "Ok. Let's go."]
dontPlayResponse = ["What else do you want to hear?"]
dontStopPauseResponse = ["Sure. Let's make some noise."]
dontResume = ["Sure. I'm ready."]

def getOkText():
    return okResponse[random.randint(0, len(okResponse)-1)]

def getDontPlayText():
    return dontPlayResponse[random.randint(0, len(dontPlayResponse)-1)]

def getDontStopPauseText():
    return dontStopPauseResponse[random.randint(0, len(dontPlayResponse)-1)]

def getDontResumeText():
    return dontResumeResponse[random.randint(0, len(dontPlayResponse)-1)]


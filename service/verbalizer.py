# verbalizer randomizes output
import random

okResponse = ["Ok. Here we go.", "Ok. Have fun!", "Ok. Let's go."]

def getOkText():
    return okResponse[random.randint(0, len(okResponse)-1)]

"""
Autor: Martin Surner
License: MIT

This script tries to parse instructions like following:

Play.
Stop.
Pause.
Play David Bowie.
Play Heroes from David Bowie.
Play not David Bowie.
Play David Bowie, Iron Maiden or Five Finger Death Punch.
Play not David Bowie, but Iron Maiden.
Don't play David Bowie.
Playing David Bowie would be nice.
My grandmother wants me to play David Bowie.
Playing David Bowie would be terrible.
Don't stop.
Don't pause.
Resume.
Don't resume.
Play rock.
Play rock music.


TODO:
from not working for now
Play very very hard rock.

"""
import spacy
from termcolor import colored
import mpd_provider_module as mpm
import verbalizer
from flask import Flask
app = Flask(__name__)

nlp = spacy.load("en_core_web_lg")

print("READY for requests")

@app.route("/<input>")
def parse(input):
    print("REQUEST: " + input)
    
    #start with part of speech tagging
    doc = nlp(input)

    response = "initial value aka no instruction found."
    
    for token in doc:
        if token.lemma_ == "play":
            print("PLAY instruction found")
            # check if there is a negation
            if is_negative(token) != True:
                if token.nbor().lemma_ == "next":
                    response = playNext()
                elif token.nbor().lemma_ == "random":
                    response = playRandom()
                elif token.nbor().lemma_ == "a" and token.nbor().nbor().lemma == "random":
                    response = playRandom()
                elif token.nbor().lemma_ == "something":
                    response = playRandom()
                else:
                    response = play(doc)
            else:
                # input is something like: Don't play David Bowie.
                response = verbalizer.getDontPlayText()
            break
        elif token.lemma_ == "stop":
            print("STOP instruction found")
            if is_negative(token) != True:
                response = stop()
            else:
                # input is something like: Don't stop.
                response = verbalizer.getDontStopPauseText()
            break
        elif token.lemma_ == "pause":
            print("PAUSE instruction found")
            if is_negative(token) != True:
                response = pause()
            else:
                # input is something like: Don't pause.
                response = verbalizer.getDontStopPauseText()
            break
        elif token.lemma_ == "resume" or token.lemma_ == "continue":
            print("RESUME instruction found")
            if is_negative(token) != True:
                response = resume()
            else:
                # input is something like: Don't resume.
                response = verbalizer.getDontResumeText()
            break
        elif token.lemma_ == "next": #TODO: check lenght(doc) == 1
            print("NEXT instruction found")
            response = playNext()
            break

    return ">> " + response + "\n"

def is_negative(token):
    # if there is a negation for play, it is a children of play in the graph
    negation = False
    for child in token.children:
        #print(child.text + " " + child.dep_)
        if child.dep_ == "neg":
            print("NEG found")
            negation = True
            break
    return negation

def play(doc):
    chunks = list(doc.noun_chunks)
    # determine if this chunks are gernes, artists or songs
    # for gerne:
    # should be only one chunk with one word or <GERNE> + music
    print("CHUNKS: " + str(chunks))

    arguments = []    
    for chunk in chunks:
        arguments.append(str(chunk))

    mpm.playGerneSongArtist(arguments)

    return verbalizer.getOkText()

def stop():
    mpm.stop()
    return verbalizer.getOkText()

def pause():
    mpm.pause()
    return verbalizer.getOkText()

def resume():
    mpm.resume()
    return verbalizer.getOkText()

def playNext():
    mpm.playNext()
    return verbalizer.getOkText()

def playRandom():
    mpm.playRandom()
    return verbalizer.getOkText()

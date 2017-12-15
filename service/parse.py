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


===================
|| Conversations ||
===================
"Play Oompa Loompa music."
>> Hmm.. I didn't get that. Should i play rock?
"Yes"
>> Ok. Here we go.
------------------------------
"Play Oompa Loompa music."
>> Hmm.. I didn't get that. Should i play rock?
"No"
>> Oh, ok.
------------------------------
"Play something."
>> Tell me an artist, song or gerne. Or do you want me to play a random song?
"David Bowie"
>> Ok. Have fun!
------------------------------
"Play something."
>> Tell me an artist, song or gerne. Or do you want me to play a random song?
"random song"
>> Ok. Have fun!
------------------------------

TODO:
Play very very hard rock.

"""
import spacy
from termcolor import colored
import mpd_provider_module as mpm
import verbalizer
from enum import Enum
from expiringdict import ExpiringDict
from conversationState import ConversationStateEnum, ConversationState
from response import Response, ErrorCodeEnum
from random import randint
from flask import Flask, request
app = Flask(__name__)

nlp = spacy.load("en_core_web_lg")


# conversation state is stored in a expiringdict
# note that there an additional state which is also the initial state which is considered if no state is stored

states = ExpiringDict(max_len=100, max_age_seconds=10)
# states[userid] = ConversationState(ConversationStateEnum.AwaitYesOrNo, "Ask for David Bowie?")


print("READY for requests")

@app.route("/")
def parseREST():
    input = request.args.get('input')
    userid = request.args.get('userid')
    print("REQUEST from id " + userid + ": " + input)
    return parse(input, userid)


def parse(input, userid):
    #start with part of speech tagging
    doc = nlp(input)

    response = "initial value aka no instruction found."

    try:
        if states.get(userid) == None:
            for token in doc:
                if token.lemma_ == "play":
                    print("PLAY instruction found")
                    # check if there is a negation
                    if is_negative(token) != True:
                        if token.nbor().lemma_ == "next":
                            response = playNext()
                        elif token.nbor().lemma_ == "random":
                            response = playRandom()
                        elif token.nbor().lemma_ == "a" and token.nbor().nbor().lemma_ == "random":
                            response = playRandom()
                        elif token.nbor().lemma_ == "something":
                            # ask for a artist/songname or gerne
                            states[userid] = ConversationState(ConversationStateEnum.AwaitSongArtistOrGerne)
                            return verbalizer.getQuestionForArtistSongGerneOrRandom()
                        else:
                            response = play(doc, userid)
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
                elif token.lemma_ == "next" and len(doc) <= 2:
                    print("NEXT instruction found")
                    response = playNext()
                    break

        elif states.get(userid).state == ConversationStateEnum.AwaitYesOrNo:
            print("Yes or no")
            state = states.pop(userid) # remove state
            if doc[0].lemma_ == "yes":
                response = parse(state.suggestion, userid) # simply call with a suggestion like 'Play rock.'
            else:
                response = "Oh, ok."
        elif states.get(userid).state == ConversationStateEnum.AwaitSongArtistOrGerne:
            print("Song, Gerne or Artist")
            states.pop(userid) # remove state
            return parse("Play " + str(doc), userid)
    except Exception as e: # specify Exception
        response = verbalizer.getConnectionError()
        raise e

    return ">>" + response + "\n"

def is_negative(token):
    # if there is a negation for play, it is a children of play in the graph
    for child in token.children:
        #print(child.text + " " + child.dep_)
        if child.dep_ == "neg":
            print("NEG found")
            return True
    return False

def play(doc, userid):
    chunks = list(doc.noun_chunks)
    # determine if this chunks are gernes, artists or songs
    # for gerne:
    # should be only one chunk with one word or <GERNE> + music
    print("CHUNKS: " + str(chunks))

    arguments = []
    for chunk in chunks:
        arguments.append(str(chunk))

    response = verbalizer.getOkText()


    arg_gernes = []
    for chunk in arguments:
        gerne = mpm.trimGerne(chunk)
        if mpm.isGerne(gerne) == True:
            arg_gernes.append(gerne)

    print(arg_gernes)

    if len(arguments) == 0:
        mpm.playOrResume()
    elif len(arg_gernes) < len(arguments) and mpm.containsSongOrArtist(arguments):
        mpm.playSongOrArtist(arguments)
    elif len(arg_gernes) > 0:
        mpm.playGernes(arg_gernes)
    else:
        # no gerne song artist found, check for alternate suggestions
        # TODO: suggest a song / gerne / artist depending
        suggestion = mpm.gernes[randint(0, len(mpm.gernes)-1)]
        states[userid] = ConversationState(ConversationStateEnum.AwaitYesOrNo, "Play " + suggestion + ".")
        response = verbalizer.getAlternatePlaySuggestion(suggestion)
    return response

def stop():
    mpm.stop() # TODO: check response
    return verbalizer.getOkText()

def pause():
    mpm.pause() # TODO: check response
    return verbalizer.getOkText()

def resume():
    mpm.resume() # TODO: check response
    return verbalizer.getOkText()

def playNext():
    mpm.playNext() # TODO: check response
    return verbalizer.getOkText()

def playRandom():
    mpm.playRandom() # TODO: check response
    return verbalizer.getOkText()

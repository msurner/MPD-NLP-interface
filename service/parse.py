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
from flask import Flask
app = Flask(__name__)

nlp = spacy.load("en_core_web_lg")

# for developement there is only one user for now
userid = 1

# conversation state is stored in a expiringdict
# note that there an additional state which is also the initial state which is considered if no state is stored

states = ExpiringDict(max_len=100, max_age_seconds=10)
# states[userid] = ConversationState(ConversationStateEnum.AwaitYesOrNo, "Ask for David Bowie?")


print("READY for requests")

@app.route("/<input>")
def parse(input):
    print("REQUEST: " + input)

    #start with part of speech tagging
    doc = nlp(input)

    response = "initial value aka no instruction found."

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
                    elif token.nbor().lemma_ == "a" and token.nbor().nbor().lemma == "random":
                        response = playRandom()
                    elif token.nbor().lemma_ == "something":
                        # ask for a artist/songname or gerne
                        states[userid] = ConversationState(ConversationStateEnum.AwaitSongArtistOrGerne)
                        return verbalizer.getQuestionForArtistSongGerneOrRandom()
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
            elif token.lemma_ == "next" and len(doc) <= 2:
                print("NEXT instruction found")
                response = playNext()
                break
                
    elif states.get(userid).state == ConversationStateEnum.AwaitYesOrNo:
        print("Yes or no")
        state = states.pop(userid) # remove state
        if doc[0].lemma_ == "yes":
            return parse(state.suggestion) # simply call with a suggestion like 'Play rock.'
        else:
            return "Oh, ok."
    elif states.get(userid).state == ConversationStateEnum.AwaitSongArtistOrGerne:
        print("Song, Gerne or Artist")
        states.pop(userid) # remove state
        return parse("Play " + str(doc))
    return ">> " + response + "\n"

def is_negative(token):
    # if there is a negation for play, it is a children of play in the graph
    for child in token.children:
        #print(child.text + " " + child.dep_)
        if child.dep_ == "neg":
            print("NEG found")
            return True
    return False

def play(doc):
    chunks = list(doc.noun_chunks)
    # determine if this chunks are gernes, artists or songs
    # for gerne:
    # should be only one chunk with one word or <GERNE> + music
    print("CHUNKS: " + str(chunks))

    arguments = []
    for chunk in chunks:
        arguments.append(str(chunk))

    response = mpm.playGerneSongArtist(arguments)

    if response.errorCode == ErrorCodeEnum.Success:
        return verbalizer.getOkText()
    elif response.errorCode == ErrorCodeEnum.ParsingError:
        states[userid] = ConversationState(ConversationStateEnum.AwaitYesOrNo, "Play " + response.suggestion + ".")
        return verbalizer.getAlternatePlaySuggestion(response.suggestion)
    elif response.errorCode == ErrorCodeEnum.ConnectionError:
        return verbalizer.getConnectionError()

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

"""
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
Don't stop.
Don't pause.
Resume.
Don't resume.
Play rock music or electro house.
Continue.
Stop playing
Play a random song.
Play random song.
Play something.
Play next.
Next.
Play rock music like Heroes from David Bowie.
Play previous song.
Previous.
Previous song.
Next song.
Clear current playlist.
Repeat playlist.
Repeat song.
Update Database.

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
>> Tell me an artist, song or genre. Or do you want me to play a random song?
"David Bowie"
>> Ok. Have fun!
------------------------------
"Play something."
>> Tell me an artist, song or genre. Or do you want me to play a random song?
"random song"
>> Ok. Have fun!
------------------------------

For more instruction see the README.md file!

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
import logging as log
import string
from flask import Flask, request
app = Flask(__name__)

nlp = spacy.load("en_core_web_lg")


# conversation state is stored in a expiringdict
# note that there an additional state which is also the initial state which is considered if no state is stored

states = ExpiringDict(max_len=100, max_age_seconds=20)
verbose = True

if verbose:
    log.basicConfig(format="%(levelname)s: %(message)s", level=log.DEBUG)
    log.info("Verbose output.")
else:
    log.basicConfig(format="%(levelname)s: %(message)s")


print("READY for requests")

@app.route("/", methods=['GET'])
def parseService():
    input = request.args.get('input')
    userid = request.args.get('userid')
    log.info("REQUEST from id " + userid + ": " + input)
    return parse(input, userid)

# to provide compability for bierschi's speech_processing
@app.route("/", methods=['POST'])
def parseREST():
    bytes_obj = request.get_data()
    resp_string = bytes_obj.decode('utf-8')
    userid = 1
    return parse(resp_string, userid)

def parse(input, userid):
    # start with part of speech tagging
    doc = nlp(input)

    response = ""

    try:
        if states.get(userid) == None:

            # search for keywords like play, stop, pause, etc..
            for token in doc:
                if token.lemma_ == "play":
                    log.info("PLAY instruction found")
                    # check if there is a negation
                    if is_negative(token) != True:
                        if token.nbor().lemma_ == "next":
                            response = playNext()
                        elif len(doc) > 1 and token.nbor().lemma_ == "previous":
                            response = playPrevious()
                        elif len(doc) > 1 and token.nbor().lemma_ == "random":
                            response = playRandom()
                        elif len(doc) > 2 and token.nbor().lemma_ == "a" and token.nbor().nbor().lemma_ == "random":
                            response = playRandom()
                        elif len(doc) > 1 and token.nbor().lemma_ == "something":
                            # ask for a artist/songname or genre
                            states[userid] = ConversationState(ConversationStateEnum.AwaitSongArtistOrGenre)
                            response = verbalizer.getQuestionForArtistSongGenreOrRandom()
                            mpm.speak(response)
                            response
                        else:
                            response = play(doc, userid)
                    else:
                        # input is something like: Don't play David Bowie.
                        response = verbalizer.getDontPlayText()
                        mpm.speak(response)
                    break
                elif token.lemma_ == "stop":
                    log.info("STOP instruction found")
                    # check if there is a negation
                    if is_negative(token) != True:
                        response = stop()
                    else:
                        # input is something like: Don't stop.
                        response = verbalizer.getDontStopPauseText()
                        mpm.speak(response)
                    break
                elif token.lemma_ == "pause":
                    log.info("PAUSE instruction found")
                    # check if there is a negation
                    if is_negative(token) != True:
                        response = pause()
                    else:
                        # input is something like: Don't pause.
                        response = verbalizer.getDontStopPauseText()
                        mpm.speak(response)
                    break
                elif token.lemma_ == "resume" or token.lemma_ == "continue":
                    log.info("RESUME instruction found")
                    # check if there is a negation
                    if is_negative(token) != True:
                        response = resume()
                    else:
                        # input is something like: Don't resume.
                        response = verbalizer.getDontResumeText()
                        mpm.speak(response)
                    break
                elif token.lemma_ == "next" and len(doc) <= 3:
                    log.info("NEXT instruction found")
                    response = playNext()
                    break
                elif token.lemma_ == "previous" and len(doc) <= 3:
                    log.info("PREVIOUS instruction found")
                    response = playPrevious()
                    break
                elif token.lemma_ == "clear":
                    log.info("CLEAR instruction found")
                    if is_negative(token) != True and 'playlist' in (str(word).lower() for word in doc):
                        response = clearCurrentPlaylist()
                    break
                elif token.lemma_ == "update":
                    log.info("UPDATE instruction found")
                    if is_negative(token) != True and 'database' in (str(word).lower() for word in doc):
                        response = updateDatabase()
                    break
                elif token.lemma_ == "repeat":
                    log.info("REPEAT instruction found")
                    if is_negative(token) != True:
                        if 'playlist' in (str(word).lower() for word in doc):
                            response = repeatPlaylist()
                        elif 'song' in (str(word).lower() for word in doc):
                            response = repeatSong()
                    break

        # Await yes or no, since a question was asked
        elif states.get(userid).state == ConversationStateEnum.AwaitYesOrNo:
            log.info("Yes or no")
            state = states.pop(userid) # remove state
            if doc[0].lemma_ == "yes":
                response = parse(state.suggestion, userid) # simply call with a suggestion like 'Play rock.'
            else:
                response = "Oh, ok."

            mpm.speak(response)
        elif states.get(userid).state == ConversationStateEnum.AwaitSongArtistOrGenre:
            log.info("Song, Genre or Artist")
            states.pop(userid) # remove state
            return parse("Play " + str(doc), userid)
    except Exception as e:
        response = verbalizer.getConnectionError()
        mpm.speak(response)
        raise e

    # no keyword was found
    if response == "":
        suggestion = mpm.getRandomGenre()
        states[userid] = ConversationState(ConversationStateEnum.AwaitYesOrNo, "Play " + suggestion + ".")
        response = verbalizer.getAlternatePlaySuggestion(suggestion)
        mpm.speak(response)

    return response

def is_negative(token):
    # if there is a negation for play, it is a children of play in the graph
    for child in token.children:
        if child.dep_ == "neg":
            log.info("NEG found")
            return True
    return False

def play(doc, userid):
    chunks = list(doc.noun_chunks)
    # determine if this chunks are genres, artists or songs
    # for genre:
    # should be only one chunk with one word or <GENRE> + music
    log.info("CHUNKS: " + str(chunks))

    arguments = []
    for chunk in chunks:
        arguments.append(str(chunk))

    # in some cases chunk analysis takes play within the chunk
    if len(arguments) > 0 and arguments[0].lower().startswith("play") and doc.text.lower().count("play") == arguments[0].lower().count("play"):
        arguments[0] = arguments[0][5:]
        arguments.remove("")

    # if chunk analysis fails, set chunk manually (this happens in short instructions)
    if len(arguments) == 0:
        table = str.maketrans({key: None for key in string.punctuation})
        arguments.append(doc.text[5:].translate(table))

    response = verbalizer.getOkText()


    arg_genres = []
    for chunk in arguments:
        genre = mpm.trimGenre(chunk)
        if mpm.isGenre(genre) == True:
            arg_genres.append(genre)

    log.info(arg_genres)

    if len(arguments) == 0: # Simple 'Play.' instruction
        mpm.speak(response)
        mpm.playOrResume()
    elif len(arg_genres) < len(arguments) and mpm.containsSongOrArtist(arguments): # Prefer song/artist
        mpm.speak(response)
        mpm.playSongOrArtist(arguments)
    elif len(arg_genres) > 0: # no songs/artist found, play genre if there are some
        mpm.speak(response)
        mpm.playGenres(arg_genres)
    else:
        # no genre, song or artist found, check for alternate suggestions
        # suggest a random genre
        suggestion = mpm.getRandomGenre()
        states[userid] = ConversationState(ConversationStateEnum.AwaitYesOrNo, "Play " + suggestion + ".")
        response = verbalizer.getAlternatePlaySuggestion(suggestion)
        mpm.speak(response)
    return response

def stop():
    response = verbalizer.getOkText()
    mpm.speak(response)
    mpm.stop()
    return response

def pause():
    response = verbalizer.getOkText()
    mpm.speak(response)
    mpm.pause()
    return response

def resume():
    response = verbalizer.getOkText()
    mpm.speak(response)
    mpm.resume()
    return response

def playNext():
    response = verbalizer.getOkText()
    mpm.speak(response)
    mpm.playNext()
    return response

def playPrevious():
    response = verbalizer.getOkText()
    mpm.speak(response)
    mpm.playPrevious()
    return response

def playRandom():
    response = verbalizer.getOkText()
    mpm.speak(response)
    mpm.playRandom()
    return response

def clearCurrentPlaylist():
    response = verbalizer.getOkText()
    mpm.speak(response)
    mpm.clearCurrentPlaylist()
    return response

def updateDatabase():
    response = verbalizer.getOkText()
    mpm.speak(response)
    mpm.updateDatabase()
    return response

def repeatSong():
    response = verbalizer.getOkText()
    mpm.speak(response)
    mpm.repeatSong()
    return response

def repeatPlaylist():
    response = verbalizer.getOkText()
    mpm.speak(response)
    mpm.repeatPlaylist()
    return response

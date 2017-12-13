from termcolor import colored
from speech_processing.music_player.mpd_connection import ControlMPD
from response import Response, ErrorCodeEnum
from random import randint

color = "green"

gernes = ["rock", "hard rock", "alternative", "electro house"]
songs = [ "heroes" ]
artists = [ "david bowie", "five finger death punch"]

# not working for now - ConnectionRefusedError: [Errno 111] Connection refused
#mpdcontrol = ControlMPD("127.0.0.1")

def playGerneSongArtist(arguments):
    # determine if this chunks are gernes, artists or songs
    # for gerne:
    # should be only chunks with one gerne or <GERNE> + music
    # if there are some gerne chunks and a artist, rather play the artist.
    # if something unknown and a known gerne/artist/song is given, ignore the unknown
    # if there is something unknown like 'very very hard rock' recursiveley remove the first? word and parse each argument
    response = Response()
    arg_gernes = []
    for chunk in arguments:
        gerne = trimGerne(chunk)
        if isGerne(gerne) == True:
            arg_gernes.append(gerne)

    if len(arguments) == 0:
       playOrResume()
    elif len(arg_gernes) < len(arguments) and containsSongOrArtist(arguments):
       print(colored("RESULT: playSongArtist(" + ", ".join(arguments) + ")", color))
    elif len(arg_gernes) > 0:
       playGernes(arg_gernes)
    else:
        # no gerne song artist found, check for alternate suggestions
        response.errorCode = ErrorCodeEnum.ParsingError
        # TODO: suggest a song / gerne / artist depending
        response.suggestion = gernes[randint(0, len(gernes)-1)]

    return response

def isGerne(gerne):
    if trimGerne(gerne).lower() in gernes:
        return True;
    return False;

def trimGerne(gerne):
    # cut ' music' in the end
    music = "music"
    if gerne.lower().endswith(music):
        gerne = gerne[:len(gerne)-(len(music)+1)]
    return gerne

def playGernes(gernes):
    # for gerne:
    # should be only one chunk with one word or <GERNE> + music
    print(colored("RESULT: playGernes(" + ", ".join(gernes) + ")", color))

def containsSongOrArtist(arguments):
    for argument in arguments:
        if isArtist(argument) or isSong(argument):
            return True
    return False

def isArtist(argument):
    return argument.lower() in artists

def isSong(argument):
    return argument.lower() in songs

def stop():
    print(colored("RESULT: stop()", color))

def pause():
    print(colored("RESULT: pause()", color))

def resume():
    print(colored("RESULT: resume()", color))

def playOrResume():
    print(colored("RESULT: playOrResume()", color))

def playRandom():
    print(colored("RESULT: playRandom()", color))

def playNext():
    print(colored("RESULT: playNext()", color))

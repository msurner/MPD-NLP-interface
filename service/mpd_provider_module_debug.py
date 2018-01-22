from termcolor import colored
from speech_processing.music_player.mpd_connection import ControlMPD
from response import Response, ErrorCodeEnum
from random import randint

# use this module to test parse.py without MPD-server

color = "green"

# This simulates the MPD-database
genres = ["rock", "hard rock", "alternative", "electro house"]
songs = [ "heroes" ]
artists = [ "david bowie", "five finger death punch"]


def trimGenre(genre):
    print("trimgenre " + genre)
    # cut ' music' in the end
    music = "music"
    if genre.lower().endswith(music):
        genre = genre[:len(genre)-(len(music)+1)]
    return genre

def containsSongOrArtist(arguments):
    for argument in arguments:
        if isArtist(argument) or isSong(argument):
            return True
    return False

def playSongOrArtist(arguments):
    print(colored("RESULT: playSongOrArtist(" + ", ".join(arguments) + ")", color))

def isGenre(genre):
    if trimGenre(genre).lower() in genres:
        return True;
    return False;

def getRandomGenre():
    genres = ["rock", "hard rock", "alternative", "electro house"]
    return genres[randint(0, len(genres)-1)]

# genres is a list of genres f. e. ['rock', 'electro house'] or ['rock']
def playGenres(genres):
    print(colored("RESULT: playGenres(" + ", ".join(genres) + ")", color))

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

def playPrevious():
    print(colored("RESULT: playPrevious()", color))

def clearCurrentPlaylist():
    print(colored("RESULT: clearCurrentPlaylist()", color))

def playPreviousSong():
    print(colored("RESULT: playPreviousSong()", color))

def repeatPlaylist():
    print(colored("RESULT: repeatPlaylist()", color))

def repeatSong():
    print(colored("RESULT: repeatSong()", color))

def updateDatabase():
    print(colored("RESULT: updateDatabase()", color))

def speak(message):
    print(colored("SPOKEN_Output: '" + message + "'", "red"))

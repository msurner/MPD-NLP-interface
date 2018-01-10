from termcolor import colored
from speech_processing.music_player.mpd_connection import ControlMPD
from response import Response, ErrorCodeEnum
from random import randint

color = "green"

gernes = ["rock", "hard rock", "alternative", "electro house"]
songs = [ "heroes" ]
artists = [ "david bowie", "five finger death punch"]

# not working for now - ConnectionRefusedError: [Errno 111] Connection refused
mpdcontrol = ControlMPD("127.0.0.1",6600)

def trimGerne(gerne):
    print("trimgerne " + gerne)
    # cut ' music' in the end
    music = "music"
    if gerne.lower().endswith(music):
        gerne = gerne[:len(gerne)-(len(music)+1)]
    return gerne

def containsSongOrArtist(arguments):
    for argument in arguments:
        if isArtist(argument) or isSong(argument):
            return True
    return False

def playSongOrArtist(arguments):
    print(colored("RESULT: playSongOrArtist(" + ", ".join(arguments) + ")", color))

# TODO: @bierschi: Move to MPD-Command
def isGerne(gerne):
    if trimGerne(gerne).lower() in gernes:
        return True;
    return False;

# TODO: @bierschi: Move to MPD-Command
def getRandomGerne():
    gernes = ["rock", "hard rock", "alternative", "electro house"]
    return gernes[randint(0, len(gernes)-1)]

# TODO: @bierschi: Move to MPD-Command
# gernes is a list of gernes f. e. ['rock', 'electro house'] or ['rock']
def playGernes(gernes):
    print(colored("RESULT: playGernes(" + ", ".join(gernes) + ")", color))

# TODO: @bierschi: Move to MPD-Command
def isArtist(argument):
    return argument.lower() in artists

# TODO: @bierschi: Move to MPD-Command
def isSong(argument):
    return argument.lower() in songs

# TODO: @bierschi: Move to MPD-Command
def stop():
    print(colored("RESULT: stop()", color))

# TODO: @bierschi: Move to MPD-Command
def pause():
    print(colored("RESULT: pause()", color))

# TODO: @bierschi: Move to MPD-Command
def resume():
    print(colored("RESULT: resume()", color))

# TODO: @bierschi: Move to MPD-Command
def playOrResume():
    print(colored("RESULT: playOrResume()", color))

# TODO: @bierschi: Move to MPD-Command
def playRandom():
    print(colored("RESULT: playRandom()", color))

# TODO: @bierschi: Move to MPD-Command
def playNext():
    print(colored("RESULT: playNext()", color))

# TODO: @bierschi: Move to MPD-Command
def playPrevious():
    print(colored("RESULT: playPrevious()", color))

# TODO: @bierschi: Move to MPD-Command
def clearCurrentPlaylist():
    print(colored("RESULT: clearCurrentPlaylist()", color))

# TODO: @bierschi: Move to MPD-Command
def playPreviousSong():
    print(colored("RESULT: playPreviousSong()", color))

# TODO: @bierschi: Move to MPD-Command
def repeatPlaylist():
    print(colored("RESULT: repeatPlaylist()", color))

# TODO: @bierschi: Move to MPD-Command
def repeatSong():
    print(colored("RESULT: repeatSong()", color))

# TODO: @bierschi: Move to MPD-Command
def updateDatabase():
    print(colored("RESULT: updateDatabase()", color))

def speak(message):
    ## BING_KEY not known
    # tts = TextToSpeech(bing_key=BING_KEY, language='united_states', gender='Female')
    # resp = tts.request_to_bing(text=message)
    # tts.play_request(resp)
    print(colored("SPOKEN_Output: '" + message + "'", "red"))

from termcolor import colored
from speech_processing.music_player.mpd_connection import ControlMPD
from speech_processing.speech_control.text_to_speech import TextToSpeech
from response import Response, ErrorCodeEnum
from random import randint
from time import sleep

color = "green"

mpdcontrol = ControlMPD("127.0.0.1", 6600)

def trimGerne(gerne):
    # cut ' music' in the end
    music = "music"
    if gerne.lower().endswith(music):
        gerne = gerne[:len(gerne)-(len(music)+1)]
    return gerne

def containsSongOrArtist(arguments):
    for argument in arguments:
        if mpdcontrol.is_artist_in_db(argument) or mpdcontrol.is_title_in_db(argument):
            return True
    return False

def playSongOrArtist(arguments):
    print(colored("RESULT: playSongOrArtist(" + ", ".join(arguments) + ")", color))
    for i in arguments:
        song_pos = mpdcontrol.add_artist_to_pl(i)
        mpdcontrol.play(song_pos)
        print(mpdcontrol.get_current_song_playlist())
        sleep(10)

def isGerne(gerne):
    gerne = trimGerne(gerne).lower()
    if mpdcontrol.is_genre_in_db(gerne):
        return True
    else:
        return False

# TODO: @bierschi: Move to MPD-Command
def getRandomGerne():
    gernes = ["rock", "hard rock", "alternative", "electro house"]
    return gernes[randint(0, len(gernes)-1)]

# gernes is a list of gernes f. e. ['rock', 'electro house'] or ['rock']
def playGernes(gernes):
    print(colored("RESULT: playGernes(" + ", ".join(gernes) + ")", color))
    for i in gernes:
        song_pos = mpdcontrol.add_genre_to_pl(i)
        mpdcontrol.play(song_pos)
        print(mpdcontrol.get_current_song_playlist())
        sleep(10)

def stop():
    print(colored("RESULT: stop()", color))
    mpdcontrol.stop()

def pause():
    print(colored("RESULT: pause()", color))
    mpdcontrol.pause()

def resume():
    print(colored("RESULT: resume()", color))
    mpdcontrol.play()

def playOrResume():
    print(colored("RESULT: playOrResume()", color))
    mpdcontrol.play()

def playRandom():
    print(colored("RESULT: playRandom()", color))
    mpdcontrol.shuffle()
    mpdcontrol.set_random()
    mpdcontrol.play()

def playNext():
    print(colored("RESULT: playNext()", color))
    mpdcontrol.next()

def playPrevious():
    print(colored("RESULT: playPrevious()", color))
    mpdcontrol.previous()

def clearCurrentPlaylist():
    print(colored("RESULT: clearCurrentPlaylist()", color))
    mpdcontrol.clear_current_playlist()

def repeatPlaylist():
    print(colored("RESULT: repeatPlaylist()", color))
    mpdcontrol.set_repeat()

def repeatSong():
    print(colored("RESULT: repeatSong()", color))

def updateDatabase():
    print(colored("RESULT: updateDatabase()", color))
    mpdcontrol.update_database()

def speak(message):
    ## BING_KEY not known
    is_playing = True;
    if(not is_playing):
        tts = TextToSpeech(bing_key="1f02ecb0273049abb906131362d91950", language='united_states', gender='Female')
        resp = tts.request_to_bing(text=message)
        tts.play_request(resp)
        print(colored("SPOKEN_Output: '" + message + "'", "red"))

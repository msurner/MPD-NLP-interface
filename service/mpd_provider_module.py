from termcolor import colored

color = "green"

def playSongArtist(arguments):
    # determine if this chunks are gernes, artists or songs
    # for gerne:
    # should be only one chunk with one word or <GERNE> + music
    print(colored("RESULT: playGerneSongArtist(" + ", ".join(arguments) + ")", color))

def isGerne(gerne):
    if gerne.lower() == 'rock':
        return True;
    return False;

def playGerne(gerne):
    # determine if this chunks are gernes, artists or songs
    # for gerne:
    # should be only one chunk with one word or <GERNE> + music
    print(colored("RESULT: playGerne(" + gerne + ")", color))


def stop():
    print(colored("RESULT: stop()", color))

def pause():
    print(colored("RESULT: pause()", color))

def resume():
    print(colored("RESULT: resume()", color))

def playOrResume():
    print(colored("RESULT: playOrResume()", color))

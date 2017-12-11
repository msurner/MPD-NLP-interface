from termcolor import colored

color = "green"

gernes = ["rock", "hard rock", "alternative", "electro house"]

def playGerneSongArtist(arguments):
    # determine if this chunks are gernes, artists or songs
    # for gerne:
    # should be only chunks with one gerne or <GERNE> + music
    is_gerne = True
    for chunk in arguments:
        if isGerne(trimGerne(chunk)) == False:
            is_gerne = False
            break
    if is_gerne:
        print(colored("RESULT: playGerne(" + ", ".join([trimGerne(argument) for argument in arguments]) + ")", color))
    else:
        print(colored("RESULT: playSongArtist(" + ", ".join(arguments) + ")", color))

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

def playGerne(gerne):
    # determine if this chunks are gernes, artists or songs
    # for gerne:
    # should be only one chunk with one word or <GERNE> + music
    print(colored("RESULT: playGerne(" + ", ".join(gerne) + ")", color))


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

# MPD-NLP-interface
This implements a natural language user interface for MPD (Music Player Daemon). It provides a restful webservice via flask which expects a instruction as string and a userid.
To run the webservice type:
```
./flask/startServer.sh ./service/parse.py
```
To run a request type:
```
./flask/sendRequest.sh "Play David Bowie."
```

## Structure

```
/flask          -> scripts to start server or send requests
/service        -> provides actual service content where instructions are parsed and MPD-commands are used
/locust         -> stress tests
/spacy_analysis -> some scripts to explore spacy-features and testing how to parse new instructions

```

## Getting started
Download with
```
git clone --recursive
```
or fetch the submodule afterwards with:
```
git submodule update --recursive --init
```

Install python and (at least on Ubuntu 17.10) curl:
```
sudo apt install python3 python3-pip curl
```
Install dependencies:
```
pip3 install flask
pip3 install expiringdict
pip3 install spacy
pip3 install python-mpd2
```
Download model:
```
python3 -m spacy download en_core_web_lg
```
Due to conflicting folder structures you'll have to modify `service/speech_processing/speech_control/text_to_speech.py`: change 
```
from resources.supported_languages import TTSLanguageCommand 
```
to 
```
from ..resources.supported_languages import TTSLanguageCommand
```

## Supported instructions
### Working
```
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
```

### Conversations
Conversations are possible, since there is an internal state for each user.
The state expires after a specified duration f.e. 10 seconds.
```
"Play Oompa Loompa music."
>> Hmm.. I didn't get that. Should i play rock?
"Yes"
>> Ok. Here we go.
```
```
"Play Oompa Loompa music."
>> Hmm.. I didn't get that. Should i play rock?
"No"
>> Oh, ok.
```
```
"Play something."
>> Tell me an artist, song or gerne. Or do you want me to play a random song?
"David Bowie"
>> Ok. Have fun!
```
```
"Play something."
>> Tell me an artist, song or gerne. Or do you want me to play a random song?
"random song"
>> Ok. Have fun!
```

## Users
This service provides support for more then one client. A user is simply specified by its given `userid` parameter.

## Testing
For testing without a MPD-server, you can import the `mpd_provider_module_debug` instead of `mpd_provider_module`.
Instead of MPD-instructions, you can see an output on console.

## Stress test
You can do a stress test based on locust with following commands:
```
pip3 install locustio
locust -f locust/locustfile.py
```
Navigate to <http://127.0.0.1:8089> specify number of users, hatchrate and start.

Feel free to specify some test cases in the locustfile.py!
In my tests, the service performs pretty well (on debug mode).


## Ideas
### Sentiment analysis
_"Playing David Bowie would be terrible."_ seems to need a sentiment analysis like in <http://nlp.stanford.edu:8080/sentiment/rntnDemo.html>.
-> But _"Playing David Bowie, since this is a very bad day."_ would return negative result. In addition spaCy doesn't provide a pre-trained model.
Sentiment analysis would help in a few cases but leads to misinterpretation of much clearer instructions.
Therefore sentiment analysis is not used.

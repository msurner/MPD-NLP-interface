# MPD-NLP-interface
This implements a natural language user interface for MPD (Music Player Deamon). It provides a restful webservice via flask and expects a string.
To run the webservice type: `./startServer.sh ../path/to/parse.py`. 
To run a request type `./sendRequest.sh "Play David Bowie."`.

## Ideas
_"Playing David Bowie would be terrible."_ seems to need a sentiment analysis like in <http://nlp.stanford.edu:8080/sentiment/rntnDemo.html>.
-> But _"Playing David Bowie, although this is a very bad day."_ would return negative result. In addition spaCy doesn't provide a pre-trained model.

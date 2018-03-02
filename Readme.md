# FB chat data chatbots
Two chatbots trained on my Facebook Messenger chat data to talk like me. One uses the [Doc2Vec implementation](https://radimrehurek.com/gensim/models/doc2vec.html) of the Python library ```gensim``` and the other is based on the library [```ChatterBot```](http://chatterbot.readthedocs.io/en/stable/). 
As my chat data is not too plentiful (~70k messages sent by me and ~35k decent input-output pairs) the strategy was to get the user input sentence, find the most similar recorded input and return the corresponding recorded output. 
#### The bots
```Doc2Vec``` is well suited for this task (and was very performant), but likely needs a corpus much larger than my chat history. I also did not experiment thorougly with parameters such as word vector dimension count. ```ChatterBot```, while preferring to be trained on full conversations, needed to be trained simply on input-output pairs to only learn "character" from me. This may have been one of the reasons for it being much slower. For responses to not take minutes, the bot based on ```ChatterBot``` was only trained on 20% of all data. Despite that, its responses generally seemed slightly more on-topic and it was less prone to repeating itself like the bot based on ```Doc2Vec```. 

![Training](https://i.imgur.com/fDzBPDe.png)
![Chatting](https://i.imgur.com/ySXJmeZ.png)

#### Running
My chat data and the models trained on it have not been included for obvious reasons. After downloading your own FB data ([instructions](https://www.facebook.com/help/131112897028467)) (change your FB language to English and the time format to 24h beforehand), place the ```messages``` folder in it into the same folder as all the scripts, delete all subfolders of ```messages```, leaving only the html files and run in succession ```scrape.py```, ```datagen.py```, ```train.py``` and finally ```chat.py```.

January 2018  
Andreas Vija
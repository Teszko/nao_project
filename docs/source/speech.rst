
Speech Recognition
==================

Utilize snowboy's hotword detection for detecting a hotword.
Snowboy is a deep neural networkbased hotword and wake word detection toolkit.
It simply analyzes the recording and compares it using pretrained models.
On match it calls a previously saved callback.

Afterwards the phrase is recorded and evaluated using Google Speech Recognition.
Unfortunately there are not any details about its implementation.

For using the Recognizer class create an instance of the class
passing a path to the model_file for hotword detection and a list of keywords. If
nothing is provided it will take the Jarvis Model and red, yellow, and blue as default values.
You may set terminate to True for enabling termination
after any keywords are recognized in a recorded phrase.

Finally call run.

recognizer = Recognizer()
recognizer.run()

You may override methods like on_hotword, on_phrase and on_keyword by subclassing Recognizer or monkey patching them.
That way you are able to control and intervene into the recognizing process perfectly.

A working internet connection is mandatory for using the class
since Google Speech Recognition requires it. Snowboy works offline.

If you want to try out the class call python recognizer.py in your shell.

For more information about Snowboy visit https://snowboy.kitt.ai/.
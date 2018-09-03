import speech_recognition as sr
import snowboydecoder
import os
from os import path

class Recognizer():
    """ Recognizer for phrases and keywords

    Simply create an instance of the class passing a path to the model_file for hotword detection and a list
    of keywords. Afterwards call run.

    recognizer = Recognizer()
    recognizer.run()

    You may overwrite methods like on_hotword, on_phrase and on_keyword by subclassing Recognizer or monkey patching them.
    """

    DEFAULT_MODEL = path.abspath(path.join(path.dirname(__file__), os.pardir, 'res', 'jarvis.umdl'))
    DEFAULT_KEYWORDS = ['red', 'green', 'blue']
    DEFAULT_ADJUSTING_DURATION = 5
    RESOURCE_FILE = path.abspath(path.join(path.dirname(__file__), os.pardir, 'res', 'common.res'))

    def __init__(self, model_file = DEFAULT_MODEL, keywords = DEFAULT_KEYWORDS, terminate = True):
        """ Creates a new Recognizer object

        Args:
            model_file: Path to a .umdl file used for hotword detection
            keywords: List of keywords for focussing the recognition
            terminate: True if recognizer should terminate once a hotword was detected

        Returns:
            New Recognizer object
        """

        self.set_keywords(keywords)
        self.set_terminate(terminate)

        self.load_recognizer()
        self.load_hotword_model(model_file)

    def is_running(self):
        """ Returns True if detection is running"

        Returns:
            True if detection is running
        """
        return hasattr(self, '__running') && self.__running

    def get_keyword_history(self):
        """ Returns the keyword history

        Returns:
            List of keywords that were detected
        """
        return self.__keyword_history

    def set_keywords(self, keywords):
        """ Sets keywords and transforms each keyword to lower

        Args:
            keywords: List of keywords

        Returns:
            None
        """

        self.__keywords = list(map(lambda x: x.lower(), keywords))

    def get_keywords(self):
        """ Returns keywords

        Returns:
            List of keywords
        """

        return self.__keywords

    def set_terminate(self, terminate):
        """ Sets the termination setting

        Args:
            terminate: True if termination is enabled
        Returns:
            None
        """

        self.__terminate = terminate

    def get_terminate(self):
        """ Returns termination setting
        Returns:
            True of termination is enabled
        """

        return self.__terminate

    def load_recognizer(self, adjust_microphone = True):
        """ Loads the recognizer
        Args:
            adjust_microphone: True for adjusting the recognizer using the default microphone

        Returns:
            None
        """

        self.__recognizer = sr.Recognizer()

        if adjust_microphone:
            print ('Adjusting microphone for ' + str(Recognizer.DEFAULT_ADJUSTING_DURATION) + ' seconds...')

            with sr.Microphone() as source:
                self.__recognizer.adjust_for_ambient_noise(source, duration = Recognizer.DEFAULT_ADJUSTING_DURATION)

    def load_hotword_model(self, model_file):
        """ Loads a new hotword model file into the detector

        Args:
            model_file: Path to a .umdl file used for hotword detection

        Returns:
            None
        """

        self.__detector = snowboydecoder.HotwordDetector(model_file, Recognizer.RESOURCE_FILE)

    def on_hotword(self):
        """ Callback which gets called whenever the hotword was detected

        Returns:
            None
        """

        print("Listening for audio...")

        with sr.Microphone() as source:
            audio = self.__recognizer.listen(source)

        try:
            print("Analyzing audio...")
            phrase = self.__recognizer.recognize_google(audio)
            self.on_phrase(phrase)
        except:
            print("No phrase found!")

    def on_phrase(self, phrase):
        """ Callback which gets called whenever a phrase was recorded

        Args:
            phrase: Phrase that was recorded

        Returns:
            None
        """

        print("Phrase \"" + phrase + "\" detected!")
        print("Detecting keywords...")

        phrase = phrase.lower()

        detected = False

        for keyword in self.get_keywords():
            if keyword in phrase:
                detected = True
                self.__keyword_history.append(keyword)
                self.on_keyword(keyword)

        if not detected:
            print("No keywords dectected!")

    def on_keyword(self, keyword):
        """ Callback which gets called whenever a keywords was detected

        Args:
            keyword: Keyword that was detected

        Returns:
            None
        """

        print("Keyword \"" + keyword + "\" detected!")

    def on_interrupt_check(self):
        """ Returns True if termination is enabled and detection should be interrupted

        Returns:
            True if termination is enabled and detection should be interrupted
        """
        return self.get_terminate() and len(self.__keyword_history) > 0

    def run(self):
        print("Listening for hotword...")

        self.__running = True
        self.__keyword_history = []

        self.__detector.start(self.on_hotword, self.on_interrupt_check)

        self.__running = False

if __name__ == '__main__':
    recognizer = Recognizer()
    recognizer.run()

import speech_recognition as sr
import snowboydecoder

class Recognizer():
    """ Recognizer for phrases and keywords

    Simply create an instance of the class passing a path to the model_file for hotword detection and a list
    of keywords. Afterwards call run.

    recognizer = Recognizer()
    recognizer.run()

    You may overwrite methods like on_hotword, on_phrase and on_keyword by subclassing Recognizer or monkey patching them.
    """

    DEFAULT_MODEL = './jarvis.umdl'
    DEFAULT_KEYWORDS = ['red', 'green', 'blue']

    def __init__(self, model_file = DEFAULT_MODEL, keywords = DEFAULT_KEYWORDS):
        """ Creates a new Recognizer object

        Args:
            model_file: Path to a .umdl file used for hotword detection
            keywords: List of keywords for focussing the recognition

        Returns:
            New Recognizer object
        """

        self.set_keywords(keywords)

        self.load_recognizer()
        self.load_hotword_model(model_file)

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

    def load_recognizer(self, adjust_microphone = True):
        """ Loads the recognizer
        Args:
            adjust_microphone: True for adjusting the recognizer using the default microphone

        Returns:
            None
        """

        self.__recognizer = sr.Recognizer()

        if adjust_microphone:
            print ('Adjusting microphone...')

            with sr.Microphone() as source:
                self.__recognizer.adjust_for_ambient_noise(source, duration = 5)

    def load_hotword_model(self, model_file):
        """ Loads a new hotword model file into the detector

        Args:
            model_file: Path to a .umdl file used for hotword detection

        Returns:
            None
        """

        self.__detector = snowboydecoder.HotwordDetector(model_file)

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

    def run(self):
        print("Listening for hotword...")

        self.__detector.start(self.on_hotword)

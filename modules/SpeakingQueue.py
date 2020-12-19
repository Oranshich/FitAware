from collections import deque
import threading
from queue import Queue
import pyttsx3


class SpeakingQueue:
    """
    The class responsible for all the talking the computer need to say, the class manage a queue of strings,
    the queue is managed by an external thread that every time a new text arrives,
    it reads the text in the order in the stack
    """
    def __init__(self):
        self.queue = Queue()
        self.engineio = pyttsx3.init()
        self.voices = self.engineio.getProperty('voices')
        self.engineio.setProperty('rate', 130)
        self.engineio.setProperty('voice', self.voices[0].id)
        self.run()

    def run(self):
        """
        Creating and starting the thread
        :return:
        """
        t = threading.Thread(target=self.worker)
        t.start()

    def worker(self):
        """
        Function is responsible for managing the queue, every time there is new text to read,
        the text is retrieved and sent for reading, the function starts processing when the thread is created
        :return:
        """
        while True:
            if self.queue.qsize() > 0:
                text = self.queue.get()
                self.speak(text)

    def speak(self, text):
        """
        The function that reads the text
        """
        self.engineio.say(text)
        self.engineio.runAndWait()

    def push(self, text):
        """
        The function push the text into the queue
        :param text: the text we ant to add to the queue
        """
        self.queue.put(text)
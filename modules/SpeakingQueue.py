import threading
from queue import Queue
import pyttsx3


class SpeakingQueue:
    def __init__(self):
        self.queue = Queue()
        self.engineio = pyttsx3.init()
        self.voices = self.engineio.getProperty('voices')
        self.engineio.setProperty('rate', 130)
        self.engineio.setProperty('voice', self.voices[0].id)
        self.t = threading.Thread(target=self.worker)
        self.is_running = False

    def run(self):
        self.t.start()
        self.is_running = True

    def worker(self):
        while True:
            if self.queue.qsize() > 0:
                text = self.queue.get()
                self.speak(text)

    def speak(self, text):

        self.engineio.say(text)
        self.engineio.runAndWait()

    def push(self, text):
        if not self.is_running:
            self.run()
        self.queue.put(text)

    def stop(self):
        if self.is_running:
            self.t.join()
            self.is_running = False

from collections import deque
import threading
from queue import Queue
import pyttsx3


class SpeakingQueue:
    def __init__(self):
        self.queue = Queue()
        self.engineio = pyttsx3.init()
        self.voices = self.engineio.getProperty('voices')
        self.engineio.setProperty('rate', 130)  # Aquí puedes seleccionar la velocidad de la voz
        self.engineio.setProperty('voice', self.voices[0].id)
        self.run()

    def run(self):
        t = threading.Thread(target=self.worker)
        t.start()

    def worker(self):
        while True:
            if self.queue.qsize() > 0:
                text = self.queue.get()
                self.speak(text)

    def speak(self, text):
        self.engineio.say(text)
        self.engineio.runAndWait()

    def push(self, text):
        self.queue.put(text)
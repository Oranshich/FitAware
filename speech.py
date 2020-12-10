# # Python program to translate
# # speech to text and text to speech
#
#
# import speech_recognition as sr
# import pyttsx3
#
# # Initialize the recognizer
# r = sr.Recognizer()
#
#
# # Function to convert text to
# # speech
# def SpeakText(command):
#     # Initialize the engine
#     engine = pyttsx3.init()
#     engine.say(command)
#     engine.runAndWait()
#
#
# # Loop infinitely for user to
# # speak
#
# while (1):
#
#     # Exception handling to handle
#     # exceptions at the runtime
#     try:
#
#         # use the microphone as source for input.
#         with sr.Microphone(device_index=1) as source2:
#
#             # wait for a second to let the recognizer
#             # adjust the energy threshold based on
#             # the surrounding noise level
#             r.adjust_for_ambient_noise(source2, duration=0.2)
#
#             # listens for the user's input
#             audio2 = r.listen(source2)
#
#             # Using ggogle to recognize audio
#             MyText = r.recognize_google(audio2)
#             MyText = MyText.lower()
#
#             print("Did you say " + MyText)
#             SpeakText(MyText)
#
#     except sr.RequestError as e:
#         print("Could not request results; {0}".format(e))
#
#     except sr.UnknownValueError:
#         print("unknown error occured")

import pyttsx3
# import engineio #engineio module is not needed.

engineio = pyttsx3.init()
voices = engineio.getProperty('voices')
engineio.setProperty('rate', 130)    # Aquí puedes seleccionar la velocidad de la voz
engineio.setProperty('voice',voices[0].id)

def speak(text):
    engineio.say(text)
    engineio.runAndWait()

speak("3")
speak("2 ")
speak("1 ")
speak("GO!")
while(1):
    phrase = input("--> ")
    if (phrase == "exit"):
        exit(0)
    speak(phrase)
    print(voices)
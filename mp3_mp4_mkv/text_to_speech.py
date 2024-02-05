"""
Text to speech
"""

import pyttsx3


TEXT = 'The quick brown fox jumps over the lazy dog'


def say(txt):
    voice = r'HKEY_LOCAL_MACHINE\SOFTWARE\Microsoft\Speech\Voices\Tokens\TTS_MS_EN-GB_HAZEL_11.0'
    engine = pyttsx3.init()
    engine.setProperty('voice', voice)
    engine.say(txt)
    engine.runAndWait()


if __name__ == '__main__':
    say(TEXT)

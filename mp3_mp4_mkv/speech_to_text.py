"""
Speech to text
"""

import speech_recognition as sr


LANGUAGE = 'en-US'


def get_speech():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        while True:
            r.adjust_for_ambient_noise(source)
            audio = r.listen(source)
            try:
                txt = r.recognize_google(audio, language=LANGUAGE)
                break
            except sr.UnknownValueError:
                pass
    return txt, audio


if __name__ == '__main__':
    print('Please start speaking')
    file_name = 'speech_to_text'
    with open(f'{file_name}.txt', 'a') as txt_file, open(f'{file_name}.wav', 'ab') as wav_file:
        while True:
            text, speech = get_speech()
            print(text)
            txt_file.write(text + '\n')  # appends to file
            wav_file.write(speech.get_wav_data())  # only saves first

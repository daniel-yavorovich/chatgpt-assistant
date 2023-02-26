import time
import wave

import pyaudio

import settings
from chat import OpenAIChat
import speech_recognition as sr
from google.cloud import texttospeech


class Assistant:
    def __init__(self):
        self.chat = OpenAIChat()
        self.recognizer = sr.Recognizer()
        self.t2s = texttospeech.TextToSpeechClient()

    def listen(self):
        with sr.Microphone() as source:
            print("Say something!")
            audio = self.recognizer.listen(source)

            try:
                text = self.recognizer.recognize_google(audio, language=settings.LANG)
                return text
            except:
                print("Sorry could not recognize what you said. Please say again.")
                time.sleep(1)

    def speak(self, text):
        synthesis_input = texttospeech.SynthesisInput(text=text)
        voice = texttospeech.VoiceSelectionParams(
            language_code=settings.LANG, ssml_gender=texttospeech.SsmlVoiceGender.FEMALE
        )
        audio_config = texttospeech.AudioConfig(
            audio_encoding=texttospeech.AudioEncoding.LINEAR16
        )
        response = self.t2s.synthesize_speech(
            input=synthesis_input, voice=voice, audio_config=audio_config
        )
        with open("/tmp/output.wave", "wb") as out:
            out.write(response.audio_content)

        wf = wave.open("/tmp/output.wave", 'rb')

        p = pyaudio.PyAudio()
        stream = p.open(format=p.get_format_from_width(wf.getsampwidth()),
                        channels=wf.getnchannels(),
                        rate=wf.getframerate(),
                        output=True)

        chunk = 1024
        data = wf.readframes(chunk)
        while data:
            # writing to the stream is what *actually* plays the sound.
            stream.write(data)
            data = wf.readframes(chunk)

        # cleanup stuff.
        wf.close()
        stream.close()
        p.terminate()

    def run(self):
        while True:
            text = None
            while not text:
                text = self.listen()

            self.chat.add_human_message(text)
            response = self.chat.chat()
            self.chat.add_ai_message(response)
            self.speak(response)


if __name__ == "__main__":
    assistant = Assistant()
    assistant.run()

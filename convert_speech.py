'''
pip install SpeechRecognition
pip install pydub
pip install pyAudio
'''

'''
Simple speech to text

import speech_recognition as sr
filename = r'c:\work\Test.wav'
r=sr.Recognizer()
with sr.AudioFile(filename) as source:
    audio_data = r.record(source)
    text = r.recognize_google(audio_data)
    print(text)
'''

import speech_recognition as sr
import os
from pydub import AudioSegment
from pydub.silence import split_on_silence

r=sr.Recognizer()

def transcribe_audio(path):
    text = ''
    with sr.AudioFile(path) as source:
        audio_listened = r.record(source)
        text = r.recognize_google(audio_listened)
    return text

def get_large_audio_transcription_on_silence(path):
    sound = AudioSegment.from_file(path)
    MIN_SILENCE_LEN_MS = 1000           # The min length considered to be a pause
    # SILENCE_THRESHOLD_DBFS = -40        # anything under -16 dBFS is considered to be silence
    SILENCE_THRESHOLD_DBFS = sound.dBFS-14
    KEEP_SILENCE_MS = 200               # keep this time of leading/trailing silence
    chunks = split_on_silence(sound,
                              min_silence_len = MIN_SILENCE_LEN_MS,
                              silence_thresh = SILENCE_THRESHOLD_DBFS,
                              keep_silence = KEEP_SILENCE_MS)
    folder_name = "audio-chunks"
    if not os.path.isdir(folder_name):
        os.mkdir(folder_name)
    whole_text = ''
    for i, audio_chunk in enumerate(chunks, start=1):
        chunk_filename = os.path.join(folder_name, f"chunk{i}.wav")
        audio_chunk.export(chunk_filename, format="wav")
        print(f"Audio chunk {chunk_filename} :")
        try:
            text=transcribe_audio(chunk_filename)
        except sr.UnknownValueError as e:
            print("Error :", str(e))
        else:
            text = f"{text.capitalize()}. "
            print(chunk_filename, ":", text)
            whole_text += text
    return whole_text

doConvert = False
# Do conversion if input is MP3
if doConvert:
    src = "audio.mp3"
    dst = "audio.wav"
    conv_sound = AudioSegment.from_mp3(src)
    conv_sound.export(dst, format="wav")
else:
    dst = r"c:\work\Test.wav"

input = dst
print(f"Using file [{dst}]")
print("\nFull text :", get_large_audio_transcription_on_silence(input))

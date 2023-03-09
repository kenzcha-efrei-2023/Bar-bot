# Ce fichier réuni toute les fonctions qui ont attrait au son (enregistrement, jouer, métronome)

import simpleaudio
import time
from mutagen.wave import WAVE
import pyaudio
import wave
import whisper
import speech_recognition as sr
from datetime import datetime

CHUNK = 1024
FORMAT = pyaudio.paInt16
CHANNELS = 1
RATE = 44100


def takeCommand(dur=3):
    """Takes microphone input from the user and returns string output"""
    print("Listening...")
    r = sr.Recognizer()

    with sr.Microphone() as source:
        # read the audio data from the default microphone
        audio_data = r.record(source, duration=dur)
        print("Recognizing...")
        # convert speech to text
        try:
            print("Reconnaissance du texte...")
            text = r.recognize_google(audio_data, language="fr-FR")
            print("text : " + text)
            return text
        except Exception as ex:
            print(ex)
            return ""

def whisper_listen():
    """Alternative : Listen to the microphone and return the transcription
    This is more precise but slower than takeCommand"""
    model = whisper.load_model("base") 

    seconds = 3
    filename = "output1.mp3" 

    p = pyaudio.PyAudio() # Create an interface to PortAudio

    print('Recording')

    stream = p.open(
        format=FORMAT,
        channels=CHANNELS,
        rate=RATE,
        frames_per_buffer=CHUNK,
        input=True
    )

    frames = [] # Initialize an array to store frames

    # Store data in chunks for 30 seconds
    for i in range(0, int(RATE / CHUNK * seconds)):
        data = stream.read(CHUNK)
        frames.append(data)

    stream.stop_stream()
    stream.close()
    p.terminate()

    # Save the recorded data as a WAV file
    wf = wave.open(filename, 'wb')
    wf.setnchannels(CHANNELS)
    wf.setsampwidth(p.get_sample_size(FORMAT))
    wf.setframerate(RATE)
    wf.writeframes(b''.join(frames))
    wf.close()

    return model.transcribe(filename,fp16=False)["text"]  # Return the transcription


def record():
    t1 = datetime.now()
    """Records from the microphone for a non specified time and returns the resulting data"""
    p = pyaudio.PyAudio()

    stream = p.open(format=FORMAT,
                    channels=CHANNELS,
                    rate=RATE,
                    input=True,
                    frames_per_buffer=CHUNK)

    print("Start recording")

    frames = []

    try:
        while True:
            
            data = stream.read(CHUNK)
            frames.append(data)
            t2 = datetime.now()
            delta = t2 - t1
            if(delta.total_seconds()>=30):
                break
    except KeyboardInterrupt:
        print("Done recording")
    except Exception as e:
        print(str(e))

    sample_width = p.get_sample_size(FORMAT)

    stream.stop_stream()
    stream.close()
    p.terminate()

    return sample_width, frames


def record_to_file(file_path):
    """Records from the microphone and outputs the resulting data to 'file_path"""
    wf = wave.open(file_path, 'wb')
    wf.setnchannels(CHANNELS)
    sample_width, frames = record()
    wf.setsampwidth(sample_width)
    wf.setframerate(RATE)
    wf.writeframes(b''.join(frames))
    wf.close()


def play(file="data/audio/Psychomecka.wav"):
    """play a wave file"""
    audio = WAVE(file)

    audio_length = int(audio.info.length)
    song = simpleaudio.WaveObject.from_wave_file(file)

    while True:
        song.play()
        time.sleep(audio_length)


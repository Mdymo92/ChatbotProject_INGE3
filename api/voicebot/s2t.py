#!/usr/bin/env python3

import subprocess
import sys

from vosk import Model, KaldiRecognizer, SetLogLevel

SAMPLE_RATE = 16000

SetLogLevel(0)

model = Model(lang="en-us")
rec = KaldiRecognizer(model, SAMPLE_RATE)

""" with subprocess.Popen(["ffmpeg", "-loglevel", "quiet", "-i",
                            sys.argv[1],
                            "-ar", str(SAMPLE_RATE) , "-ac", "1", "-f", "s16le", "-"],
                            stdout=subprocess.PIPE) as process:

    while True:
        if process.stdout is not None:
            data = process.stdout.read(4000)
            if len(data) == 0:
                break
            if rec.AcceptWaveform(data):
                print(rec.Result())
            else:
                print(rec.PartialResult())

    print(rec.FinalResult()) """


def convert_file_to_wav(filename):
    subprocess.run(["ffmpeg", "-i", filename, "-ar", "16000", "processed_file.wav"])

def process_voice(filename):
    with open(filename, "rb") as f:
        data = f.read()
        if rec.AcceptWaveform(data):
            print(rec.Result())
        else:
            print("Incorrect waveform")
            convert_file_to_wav(filename)
            print("Converted to wav")
            with open("processed_file.wav", "rb") as f:
                data = f.read()
                if rec.AcceptWaveform(data):
                    print(rec.Result())
                else:
                    print(rec.PartialResult())

    print(rec.FinalResult())
    
    
#process_voice("bot_answer.mp3")
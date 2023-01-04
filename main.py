import os
import wave

import pyaudio

# File Management
PROMPTS_FILE = "prompts2.txt"
RECORDINGS_FOLDER = "data"
TRANSCRIPT_FILE = f"{RECORDINGS_FOLDER}/transcript.txt"

# Recording config
CHUNK = 1024
FORMAT = pyaudio.paInt16
CHANNELS = 1
RATE = 44100
RECORD_SECONDS = 5

p = pyaudio.PyAudio()

counter = 0
transcript = ""


class bcolors:
    HEADER = "\033[95m"
    OKBLUE = "\033[94m"
    OKCYAN = "\033[96m"
    OKGREEN = "\033[92m"
    WARNING = "\033[93m"
    FAIL = "\033[91m"
    ENDC = "\033[0m"
    BOLD = "\033[1m"
    UNDERLINE = "\033[4m"


if not os.path.exists(RECORDINGS_FOLDER):
    os.makedirs(RECORDINGS_FOLDER)

with open(PROMPTS_FILE, "r") as f:
    for line in f:
        while True:
            print(
                f'\nPlease read aloud: {bcolors.OKGREEN}"{line.strip()}"{bcolors.ENDC}\n'
            )

            stream = p.open(
                format=FORMAT,
                channels=CHANNELS,
                rate=RATE,
                input=True,
                frames_per_buffer=CHUNK,
                input_device_index=0,
            )
            print(f"{bcolors.FAIL}Recording...{bcolors.ENDC}")
            frames = []

            for i in range(0, int(RATE / CHUNK * RECORD_SECONDS)):
                data = stream.read(CHUNK)
                frames.append(data)

            print(
                f"{bcolors.WARNING}Recording Complete. Press W to save or any-key to retry{bcolors.ENDC}"
            )
            stream.stop_stream()
            stream.close()

            key = input().lower()
            if key == "w":
                wf = wave.open(f"{RECORDINGS_FOLDER}/{counter}_output.wav", "wb")
                wf.setnchannels(CHANNELS)
                wf.setsampwidth(p.get_sample_size(FORMAT))
                wf.setframerate(RATE)
                wf.writeframes(b"".join(frames))
                wf.close()
                transcript += f"{counter}_output.wav\t{line}\n"
                counter += 1
                break
            else:
                print(f"{bcolors.OKCYAN}Rerecording phrase{bcolors.ENDC}")
                print("")
                continue

with open(TRANSCRIPT_FILE, "w") as f:
    f.write(transcript)

p.terminate()

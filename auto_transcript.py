"""
How to use:
1. Open CMD
2. VENV USED so enter "conda activate pyannote"
3. change to this directory
4. type: "python auto_transcript.py"
5. Fill 2 inputs, path to audio and num of speakers.

The program:
- takes an audio file as an input
- Uses pyannote.audio to identify speakers and speech times
- Splits the audio file between each start and end speech time
- uses OpenAI's whisper module to convert speech to text
    - Create an object for each start time, end time, speech, speaker to format later
- Format the generated data into a PDF file (or file to edit like text) which is your transcript"""
import openai
from pyannote.audio import Pipeline
from pydub import AudioSegment
from time import strftime
from time import gmtime
import time
import os

openai.api_key = os.environ["OPENAI_TOKEN"]
hugging_face_api_key = os.environ["HUGGINGFACE_TOKEN"]

PATH_TO_AUDIO = input("Path to audio file (include the .wav extension): \n")
NUMBER_OF_SPEAKERS = input("Number of speakers (if unknown, hit ENTER): ")

# Access token for model from Hugging Face - https://huggingface.co/pyannote/speaker-diarization
pipeline = Pipeline.from_pretrained("pyannote/speaker-diarization",
                                    use_auth_token=hugging_face_api_key)

if NUMBER_OF_SPEAKERS != "":
    diarization = pipeline(PATH_TO_AUDIO, num_speakers=int(NUMBER_OF_SPEAKERS))
elif NUMBER_OF_SPEAKERS == "":
    diarization = pipeline(PATH_TO_AUDIO)

total_audio_metadata = []
total_audio = []

# Assort data into objects by creating an array of dictionaries. Detects speakers and timestamps.
for turn, _, speaker in diarization.itertracks(yield_label=True):
    temp_dict = {"start time": 0,
                 "end time": 0,
                 "speaker": "NA"}
    temp_dict["start time"] = turn.start
    temp_dict["end time"] = turn.end
    temp_dict["speaker"] = speaker
    total_audio_metadata.append(temp_dict)

# Split original WAV file into several based on start and end times.
for i in range(len(total_audio_metadata)):

    # Convert times to milliseconds
    start = total_audio_metadata[i]["start time"] * 1000
    end = total_audio_metadata[i]["end time"] * 1000
    newAudio = AudioSegment.from_wav(PATH_TO_AUDIO)
    newAudio = newAudio[start:end]

    name_of_split = f'build/part_{i+1}.wav'
    newAudio.export(name_of_split, format="wav") #Exports to a wav file in the current path.

    # Records names of all split files to transcript later.
    total_audio.append(name_of_split)

print(total_audio_metadata)
# Clears the contents of the transcript file before writing to it
open('transcript.txt', 'w').close()
transcript_file = open('transcript.txt', 'a')

preminute = time.time()
# Use OpenAIs whisper model to convert each WAV file into text and output it.
for i in range(len(total_audio)):

    
    split_audio_path = total_audio[i]
    audio_to_convert = open(split_audio_path, "rb")
    transcript = openai.Audio.transcribe("whisper-1", audio_to_convert)
    audio_to_convert.close()

    # Put in format:
    # [HH:MM:SS] SPEAKER    TEXT...
    line = f"[{strftime('%H:%M:%S', gmtime(int(total_audio_metadata[i]['start time'])))}] {total_audio_metadata[i]['speaker']}\t\t{transcript['text']}\n\n"

    # Output the text to a textfile
    transcript_file.write(line)

    # OpenAI allows 3 requests per minute
    if i % 3 == 2:
        now = time.time()

        if (now - preminute) > 60:
            preminute = time.time()
        elif (now - preminute) <= 60:
            time.sleep(61 - (now - preminute))
            preminute = time.time()

transcript_file.close()
    

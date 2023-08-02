# AI-Transcription
Purpose: Transcribes audio files. It performs speaker diarisation, and produces timestamps each time a new speaker speaks. The output is a formatted text file with the transcription of the audio.

## How to use
1. Create a virtual environment with Python 3.8.17
2. Create an account on OpenAI's website and create an API Token.
3. Enter into the command prompt
4. Follow these instructions to install Pyannote: https://github.com/pyannote/pyannote-audio
5. Replace the values in lines 24 and 25 with your OpenAI token and Hugging Face token, respectively.
6. Run auto_transcript.py and follow the instructions in the terminal. Expect to wait a couple minutes for the test file.
7. The program should have successfully finished when transcript.txt has the formatted transcript.

Note that the program may take an unrealistic amount of time to transcribe audio files that are over several minutes long.

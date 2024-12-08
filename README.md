A simple audio-to-text converter using Vosk.

## Setup 
1. Install [uv](https://docs.astral.sh/uv/getting-started/installation/) if necessary
2. Install project dependencies with ```uv install```
3. Download one of the [Vosk models](https://alphacephei.com/vosk/models) and unzip into the project directory  
[128MB vosk-model-en-us-0.22-lgraph](https://alphacephei.com/vosk/models/vosk-model-en-us-0.22-lgraph.zip)  
[1.8G vosk-model-en-us-0.22](https://alphacephei.com/vosk/models/vosk-model-en-us-0.22.zip)  
  
## Run the script
1. Put the audio file to convert in the `/input` folder.
2. Run the script with ```uv run audio_to_text.py```.
3. The `/output` folder will contain text files.
4. The `/processed` folder will contain processed audio files.  


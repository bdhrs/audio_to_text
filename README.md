## Install dependencies
```shell
uv insta

## Download Vosk
1. Download one of the models from https://alphacephei.com/vosk/models
    [128MB](https://alphacephei.com/vosk/models/vosk-model-en-us-0.22-lgraph.zip) 
    [1.8G](https://alphacephei.com/vosk/models/vosk-model-en-us-0.22.zip)
2. Unzip 
3. Put into the project directory    

ll
```

## Audio to text converter
1. Put the audio file to convert in the `/input` folder
2. Run the script 
```shell
uv run audio_to_text.py
```
3. `/output` folder contains text files
4. `/processed` folder contains processed audio  


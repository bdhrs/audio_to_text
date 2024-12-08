
import json
import subprocess
import wave

from pathlib import Path
from vosk import Model, KaldiRecognizer
from rich import print


input_folder = Path("input")
output_folder = Path("output")
processed_folder = Path("processed")
model1_path = "vosk-model-en-us-0.22-lgraph"
model2_path = "vosk-model-en-us-0.22"

if Path(model2_path).exists():
    model_path = model2_path
else:
    model_path = model1_path


def convert_to_mono_wav(input_path: Path, wav_path: Path):
    """Vosk needs mono .wav files to process.""" 

    print(f"\n[yellow]Converting '{input_path}' to wav\n")

    command = [
        "ffmpeg",
        "-y",                     # Overwrite output files without prompting
        "-i", input_path,
        "-af", "pan=mono|c0=FL",  # Use the left channel (Front Left)
        "-ar", "16000",           # Set sample rate to 16 kHz
        wav_path
    ]
    
    # Execute the command using subprocess
    try:
        subprocess.run(command, check=True)
        print(f"Converted: {input_path} -> {wav_path}")
    except subprocess.CalledProcessError as e:
        print(f"Error converting {input_path}: {e}")


def convert_wav_to_text(input_path:Path, wav_path: Path):

    print(f"\n[yellow]Converting '{input_path}' to text\n")

    model = Model(model_path)

    with wave.open(str(wav_path), "rb") as wf:
        if wf.getnchannels() != 1 or wf.getsampwidth() != 2 or wf.getframerate() not in [8000, 16000]:
            raise ValueError(f"Audio file {wav_path} must be mono PCM WAV with 8kHz or 16kHz sample rate.")
        
        recognizer = KaldiRecognizer(model, wf.getframerate())
        results = []
        while True:
            data = wf.readframes(4000)  # Read audio in chunks
            if len(data) == 0:
                break
            if recognizer.AcceptWaveform(data):
                result = json.loads(recognizer.Result())
                results.append(result.get("text", ""))

        final_result = json.loads(recognizer.FinalResult())
        results.append(final_result.get("text", ""))

    transcription = " ".join(results)

    # Save transcription to a text file
    output_file = output_folder / f"{input_path.stem}.txt"
    with open(output_file, "w") as f:
        f.write(transcription)

    print(f"Processed: {wav_path} -> {output_file}")

    # Remove the input .wav file after processing
    wav_path.unlink()


def main():
    
    # make the input and output folders if they don't exist
    Path(input_folder).mkdir(parents=True, exist_ok=True)
    Path(output_folder).mkdir(parents=True, exist_ok=True)
    Path(processed_folder).mkdir(parents=True, exist_ok=True)
    

    for input_path in Path(input_folder).iterdir():
        if input_path.suffix in {".wav", ".mp3", ".mp4", ".m4a"}:

            # convert the input file to mono wav
            wav_path = input_path \
                .with_name(f"{input_path.stem}_processing") \
                .with_suffix(".wav")

            convert_to_mono_wav(input_path, wav_path)

            # convert the wav to text
            convert_wav_to_text(input_path, wav_path)

            # move the original file to processed folder
            input_path.rename(Path(processed_folder) / input_path.name)


if __name__ == "__main__":
    main()

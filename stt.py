from faster_whisper import WhisperModel
import logging
import os
import torch
from config import model_name, dvce, SEG_PATH,CSV
import torchaudio
from torchaudio.transforms import Resample
from pydub import AudioSegment
import pandas as pd


logging.basicConfig(level=logging.INFO)

model = WhisperModel(model_name, device = "cpu",compute_type="int8")
mod, utils = torch.hub.load('snakers4/silero-vad','silero_vad',force_reload=True)
(get_speech_timestamps, _, read_audio, _, _) = utils
results = []

def is_speech(audio, sr = 16000, threshold = 0.1):
    '''Check for Voice activity in the audio'''
    wav = read_audio(audio, sampling_rate=sr)

    speech_timestamps = get_speech_timestamps(wav, mod, sampling_rate=sr)

    return len(speech_timestamps) > 0

def transcribe(audio_dir, output_csv):
    '''Transcribes the audio and saves in a csv'''
    
    if not os.path.exists(audio_dir):
        logging.error("Directory does not exist")
        return
    
    audio_files = []
    for root, _, files in os.walk(audio_dir):
        for f in files:
            if f.endswith('.wav'):
                audio_files.append(os.path.join(root, f))
    if not audio_files:
        logging.error("No audio files found")
        return
    
    logging.info(f"Found {len(audio_files)} audio files")

    for audio_f in audio_files:
        try:
            if not is_speech(audio_f):
                logging.info(f"Skipping {audio_f} as it is not speech")
                continue
            segments, _ = model.transcribe(audio_f)
            for seg in segments:
                results.append({
                    "file" : audio_f,
                    "start" : seg.start,
                    "end" : seg.end,
                    "transcription" : seg.text
                })
                
            logging.info(f"Transcribed {audio_f}")
            
        except Exception as e:
            logging.error(f"Failed to transcribe {audio_f} : {str(e)}")
            

        df = pd.DataFrame(results)
        df.to_csv(CSV, index = False)
        logging.info(f"Transcription saved to {output_csv}")
        print(results)

transcribe(SEG_PATH, CSV)



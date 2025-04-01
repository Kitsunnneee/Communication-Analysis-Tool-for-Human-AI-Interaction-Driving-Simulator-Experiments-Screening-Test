from faster_whisper import WhisperModel
import logging
import os
import torch
from config import model_name,split_length
import pandas as pd
from sentiment import get_sentiment
import re


logging.basicConfig(level=logging.INFO)

model = WhisperModel(model_name, device = "cpu",compute_type="int8")
mod, utils = torch.hub.load('snakers4/silero-vad','silero_vad',force_reload=True)
(get_speech_timestamps, _, read_audio, _, _) = utils
results = []

def is_speech(audio, sr = 16000, threshold = 0.1):
    '''Function that check for Voice activity in the audio'''
    wav = read_audio(audio, sampling_rate=sr)

    speech_timestamps = get_speech_timestamps(wav, mod, sampling_rate=sr)

    return len(speech_timestamps) > 0

def file_sorting(file_path):
    '''Function that sorts the files based on the number in the file name'''
    base_name = os.path.basename(file_path)
    match = re.match(r"(.*)_(\d+)\.wav", base_name)
    if match:
        original_name = match.group(1)
        segment_no = int(match.group(2))
        return (original_name, segment_no)   
    
    return (base_name, float('inf')) 

def transcribe(audio_dir, output_dir):
    '''Function that transcribes the audio and saves it to a CSV file with sentiment analysis'''
    
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
    audio_files.sort(key=file_sorting)

    results = []  
    skipped_duration = 0 

    for audio_f in audio_files:
        try:
            if not is_speech(audio_f):
                logging.info(f"Skipping {audio_f} as it is not speech")
                skipped_duration += split_length / 1000
                continue
            
            _, seg_idx = file_sorting(audio_f)
            absolute_start = seg_idx * (split_length / 1000) 
            
            segments, _ = model.transcribe(audio_f)
            segments = list(segments)
            
            actual_start = absolute_start + segments[0].start + 1
            
            results.append({
                    "file": os.path.basename(audio_f),
                    "start": actual_start,
                    "transcription": segments[0].text
                })
            
            logging.info(f"Transcribed {audio_f}")
            
        except Exception as e:
            logging.error(f"Failed to transcribe {audio_f} : {str(e)}")
    
    audio_base_name = os.path.splitext(os.path.basename(audio_f))[0]
    output_csv = os.path.join(output_dir, f"{audio_base_name}.csv")
    os.makedirs(os.path.dirname(output_csv), exist_ok=True)

    df = pd.DataFrame(results)
    df.to_csv(output_csv, index=False)

    get_sentiment(output_csv, output_csv)

    logging.info(f"Transcription and sentiment saved to {output_csv}")

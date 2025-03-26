from utils import video_to_audio, split_audio
from stt import transcribe
from sentiment import get_sentiment

from config import CSV, VIDEO_PATH, AUDIO_PATH, SEG_PATH, model_name
import logging
import pandas as pd

logging.basicConfig(level=logging.INFO)

print("STEP 1 : Extracting audio from video")
video_to_audio(VIDEO_PATH, AUDIO_PATH)

print("STEP 2 : Splitting audio into segments")
split_audio(AUDIO_PATH, SEG_PATH)

print("STEP 3 : Transcribing audio")
transcribe(SEG_PATH, CSV)

print("STEP 4 : Performing sentiment analysis")
data = pd.read_csv(CSV)
get_sentiment(data)
data.to_csv(CSV, index=False)

print("STEP 5 : Sentiment analysis completed and saved to CSV.")
print("Pipeline completed successfully")

from utils import video_to_audio, split_audio
from stt import transcribe
import logging
from config import VIDEO_PATH, AUDIO_PATH, SEG_PATH, TRANSCRIBE_DIR

logging.basicConfig(level=logging.INFO)

logging.info("STEP 1: Extracting audio from video")
video_to_audio(VIDEO_PATH, AUDIO_PATH)

logging.info("STEP 2: Splitting audio into segments")
split_audio(AUDIO_PATH, SEG_PATH)

logging.info("STEP 3: Transcribing audio and performing sentiment analysis")
transcribe(SEG_PATH, TRANSCRIBE_DIR)

logging.info("Pipeline completed successfully.")

# test_pipeline.py

import unittest
import os
import shutil
import pandas as pd
import matplotlib
import warnings
warnings.filterwarnings("ignore")
matplotlib.use('Agg')

# Import the modules
from utils import read_directory, extract_audio, split_audio
from stt import transcribe, is_speech
from sentiment import get_sentiment
from visualization import generate_time_bucket_histogram, generate_sentiment_visualization
from ui import CommunicationAnalysisApp
import tkinter as tk

# Declare the paths
VIDEO_FILE_PATH = "/Users/rahul/Desktop/HumainAI/Videos/Experimenter_CREW_999_1_All_1731617801.mp4"
AUDIO_PATH = "temp/valid.wav"
SEGMENT_DIR = "temp/segments"
TRANSCRIBE_CSV = "temp/valid.csv"
SENTIMENT_CSV = "temp/valid_sentiment.csv"

def setUpModule():
    os.makedirs("temp", exist_ok=True)

    # 1. Extract audio from video
    print("[Setup] Extracting audio...")
    extract_audio(VIDEO_FILE_PATH, AUDIO_PATH)
    
    # 2. Segment audio
    print("[Setup] Splitting audio...")
    split_audio("temp", SEGMENT_DIR)

    # 3. Transcribe audio segments
    print("[Setup] Transcribing segments...")
    transcribe("temp", "temp")  # writes to TRANSCRIBE_CSV

    # 4. Perform sentiment analysis
    print("[Setup] Performing sentiment analysis...")
    get_sentiment(TRANSCRIBE_CSV, SENTIMENT_CSV)


def tearDownModule():
    print("[Cleanup] Removing temp files...")
    shutil.rmtree("temp", ignore_errors=True)


class TestUtils(unittest.TestCase):
    def test_read_directory(self):
        videos = read_directory(os.path.dirname(VIDEO_FILE_PATH))
        self.assertGreater(len(videos), 0)

    def test_audio_file_created(self):
        self.assertTrue(os.path.exists(AUDIO_PATH))
        self.assertGreater(os.path.getsize(AUDIO_PATH), 0)

    def test_segment_created(self):
        segments = os.listdir(os.path.join(SEGMENT_DIR, "valid"))
        self.assertGreater(len(segments), 0)


class TestSTT(unittest.TestCase):
    def test_is_speech(self):
        result = is_speech(AUDIO_PATH)
        self.assertIsInstance(result, bool)

    def test_transcription_file(self):
        self.assertTrue(os.path.exists(TRANSCRIBE_CSV))
        df = pd.read_csv(TRANSCRIBE_CSV)
        self.assertIn("transcription", df.columns)


class TestSentiment(unittest.TestCase):
    def test_sentiment_file_created(self):
        self.assertTrue(os.path.exists(SENTIMENT_CSV))
        df = pd.read_csv(SENTIMENT_CSV)
        self.assertIn("sentiment", df.columns)


class TestVisualization(unittest.TestCase):
    def test_histogram_plot(self):
        plot = generate_time_bucket_histogram(SENTIMENT_CSV)
        self.assertIsNotNone(plot)

    def test_sentiment_plot(self):
        plot = generate_sentiment_visualization(SENTIMENT_CSV)
        self.assertIsNotNone(plot)


class TestUI(unittest.TestCase):
    def setUp(self):
        self.root = tk.Tk()
        self.app = CommunicationAnalysisApp(self.root)

    def tearDown(self):
        self.root.destroy()
        if os.path.exists("analysis_log.txt"):
            os.remove("analysis_log.txt")

    def test_ui_initialization(self):
        self.assertIsNotNone(self.app.file_entry)
        self.assertIsNotNone(self.app.plot_frame)

    def test_upload_file(self):
        self.app.file_path.set(SENTIMENT_CSV)
        self.assertEqual(self.app.file_path.get(), SENTIMENT_CSV)


if __name__ == "__main__":
    unittest.main()

import unittest
import os
import requests
import shutil
from pydub import AudioSegment
from utils import read_directory, extract_audio, split_audio

import warnings
warnings.filterwarnings("ignore")

class TestUtils(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        # Create test directories
        cls.test_video_dir = "test_videos"
        cls.test_audio_dir = "test_audios"
        cls.test_seg_dir = "test_segments"
        
        os.makedirs(cls.test_video_dir, exist_ok=True)
        os.makedirs(cls.test_audio_dir, exist_ok=True)
        os.makedirs(cls.test_seg_dir, exist_ok=True)

        # Download a sample video
        cls.download_sample_video()

    @classmethod
    def download_sample_video(cls):
        """
        Download a sample video for testing
        Using a small, publicly accessible video file
        """
        sample_video_urls = [
            "https://commondatastorage.googleapis.com/gtv-videos-bucket/sample/BigBuckBunny.mp4"
            ]

        cls.valid_video_path = os.path.join(cls.test_video_dir, "sample_video.mp4")
        
        for url in sample_video_urls:
            try:
                response = requests.get(url, stream=True)
                response.raise_for_status() 

                with open(cls.valid_video_path, 'wb') as out_file:
                    shutil.copyfileobj(response.raw, out_file)

                if os.path.getsize(cls.valid_video_path) > 0:
                    print(f"Successfully downloaded video from {url}")
                    break
            except Exception as e:
                print(f"Failed to download from {url}: {e}")
                continue
        else:
            cls.create_dummy_video()

    @classmethod
    def create_dummy_video(cls):
        """
        Create a dummy video file if download fails
        """
        cls.valid_video_path = os.path.join(cls.test_video_dir, "valid.mp4")
        with open(cls.valid_video_path, "wb") as f:
            f.write(b"\x00\x00\x00\x20ftypmp42\x00\x00\x00\x00mp42isom")

    def setUp(self):
        self.valid_audio_path = os.path.join(self.test_audio_dir, "valid.wav")
        
        silent_audio = AudioSegment.silent(duration=5000)  
        silent_audio.export(self.valid_audio_path, format="wav")

    def tearDown(self):
        if os.path.exists(self.valid_audio_path):
            os.remove(self.valid_audio_path)

    @classmethod
    def tearDownClass(cls):
        for path in [cls.test_video_dir, cls.test_audio_dir, cls.test_seg_dir]:
            if os.path.exists(path):
                shutil.rmtree(path)

    def test_read_directory(self):
        videos = read_directory(self.test_video_dir)
        self.assertGreater(len(videos), 0, "No videos found in test directory")

    def test_extract_audio(self):
        extract_audio(self.valid_video_path, self.valid_audio_path)
        self.assertTrue(os.path.exists(self.valid_audio_path))
        self.assertGreater(os.path.getsize(self.valid_audio_path), 0)

    def test_split_audio(self):
        split_audio(self.test_audio_dir, self.test_seg_dir)
        
        audio_filename = os.path.basename(self.valid_audio_path)
        base_name = os.path.splitext(audio_filename)[0]
        
        segment_dir = os.path.join(self.test_seg_dir, base_name)
        segments = os.listdir(segment_dir)
        self.assertGreater(len(segments), 0, "No audio segments created")

if __name__ == "__main__":
    unittest.main()
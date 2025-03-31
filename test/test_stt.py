import unittest
import os
from stt import transcribe, is_speech
from pydub import AudioSegment

import warnings
warnings.filterwarnings("ignore")

class TestSTT(unittest.TestCase):
    def setUp(self):
        self.test_audio_dir = "test_audios"
        self.test_output_dir = "test_output"
        
        os.makedirs(self.test_audio_dir, exist_ok=True)
        os.makedirs(self.test_output_dir, exist_ok=True)

        self.valid_audio_path = os.path.join(self.test_audio_dir, "valid.wav")
        with open(self.valid_audio_path, "wb") as f:
            AudioSegment.silent(duration=1000).export(f, format="wav")

    def tearDown(self):
        for path in [self.test_audio_dir, self.test_output_dir]:
            if os.path.exists(path):
                for root, _, files in os.walk(path):
                    for f in files:
                        os.remove(os.path.join(root, f))
                os.rmdir(path)

    def test_is_speech(self):
        result = is_speech(self.valid_audio_path)
        self.assertIsInstance(result, bool)

    def test_transcribe(self):
        transcribe(self.test_audio_dir, self.test_output_dir)

        self.assertTrue(os.path.exists(self.test_output_dir))

if __name__ == "__main__":
    unittest.main()
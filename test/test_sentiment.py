import unittest
import pandas as pd
from sentiment import get_sentiment
import os

import warnings
warnings.filterwarnings("ignore")

class TestSentiment(unittest.TestCase):

    def setUp(self):
        self.input_csv = "test_input.csv"
        self.output_csv = "test_output.csv"

        data = {
            "transcription": ["I love this!", "This is okay.", "I hate this!"]
        }
        df = pd.DataFrame(data)
        df.to_csv(self.input_csv, index=False)

    def tearDown(self):
        for file in [self.input_csv, self.output_csv]:
            if os.path.exists(file):
                os.remove(file)

    def test_get_sentiment(self):
        get_sentiment(self.input_csv, self.output_csv)
        
        self.assertTrue(os.path.exists(self.output_csv))
        
        with open(self.output_csv, 'r') as f:
            content = f.read()
            self.assertGreater(len(content), 0)
        
        output_data = pd.read_csv(self.output_csv)
        self.assertIn("sentiment", output_data.columns)

if __name__ == "__main__":
    unittest.main()
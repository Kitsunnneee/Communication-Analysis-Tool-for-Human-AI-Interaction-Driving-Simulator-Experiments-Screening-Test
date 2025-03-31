import unittest
import pandas as pd
from visualization import generate_time_bucket_histogram, generate_sentiment_visualization
import os
import matplotlib

import warnings
warnings.filterwarnings("ignore")

matplotlib.use('Agg') 

class TestVisualization(unittest.TestCase):

    def setUp(self):
        self.dummy_csv_path = "dummy.csv"
        
        data = {
            "start": [0.0, 5.0, 10.0], 
            "transcription": ["Hello world", "Testing visualization", "Another test"],
            "sentiment": ["positive", "neutral", "negative"]
        }
        df = pd.DataFrame(data)
        df.to_csv(self.dummy_csv_path, index=False)

    def tearDown(self):
        if os.path.exists(self.dummy_csv_path):
            os.remove(self.dummy_csv_path)

    def test_generate_time_bucket_histogram(self):
        plot = generate_time_bucket_histogram(self.dummy_csv_path)
        self.assertIsNotNone(plot)

    def test_generate_sentiment_visualization(self):
        plot = generate_sentiment_visualization(self.dummy_csv_path)
        self.assertIsNotNone(plot)

if __name__ == "__main__":
    unittest.main()
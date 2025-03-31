import unittest
import os
import tkinter as tk
from ui import CommunicationAnalysisApp

import warnings
warnings.filterwarnings("ignore")

class TestUI(unittest.TestCase):

    def setUp(self):
        self.root = tk.Tk()
        if os.path.exists("analysis_log.txt"):
            os.remove("analysis_log.txt")
            
        self.app = CommunicationAnalysisApp(self.root)

    def tearDown(self):
        self.root.destroy()
        if os.path.exists("analysis_log.txt"):
            os.remove("analysis_log.txt")

    def test_ui_initialization(self):
        self.assertIsNotNone(self.app.file_entry)
        self.assertIsNotNone(self.app.plot_frame)

    def test_upload_file_functionality(self):
        test_file_path = "dummy.csv"
        
        self.app.file_path.set(test_file_path)
        self.assertEqual(self.app.file_path.get(), test_file_path)
        
if __name__ == "__main__":
    unittest.main()
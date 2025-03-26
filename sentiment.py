from pysentimiento import create_analyzer
import transformers
from config import CSV
import pandas as pd
import os

transformers.logging.set_verbosity(transformers.logging.ERROR)

analyzer = create_analyzer(task="sentiment", lang="en")

print(analyzer.predict("I am devastaed by the news!"))


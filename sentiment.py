from pysentimiento import create_analyzer
import transformers
from config import CSV

transformers.logging.set_verbosity(transformers.logging.ERROR)

analyzer = create_analyzer(task="sentiment", lang="en")


def get_sentiment(data):
    if "sentiment" not in data.columns:
        data["sentiment"] = ""
    for i in range(len(data)):
        row = data.iloc[i]
        text = row["transcription"]
        sentiment = analyzer.predict(text)
        data.at[i, "sentiment"] = sentiment.output
        
    data.to_csv(CSV, index=False)

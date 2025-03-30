from pysentimiento import create_analyzer
import transformers
import pandas as pd

transformers.logging.set_verbosity(transformers.logging.ERROR)

analyzer = create_analyzer(task="sentiment", lang="en")


def get_sentiment(input_csv, output_csv):
    '''Function that predicts sentiment for a transcription file'''
    try:
        data = pd.read_csv(input_csv)
        if "sentiment" not in data.columns:
            data["sentiment"] = ""

        for i in range(len(data)):
            row = data.iloc[i]
            text = row["transcription"]
            sentiment = analyzer.predict(text)
            data.at[i, "sentiment"] = sentiment.output

        data.to_csv(output_csv, index=False)
        print(f"Sentiment analysis saved to {output_csv}")

    except Exception as e:
        print(f"Error processing {input_csv}: {str(e)}")

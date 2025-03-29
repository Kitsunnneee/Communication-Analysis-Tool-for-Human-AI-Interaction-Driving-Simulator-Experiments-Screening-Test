import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import os

def generate_time_bucket_histogram(csv_path, bucket_size=5):
    df = pd.read_csv(csv_path)
    
    if 'start' not in df.columns:
        print("Warning: 'start' column not found. Using index as proxy.")
        df['start'] = df.index * bucket_size
    
    if 'transcription' not in df.columns:
        print("Error: 'transcription' column not found in CSV.")
        return None
    
    max_time = df['start'].max()
    
    buckets = np.arange(0, max_time + bucket_size, bucket_size)
    bucket_labels = [
        f"{int(start//60):02d}:{int(start%60):02d}-{int((start+bucket_size)//60):02d}:{int((start+bucket_size)%60):02d}"
        for start in buckets[:-1]
    ]
    
    bucket_counts = []
    for i in range(len(buckets) - 1):
        bucket_mask = (df['start'] >= buckets[i]) & (df['start'] < buckets[i+1])
        words_in_bucket = df[bucket_mask]['transcription'].str.split().str.len().sum()
        bucket_counts.append(words_in_bucket)
    
    plt.figure(figsize=(12, 6))
    plt.bar(bucket_labels, bucket_counts)
    plt.title('Words per Time Bucket')
    plt.xlabel('Time Buckets')
    plt.ylabel('Number of Words')
    plt.xticks(rotation=45, ha='right')
    plt.tight_layout()
    
    return plt

def generate_sentiment_visualization(csv_path):

    df = pd.read_csv(csv_path)
    
    if 'sentiment' not in df.columns:
        print("Warning: No sentiment data found!")
        return None
    
    sentiment_counts = df['sentiment'].value_counts()
    
    plt.figure(figsize=(10, 7))
    plt.pie(sentiment_counts, labels=sentiment_counts.index, autopct='%1.1f%%')
    plt.title('Sentiment Distribution')
    
    return plt

def save_plots(csv_path, output_dir='./plots'):

    os.makedirs(output_dir, exist_ok=True)
    
    try:
        histogram_plot = generate_time_bucket_histogram(csv_path)
        histogram_plot.savefig(os.path.join(output_dir, 'transcription_histogram.png'))
        histogram_plot.close()
    except Exception as e:
        print(f"Error generating histogram: {e}")
    
    try:
        sentiment_plot = generate_sentiment_visualization(csv_path)
        if sentiment_plot:
            sentiment_plot.savefig(os.path.join(output_dir, 'sentiment_distribution.png'))
            sentiment_plot.close()
    except Exception as e:
        print(f"Error generating sentiment plot: {e}")

if __name__ == "__main__":
    from config import CSV  # Assuming your config file has the CSV path
    save_plots(CSV)
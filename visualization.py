import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import os
from config import TRANSCRIBE_DIR 

files = os.listdir(TRANSCRIBE_DIR) # Take the first file for testing. In actual use case specify the file you want to transcribe

def generate_time_bucket_histogram(csv_path, bucket_size=5):
    '''Function to generate the histogram for 5 second buckets'''
    df = pd.read_csv(csv_path)

    if 'start' not in df.columns:
        print("Error : 'start' column not found.")
        return None

    if 'transcription' not in df.columns:
        print("Error: 'transcription' column not found in CSV.")
        return None

    df = df[pd.to_numeric(df['start'], errors='coerce').notnull()]
    df['start'] = df['start'].astype(float)
    df = df[np.isfinite(df['start'])]

    max_time = df['start'].max()
    print(f"Max Time : {max_time}")
    if max_time > 10000:
        print(f"Warning: Skipping histogram generation. max_time={max_time} is too large.")
        return None

    # Generate bucket edges and labels
    buckets = np.arange(0, max_time + bucket_size, bucket_size)
    bucket_labels = [
        f"{int(start // 60):02d}:{int(start % 60):02d}-{int((start + bucket_size) // 60):02d}:{int((start + bucket_size) % 60):02d}"
        for start in buckets[:-1]
    ]

    # Aggregate words into buckets
    bucket_counts = [0] * (len(buckets) - 1)
    for _, row in df.iterrows():
        start_time = row['start']
        word_count = len(str(row['transcription']).split())

        bucket_index = min(int(start_time // bucket_size), len(bucket_counts) - 1)
        bucket_counts[bucket_index] += word_count

    # Plotting
    plt.figure(figsize=(12, 6))
    plt.bar(bucket_labels, bucket_counts, color='skyblue')
    plt.title('Words per Time Bucket')
    plt.xlabel('Time Buckets')
    plt.ylabel('Number of Words')
    plt.xticks(rotation=45, ha='right')
    plt.tight_layout()

    return plt


def generate_sentiment_visualization(csv_path):
    '''Function to generate a pie chart of sentiment distribution'''

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
    '''Function to save plots in a folder'''

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
    save_plots(os.path.join(TRANSCRIBE_DIR,files[0]))
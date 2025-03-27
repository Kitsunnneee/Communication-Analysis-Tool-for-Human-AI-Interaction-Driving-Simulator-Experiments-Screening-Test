import tkinter as tk
from tkinter import filedialog, messagebox, ttk
import os
import threading
import sys
import subprocess

# Import your existing modules
from utils import video_to_audio, split_audio
from stt import transcribe
from sentiment import get_sentiment
from visualization import save_plots

import pandas as pd
import logging

class CommunicationAnalysisApp:
    def __init__(self, master):
        self.master = master
        master.title("Communication Analysis Tool")
        master.geometry("600x500")
        master.configure(bg='#f0f0f0')

        self.style = ttk.Style()
        self.style.configure('TLabel', background='#f0f0f0', font=('Arial', 10))
        self.style.configure('TButton', font=('Arial', 10))

        video_frame = ttk.Frame(master, padding="10")
        video_frame.pack(fill=tk.X, padx=10, pady=10)

        self.video_paths = []
        self.video_listbox = tk.Listbox(video_frame, height=5, width=70)
        self.video_listbox.pack(side=tk.LEFT, expand=True, fill=tk.X, padx=(0,10))

        scrollbar = ttk.Scrollbar(video_frame, orient=tk.VERTICAL, command=self.video_listbox.yview)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.video_listbox.config(yscrollcommand=scrollbar.set)

        button_frame = ttk.Frame(master, padding="10")
        button_frame.pack(fill=tk.X, padx=10)

        ttk.Button(button_frame, text="Select Videos", command=self.select_videos).pack(side=tk.LEFT, padx=5)
        ttk.Button(button_frame, text="Clear Videos", command=self.clear_videos).pack(side=tk.LEFT, padx=5)
        ttk.Button(button_frame, text="Run Analysis", command=self.run_analysis).pack(side=tk.LEFT, padx=5)

        progress_frame = ttk.Frame(master, padding="10")
        progress_frame.pack(fill=tk.X, padx=10)

        self.progress_label = ttk.Label(progress_frame, text="Ready to start analysis")
        self.progress_label.pack(side=tk.TOP, fill=tk.X)

        self.progress_bar = ttk.Progressbar(progress_frame, orient="horizontal", length=100, mode="determinate")
        self.progress_bar.pack(side=tk.TOP, fill=tk.X, pady=5)

        viz_frame = ttk.Frame(master, padding="10")
        viz_frame.pack(fill=tk.X, padx=10)

        ttk.Button(viz_frame, text="Generate Visualizations", command=self.generate_visualizations).pack(side=tk.LEFT, padx=5)
        ttk.Button(viz_frame, text="Open Plots Folder", command=self.open_plots_folder).pack(side=tk.LEFT, padx=5)

        logging.basicConfig(level=logging.INFO, 
                            format='%(asctime)s - %(levelname)s: %(message)s',
                            handlers=[
                                logging.StreamHandler(sys.stdout),
                                logging.FileHandler('analysis_log.txt')
                            ])

    def select_videos(self):
        filetypes = [('Video Files', '*.mp4'), ('All Files', '*.*')]
        selected_videos = filedialog.askopenfilenames(title="Select Video Files", filetypes=filetypes)
        
        for video in selected_videos:
            if video not in self.video_paths:
                self.video_paths.append(video)
                self.video_listbox.insert(tk.END, os.path.basename(video))

    def clear_videos(self):
        self.video_paths.clear()
        self.video_listbox.delete(0, tk.END)

    def run_analysis(self):
        if not self.video_paths:
            messagebox.showerror("Error", "Please select video files first.")
            return

        os.makedirs('Videos', exist_ok=True)
        os.makedirs('Audios', exist_ok=True)
        os.makedirs('Segments', exist_ok=True)

        for video_path in self.video_paths:
            subprocess.run(['cp', video_path, 'Videos/'])

        thread = threading.Thread(target=self._run_analysis_thread)
        thread.start()

    def _run_analysis_thread(self):
        try:
            self.update_progress("Extracting audio from videos...")
            video_to_audio('Videos', 'Audios')

            self.update_progress("Splitting audio into segments...")
            split_audio('Audios', 'Segments')

            self.update_progress("Transcribing audio...")
            transcribe('Segments', 'Transcription.csv')

            self.update_progress("Performing sentiment analysis...")
            data = pd.read_csv('Transcription.csv')
            get_sentiment(data)

            self.update_progress("Analysis complete!")
            messagebox.showinfo("Success", "Analysis completed successfully!")
        except Exception as e:
            logging.error(f"Analysis failed: {e}")
            messagebox.showerror("Error", f"Analysis failed: {e}")

    def update_progress(self, message):
        self.progress_label.config(text=message)
        self.progress_bar['value'] += 25
        if self.progress_bar['value'] >= 100:
            self.progress_bar['value'] = 100

    def generate_visualizations(self):
        try:
            save_plots('Transcription.csv')
            messagebox.showinfo("Success", "Visualizations generated in 'plots' directory!")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to generate visualizations: {e}")

    def open_plots_folder(self):
        plots_path = os.path.abspath('./plots')
        if os.path.exists(plots_path):
            if sys.platform.startswith('darwin'):  
                subprocess.run(['open', plots_path])
            elif sys.platform.startswith('win'): 
                os.startfile(plots_path)
            else:  
                subprocess.run(['xdg-open', plots_path])
        else:
            messagebox.showwarning("Warning", "Plots folder does not exist. Run analysis first.")

def main():
    root = tk.Tk()
    app = CommunicationAnalysisApp(root)
    root.mainloop()

if __name__ == "__main__":
    main()
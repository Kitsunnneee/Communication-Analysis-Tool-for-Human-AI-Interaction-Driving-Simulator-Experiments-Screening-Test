import tkinter as tk
from tkinter import filedialog, messagebox, ttk
import os
import sys
import subprocess
import pandas as pd
import logging

from visualization import save_plots

class CommunicationAnalysisApp:
    def __init__(self, master):
        self.master = master
        master.title("Communication Analysis Tool")
        master.geometry("600x400")
        master.configure(bg='#f0f0f0')

        self.style = ttk.Style()
        self.style.configure('TLabel', background='#f0f0f0', font=('Arial', 10))
        self.style.configure('TButton', font=('Arial', 10))

        file_frame = ttk.Frame(master, padding="10")
        file_frame.pack(fill=tk.X, padx=10, pady=10)

        self.file_path = tk.StringVar()
        ttk.Label(file_frame, text="Selected Transcription File:").pack(anchor='w')
        self.file_entry = ttk.Entry(file_frame, textvariable=self.file_path, state='readonly', width=60)
        self.file_entry.pack(side=tk.LEFT, padx=(0, 5))
        ttk.Button(file_frame, text="Upload Transcription File", command=self.upload_file).pack(side=tk.LEFT)

        button_frame = ttk.Frame(master, padding="10")
        button_frame.pack(fill=tk.X, padx=10)

        ttk.Button(button_frame, text="Generate Visualizations", command=self.generate_visualizations).pack(side=tk.LEFT, padx=5)
        ttk.Button(button_frame, text="Open Plots Folder", command=self.open_plots_folder).pack(side=tk.LEFT, padx=5)

        self.progress_label = ttk.Label(master, text="Ready to start analysis")
        self.progress_label.pack(pady=10)

        logging.basicConfig(level=logging.INFO, 
                            format='%(asctime)s - %(levelname)s: %(message)s',
                            handlers=[
                                logging.StreamHandler(sys.stdout),
                                logging.FileHandler('analysis_log.txt')
                            ])

    def upload_file(self):
        filetypes = [('CSV Files', '*.csv'), ('All Files', '*.*')]
        selected_file = filedialog.askopenfilename(title="Select Transcription File", filetypes=filetypes)
        if selected_file:
            self.file_path.set(selected_file)

    def generate_visualizations(self):
        if not self.file_path.get():
            messagebox.showerror("Error", "Please upload a transcription file first.")
            return
        try:
            save_plots(self.file_path.get())
            messagebox.showinfo("Success", "Visualizations generated in 'plots' directory!")
        except Exception as e:
            logging.error(f"Visualization generation failed: {e}")
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
            messagebox.showwarning("Warning", "Plots folder does not exist. Generate visualizations first.")


def main():
    root = tk.Tk()
    app = CommunicationAnalysisApp(root)
    root.mainloop()


if __name__ == "__main__":
    main()

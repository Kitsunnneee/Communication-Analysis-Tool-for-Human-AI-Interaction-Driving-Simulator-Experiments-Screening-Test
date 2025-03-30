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
        master.geometry("800x600")
        
        # Set theme colors
        self.primary_color = "#2c3e50"
        self.secondary_color = "#ecf0f1"
        self.accent_color = "#3498db"
        self.success_color = "#2ecc71"
        
        # Configure the window
        master.configure(bg=self.secondary_color)
        master.option_add("*Font", "Helvetica 10")
        
        # Create and configure styles
        self.configure_styles()
        
        # Create main frames
        self.create_header_frame()
        self.create_content_frame()
        self.create_status_bar()
        
        # Set up logging
        self.setup_logging()

    def configure_styles(self):
        """Configure ttk styles for a modern look"""
        self.style = ttk.Style()
        
        # Configure common styles
        self.style.configure('TFrame', background=self.secondary_color)
        self.style.configure('TLabel', background=self.secondary_color, font=('Helvetica', 10))
        self.style.configure('Header.TLabel', background=self.primary_color, foreground='white', font=('Helvetica', 14, 'bold'))
        self.style.configure('Title.TLabel', font=('Helvetica', 12, 'bold'))
        
        # Configure specialized frames
        self.style.configure('Primary.TFrame', background=self.primary_color)
        
        # Configure button styles
        self.style.configure('TButton', font=('Helvetica', 10))
        self.style.configure('Primary.TButton', background=self.accent_color)
        
        # Configure entry styles
        self.style.configure('TEntry', fieldbackground='white')
        
        # Configure progressbar
        self.style.configure('TProgressbar', troughcolor=self.secondary_color, background=self.accent_color)

    def create_header_frame(self):
        """Create the header section"""
        header_frame = ttk.Frame(self.master, style='TFrame')
        header_frame.pack(fill=tk.X)
        
        # Use a standard tk Frame for custom background color
        title_container = tk.Frame(header_frame, bg=self.primary_color, height=60)
        title_container.pack(fill=tk.X)
        
        # App title
        title_label = tk.Label(title_container, text="Communication Analysis Tool", 
                              bg=self.primary_color, fg="white", font=('Helvetica', 14, 'bold'))
        title_label.pack(pady=15)

    def create_content_frame(self):
        """Create the main content area"""
        main_frame = ttk.Frame(self.master, style='TFrame')
        main_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
        
        # File selection section
        file_section = ttk.LabelFrame(main_frame, text="File Selection", padding="10")
        file_section.pack(fill=tk.X, pady=10)
        
        self.file_path = tk.StringVar()
        
        file_label = ttk.Label(file_section, text="Transcription File:", style='TLabel')
        file_label.grid(row=0, column=0, sticky='w', pady=5)
        
        file_frame = ttk.Frame(file_section, style='TFrame')
        file_frame.grid(row=1, column=0, sticky='ew', pady=5)
        file_section.columnconfigure(0, weight=1)
        
        self.file_entry = ttk.Entry(file_frame, textvariable=self.file_path, state='readonly', width=60)
        self.file_entry.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(0, 10))
        
        upload_button = ttk.Button(file_frame, text="Browse...", command=self.upload_file, width=15)
        upload_button.pack(side=tk.RIGHT)
        
        # Actions section
        actions_section = ttk.LabelFrame(main_frame, text="Actions", padding="10")
        actions_section.pack(fill=tk.X, pady=10)
        
        actions_frame = ttk.Frame(actions_section, style='TFrame')
        actions_frame.pack(fill=tk.X, pady=5)
        
        # Use the native ttk.Button for consistent look across platforms
        generate_button = ttk.Button(actions_frame, text="Generate Visualizations", 
                                  command=self.generate_visualizations, width=25)
        generate_button.pack(side=tk.LEFT, padx=5, pady=10)
        
        open_folder_button = ttk.Button(actions_frame, text="Open Plots Folder", 
                                      command=self.open_plots_folder, width=20)
        open_folder_button.pack(side=tk.LEFT, padx=5, pady=10)
        
        # Progress section
        progress_section = ttk.LabelFrame(main_frame, text="Progress", padding="10")
        progress_section.pack(fill=tk.X, pady=10)
        
        self.progress_var = tk.DoubleVar()
        self.progress_bar = ttk.Progressbar(progress_section, orient=tk.HORIZONTAL, 
                                         length=100, mode='determinate', 
                                         variable=self.progress_var)
        self.progress_bar.pack(fill=tk.X, pady=10)
        
        self.progress_label = ttk.Label(progress_section, text="Ready to start analysis", style='TLabel')
        self.progress_label.pack(pady=5)

    def create_status_bar(self):
        """Create a status bar at the bottom"""
        # Use standard tk Frame for status bar to allow direct background setting
        status_frame = tk.Frame(self.master, relief=tk.SUNKEN, bg=self.primary_color)
        status_frame.pack(side=tk.BOTTOM, fill=tk.X)
        
        self.status_label = tk.Label(status_frame, text="Ready", fg="white", bg=self.primary_color)
        self.status_label.pack(side=tk.LEFT, padx=10, pady=3)

    def setup_logging(self):
        """Set up logging configuration"""
        logging.basicConfig(level=logging.INFO, 
                            format='%(asctime)s - %(levelname)s: %(message)s',
                            handlers=[
                                logging.StreamHandler(sys.stdout),
                                logging.FileHandler('analysis_log.txt')
                            ])

    def upload_file(self):
        """Handle file selection"""
        filetypes = [('CSV Files', '*.csv'), ('All Files', '*.*')]
        selected_file = filedialog.askopenfilename(title="Select Transcription File", filetypes=filetypes)
        if selected_file:
            self.file_path.set(selected_file)
            self.update_status(f"File selected: {os.path.basename(selected_file)}")

    def generate_visualizations(self):
        """Generate visualizations from the selected file"""
        if not self.file_path.get():
            messagebox.showerror("Error", "Please upload a transcription file first.")
            return
            
        try:
            # Reset progress
            self.progress_var.set(0)
            self.progress_label.config(text="Generating visualizations...")
            self.update_status("Processing...")
            self.master.update_idletasks()
            
            # Simulate progress (in a real app, you'd update this based on actual progress)
            for i in range(1, 101):
                self.master.after(20)  # Small delay for visual feedback
                self.progress_var.set(i)
                self.master.update_idletasks()
                
            # Generate the actual visualizations
            save_plots(self.file_path.get())
            
            self.progress_label.config(text="Visualizations completed successfully!")
            self.update_status("Completed")
            messagebox.showinfo("Success", "Visualizations generated in 'plots' directory!")
            
        except Exception as e:
            logging.error(f"Visualization generation failed: {e}")
            self.progress_label.config(text=f"Error: {str(e)}")
            self.update_status("Error")
            messagebox.showerror("Error", f"Failed to generate visualizations: {e}")

    def open_plots_folder(self):
        """Open the plots folder in the file explorer"""
        plots_path = os.path.abspath('./plots')
        if os.path.exists(plots_path):
            if sys.platform.startswith('darwin'):
                subprocess.run(['open', plots_path])
            elif sys.platform.startswith('win'):
                os.startfile(plots_path)
            else:
                subprocess.run(['xdg-open', plots_path])
            self.update_status(f"Opened plots folder: {plots_path}")
        else:
            self.update_status("Plots folder not found")
            messagebox.showwarning("Warning", "Plots folder does not exist. Generate visualizations first.")

    def update_status(self, message):
        """Update the status bar message"""
        self.status_label.config(text=message)


def main():
    root = tk.Tk()
    app = CommunicationAnalysisApp(root)
    root.mainloop()


if __name__ == "__main__":
    main()
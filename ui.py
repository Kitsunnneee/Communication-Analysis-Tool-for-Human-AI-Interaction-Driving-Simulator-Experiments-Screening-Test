import tkinter as tk
from tkinter import filedialog, messagebox, ttk
import sys
import logging
import os
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from PIL import Image, ImageTk
from visualization import generate_time_bucket_histogram, generate_sentiment_visualization


class CommunicationAnalysisApp:
    def __init__(self, master):
        self.master = master
        master.title("Communication Analysis Tool")
        master.geometry("1000x700")

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

    def setup_logging(self):
        logging.basicConfig(level=logging.INFO,
                            format='%(asctime)s - %(levelname)s: %(message)s',
                            handlers=[
                                logging.StreamHandler(sys.stdout),
                                logging.FileHandler('analysis_log.txt')
                            ])

    def configure_styles(self):
        self.style = ttk.Style()
        self.style.configure('TFrame', background=self.secondary_color)
        self.style.configure('TLabel', background=self.secondary_color)

    def create_header_frame(self):
        header_frame = ttk.Frame(self.master)
        header_frame.pack(fill=tk.X)
        title_label = ttk.Label(header_frame, text="Communication Analysis Tool", font=('Helvetica', 16, 'bold'))
        title_label.pack(pady=10)

    def create_content_frame(self):
        content_frame = ttk.Frame(self.master)
        content_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)

        file_frame = ttk.Frame(content_frame)
        file_frame.pack(fill=tk.X)
        self.file_path = tk.StringVar()
        file_label = ttk.Label(file_frame, text="Transcription File:")
        file_label.pack(side=tk.LEFT)
        self.file_entry = ttk.Entry(file_frame, textvariable=self.file_path, width=60)
        self.file_entry.pack(side=tk.LEFT, padx=5)
        browse_button = ttk.Button(file_frame, text="Browse", command=self.upload_file)
        browse_button.pack(side=tk.LEFT)

        self.plot_frame = ttk.Frame(content_frame)
        self.plot_frame.pack(fill=tk.BOTH, expand=True)

        generate_button = ttk.Button(content_frame, text="Generate Visualizations", command=self.generate_visualizations)
        generate_button.pack(pady=10)

    def upload_file(self):
        filetypes = [('CSV Files', '*.csv'), ('All Files', '*.*')]
        selected_file = filedialog.askopenfilename(title="Select Transcription File", filetypes=filetypes)
        if selected_file:
            self.file_path.set(selected_file)

    def generate_visualizations(self):
        file_path = self.file_path.get()
        if not file_path:
            messagebox.showerror("Error", "Please select a file.")
            return

        try:
            for widget in self.plot_frame.winfo_children():
                widget.destroy()

            output_dir = './plots'
            os.makedirs(output_dir, exist_ok=True)

            fig1 = generate_time_bucket_histogram(file_path)
            histogram_path = os.path.join(output_dir, 'transcription_histogram.png')
            fig1.savefig(histogram_path)
            fig1.clf()

            fig2 = generate_sentiment_visualization(file_path)
            sentiment_path = os.path.join(output_dir, 'sentiment_distribution.png')
            fig2.savefig(sentiment_path)
            fig2.clf()

            self.display_image(histogram_path)
            self.display_image(sentiment_path)

            messagebox.showinfo("Success", "Visualizations generated and displayed successfully!")

        except Exception as e:
            logging.error(f"Visualization generation failed: {e}")
            messagebox.showerror("Error", f"Failed to generate visualizations: {e}")

    def display_image(self, image_path):
        try:
            img = Image.open(image_path)
            img = img.resize((500, 300), Image.LANCZOS)
            img_tk = ImageTk.PhotoImage(img)
            label = ttk.Label(self.plot_frame, image=img_tk)
            label.image = img_tk
            label.bind("<Button-1>", lambda e: self.open_zoomable_image(image_path))
            label.pack(side=tk.TOP, fill=tk.BOTH, expand=True, pady=10)
        except Exception as e:
            logging.error(f"Failed to display image {image_path}: {e}")
            messagebox.showerror("Error", f"Failed to display image: {e}")

    def open_zoomable_image(self, image_path):
        zoom_window = tk.Toplevel(self.master)
        zoom_window.title("Zoomable Image")

        canvas = tk.Canvas(zoom_window, bg="white")
        scroll_x = tk.Scrollbar(zoom_window, orient="horizontal", command=canvas.xview)
        scroll_y = tk.Scrollbar(zoom_window, orient="vertical", command=canvas.yview)
        canvas.configure(xscrollcommand=scroll_x.set, yscrollcommand=scroll_y.set)

        img = Image.open(image_path)
        img_tk = ImageTk.PhotoImage(img)

        canvas.create_image(0, 0, anchor="center", image=img_tk)
        canvas.image = img_tk  # Keep a reference to avoid garbage collection
        canvas.config(scrollregion=canvas.bbox("all"))

        canvas.pack(fill="both", expand=True)
        scroll_x.pack(fill="x", side="bottom")
        scroll_y.pack(fill="y", side="right")


    def create_status_bar(self):
        status_frame = ttk.Frame(self.master)
        status_frame.pack(side=tk.BOTTOM, fill=tk.X)
        self.status_label = ttk.Label(status_frame, text="Ready")
        self.status_label.pack(side=tk.LEFT)


def main():
    root = tk.Tk()
    app = CommunicationAnalysisApp(root)
    root.mainloop()


if __name__ == "__main__":
    main()

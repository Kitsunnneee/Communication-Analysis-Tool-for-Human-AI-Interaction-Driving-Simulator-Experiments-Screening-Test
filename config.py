import torch

VIDEO_PATH = "Videos"
AUDIO_PATH = "Audios"
SEG_PATH = "Segments"
CSV = "Transcription.csv"
model_name = "tiny"

dvce = torch.device("cuda" if torch.cuda.is_available() else "cpu")
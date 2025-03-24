import os 
import logging
from pydub import AudioSegment
from config import VIDEO_PATH,AUDIO_PATH

logging.basicConfig(level=logging.INFO)

def read_directory(dir_path):
    '''Reads and return all the files in the directory'''
    if not os.path.exists(dir_path):
        logging.error("Directory does not exist")
        return
    dir_list = os.listdir(dir_path)
    video_files = [file for file in dir_list if file.endswith('.mp4')] #Change mp4 to the video format you are using
    logging.info(f" Found {len(video_files)} video files")
    return video_files

def extract_audio(video_path, output_audio_path):
    '''Extracts audio from the video file'''
    try:
        # print(video_path)
        # print(output_audio_path)
        video = AudioSegment.from_file(video_path)
        video.export(output_audio_path, format='wav')
        logging.info(f"Successfully extracted audio from {video_path} -> {output_audio_path}")
    except Exception as e:
        logging.error(f"Failed to extract audio from {video_path}")

def video_to_audio(video_dir, output_dir):
    '''Goes through the directory and extracts audio from each video file'''
    if not os.path.exists(output_dir):
        os.makedirs(output_dir,exist_ok=True)
        
    videos = read_directory(video_dir)
    if not videos:
        logging.error("No video files found")
        return
    
    for video in videos:
        full_path = os.path.join(video_dir, video)
        full_audio_path = os.path.join(output_dir, video.split('.')[0] + '.wav')
        
        if not os.path.exists(full_path):
            logging.error(f"File {full_path} does not exist.Skipping...")
            continue
        extract_audio(full_path, full_audio_path)
        
        
    
path = VIDEO_PATH
output_dir = AUDIO_PATH
videos = read_directory(path)

video_to_audio(path, output_dir)
import os 
import logging
from pydub import AudioSegment
from config import split_length

logging.basicConfig(level=logging.INFO)

def read_directory(dir_path):
    '''Function that reads and return all the files in the directory'''
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
        video = AudioSegment.from_file(video_path)
        video.export(output_audio_path, format='wav')
        logging.info(f"Successfully extracted audio from {video_path} -> {output_audio_path}")
    except Exception as e:
        logging.error(f"Failed to extract audio from {video_path}")

def video_to_audio(video_dir, output_dir):
    '''Function that goes through the directory and extracts audio from each video file'''
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

def split_audio(input_audio_dir, output_dir,split = split_length):
    '''Function that split the all audio in Audios directory into desired amounts of second and save them'''
    if not os.path.exists(input_audio_dir):
        logging.error("Directory does not exist")
        return
    
    audio_files = [f for f in os.listdir(input_audio_dir) if f.endswith('.wav')]
    if not audio_files:
        logging.error("No audio files found")
        return
    logging.info(f"Found {len(audio_files)} audio files")
    for audio_f in audio_files:
        try:
            full_path = os.path.join(input_audio_dir, audio_f)
            audio = AudioSegment.from_file(full_path)
            audio_len = len(audio)
            logging.info(f"Splitting {audio_f} into {audio_len//split} segments")
            base_name = os.path.splitext(audio_f)[0]
            # print(base_name[0])
            audio_out_dir = os.path.join(output_dir, base_name)
            os.makedirs(audio_out_dir, exist_ok=True)
            for i, start in enumerate(range(0, audio_len, split)):
                end = min(start+split, audio_len)
                audio_chunk = audio[start:end]
                chunk_name = os.path.join(audio_out_dir, f"{base_name}_{i}.wav")
                audio_chunk.export(chunk_name, format='wav')
                logging.info(f"Saved {chunk_name}")
                
        except Exception as e:
            logging.error(f"Failed to split {audio}")

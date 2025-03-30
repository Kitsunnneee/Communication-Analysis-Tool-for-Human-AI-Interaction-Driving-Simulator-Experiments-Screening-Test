
# Communication Analysis Tool for Human-AI Interaction Driving Simulator Experiments – Screening Test

This is the test for HumanAI for the Project titled : Communication Analysis Tool for Human-AI Interaction Driving Simulator Experiments. It contains all the neccessary codes, information on how to run it, the requirements, screenshots and video demonstration and how everything was tested.


## Requirements for Running

**NOTE** : All the tasks were run on **MacOS** and **python version 3.10 .16**.  So, you may face issues for Windows or Ubuntu or wrong python versions.

To deploy this project : 


1. Install everything in the requirements file : 

```bash
  pip install -r requirements.txt
```
2. Install tkinter for UI.
    
For Linux based systems : 

```bash
  sudo apt-get update
  sudo apt-get install python3-tk

```   
    
For MacOS : 

 ```bash
    brew install python-tk@3.10

``` 

For Windows : 

It's bundled with python in Windows.

3. Install sox for audio processing tasks.
For Linux based systems :
 ```bash
    sudo apt-get update
    sudo apt-get install sox libsox-fmt-all
``` 


For MacOS : 
 ```bash
    brew install sox
``` 

For Windows:

Download from : **[Here](https://sourceforge.net/projects/sox/)** .
Follow the instuctions and add sox to your **system's path**.






## How to Run?

1. In order to Run for **Test 1** : 

- First, put you configuration in the config.py file : 
```bash
    VIDEO_PATH = "Videos" # Specify the path of the directory containing videos
    AUDIO_PATH = "Audios" # Specify the path of the directory where audio will be saved
    SEG_PATH = "Segments" # Specify the path of the directory where the segments will be saved
    TRANSCRIBE_DIR = "Transcription" # Specify the transcription directory name
    model_name = "tiny" # Specify the STT model (Whisper)
    split_length = 2000 # Specify the split length for audio
```

- Now for Running the code for video to audio conversion , splitting, transcribing and then doing sentiment analysis 
```bash
  python main.py
```
2. In order to Run **Test 2** :

- First, for visualizing histogram for word count and pie chart for sentiment : 

```bash
  python visualization.py
```

- After this in order to run the UI : 
```bash
  python ui.py
```

This will open up the UI. You have to upload your CSV file and it will generate and display the plots and save them in a plot folder.
## Information on the Code and Test

- File structure should be like this : 
```bash
├── Audios # Contains audio of all the videos
│   └── file_name_1.wav
|   └── file_name_2.wav
├── Segments # Contains subfolder containing segments for al the audio
│   └── file_name_1
|   └── file_name_2
├── Transcriptions # Contains the transcription and sentiment analysis csvs for the audios.
├── Videos # Contains the videos.
├── config.py
├── main.py
├── plots # contains the plots
├── requirements.txt
├── sentiment.py
├── stt.py
├── ui.py
├── utils.py
└── visualization.py
```

- I started with writing the **utils.py** function  which handled the basic functionalities of Extracting audio from each Video in the directory, creating segments for each audio and saving the same. For all of these tasks I have used PyDub. I have also added a **config.py** to make the task of naming the directories and models and split length easier in one place only.

- Next I moved onto STT and Sentiment analysis task. Here I have used [**faster-whisper**](https://github.com/SYSTRAN/faster-whisper) library for transcription as it uses CTranslate2 which makes the inferencing much more faster. For sentiment I have used a library called [**pysentimiento**](https://arxiv.org/pdf/2106.09462) as it already contains Fine-trained model(by default uses BERTweet) for sentiment analysis which it downloads from HuggingFace and uses. Below are attached metric from their paper for the benchmarks(done on mean MARCO F1 score for 10 runs) :

![Benchmarks](https://via.placeholder.com/468x300?text=App+Screenshot+Here)

- 


# Communication Analysis Tool for Human-AI Interaction Driving Simulator Experiments – Screening Test

This is the test for HumanAI for the Project titled : Communication Analysis Tool for Human-AI Interaction Driving Simulator Experiments. It contains all the neccessary codes, information on how to run it, the requirements, screenshots and video demonstration and how everything was tested.


## Requirements for Running

**NOTE** : All the tasks were run on **MacOS** and **python version 3.10 .16**.  So, you may face issues for Windows or Ubuntu or wrong python versions.

To deploy this project : 

1. Create Virtual Enviroment and activate it :
```bash
  python -m venv humanai
  source humanai/bin/activate
```


2. Install everything in the requirements file : 

```bash
  pip install -r requirements.txt
```
3. Install tkinter for UI.
    
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

4. Install sox for audio processing tasks.
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
├── Audios
│   └── Experimenter_CREW_999_1_All_1731617801.wav
├── README.md
├── Segments
│   └── Experimenter_CREW_999_1_All_1731617801
│       ├── Experimenter_CREW_999_1_All_1731617801_0.wav
│       ├── Experimenter_CREW_999_1_All_1731617801_1.wav
|       .
|       .
|       .
├── Transcriptions
│   └── Experimenter_CREW_999_1_All_1731617801_71.csv
├── Videos
│   └── Experimenter_CREW_999_1_All_1731617801.mp4
├── config.py
├── main.py
├── plots
│   ├── sentiment_distribution.png
│   └── transcription_histogram.png
├── requirements.txt
├── sentiment.py
├── stt.py
├── test
│   ├── __init__.py
│   ├── test_sentiment.py
│   ├── test_stt.py
│   ├── test_ui.py
│   ├── test_utils.py
│   └── test_visualization.py
├── ui.py
├── utils.py
└── visualization.py
```

- I started with writing the **utils.py** function  which handled the basic functionalities of Extracting audio from each Video in the directory, creating segments for each audio and saving the same. For all of these tasks I have used PyDub. I have also added a **config.py** to make the task of naming the directories and models and split length easier in one place only.

- Next I moved onto STT and Sentiment analysis task. Here I have used [**faster-whisper**](https://github.com/SYSTRAN/faster-whisper) library for transcription as it uses CTranslate2 which makes the inferencing much more faster. For sentiment I have used a library called [**pysentimiento**](https://arxiv.org/pdf/2106.09462) as it already contains Fine-trained model(by default uses BERTweet) for sentiment analysis which it downloads from HuggingFace and uses. When calculating the start of transcription of segments to match with the actual audio/video timestamp I have used this logic: I am keeping a count of any time a audio is silent using VAD(Voice Activity Detection). Whenever a segment is getting skipped due to VAD I keep a count of it. Now, When calculating the actual timestamp of the start of the segment in comparison with the actual Video/Audio I calculate the absolute start as absolute start -> segment index(taken from the filename) * the split length + 0(segment start) + 1 . 
**For running all the model I have defaulted to 'cpu' due to personal GPU restriction**

Below are attached metric from their paper for the benchmarks(done on mean MARCO F1 score for 10 runs) :

![Benchmarks](assets/Screenshot 2025-03-31 at 1.08.20 AM.png)

- After this, we move on to the second portion of the test that is to vizualize and create an application to load any transcription and generate graphs. For the this portion the logic is simple first I calculate the total duration of the Video. For each row of transcription.csv file I take the start time and the transcription and I figure out which bucket the row falls to by start time // bucket size(5 second in this case). This gives us which bucket the current row falls into. we pass the above to a min() function with the other parameter being len(bucket count) - 1. This help us in case the start time // bucket size is more than the bucket count. Thus, the row will fall in the last bucket always. After this I count the words for each row and create a bar graph/histogram using matplotlib.

- For the second visualization, I use a simple pie chart. I count the sentiment column for each row and then create a pie chart using simple matplotlib functions.



## Demo Video

![AppVideoDemo]()


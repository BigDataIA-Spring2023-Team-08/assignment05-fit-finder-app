from diagrams.custom import Custom
from diagrams import Cluster, Diagram, Edge
from diagrams.aws.compute import EC2
from diagrams.aws.database import RDS
from diagrams.aws.integration import SQS
from diagrams.aws.storage import S3
from diagrams.onprem.client import User
from diagrams.programming.framework import FastAPI
from diagrams.programming.language import Python
from diagrams.onprem.workflow import Airflow
from diagrams.programming.framework import Flask
from diagrams.digitalocean.storage import Folder

with Diagram("Fit Finder App Architecture", show=False,direction="LR"):
    with Cluster("Compute Instance"):

        with Cluster("Streamlit"):
            streamlit_app = Custom("Streamlit", "./streamlit-icon.png")

        with Cluster("APIs"):
            whisper_api = Custom("Whisper API", "./whisper-icon.png")
            chat_api = Custom("Chat API", "./chatgpt-icon.png")
            youtube_api = Custom("YouTube API", "./youtubeapi2.png")
        with Cluster("System"):
            audio_files = Folder("Audio Folder")
            transcriptions = Folder("Transcription Folder")



        # with Cluster("Database"):
        #     db_instance = RDS("RDS")

        # with Cluster("Storage"):
        #     audio_files = S3("Audio Files")

        # with Cluster("Message Queue"):
        #     message_queue = SQS("Message Queue")

    with Cluster("User"):
        user = User("User")

    user >> Edge(label="Access FitFinder application") >> streamlit_app
    streamlit_app >> Edge(label="Search request related to user query") >> youtube_api
    youtube_api >> Edge(label="Store the audio files from the suggestion") >> audio_files
    audio_files >> Edge(label="Transcribe the audio files using Whisper") >> whisper_api
    whisper_api >> Edge(label="Store the transcriptions from whisper API") >> transcriptions






    #user >> whisper_api >> audio_conversion >> audio_files
    #audio_conversion >> chat_api >> message_queue
    # dag_batch >> audio_conversion
    # dag_adhoc >> chat_api
    #audio_files >> audio_conversion
    # audio_conversion >> db_instance
    #message_queue >> chat_api
    #whisper_api >> audio_conversion
    streamlit_app >> whisper_api
    streamlit_app >> chat_api

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

with Diagram("Fit Finder App Architecture", show=False, direction="RL"):
    with Cluster("Compute Instance"):
        with Cluster("Streamlit"):
            streamlit_app = Custom("Streamlit", "./streamlit-icon.png")

        with Cluster("APIs"):
            whisper_api = Custom("Whisper API", "./whisper-icon.png")
            youtube_api = Custom("YouTube API", "./youtubeapi2.png")

        with Cluster("GPT"):
            chat_api = Custom("Chat API", "./chatgpt-icon.png")

        with Cluster("Storage"):
            json = S3("JSON")

    with Cluster("User"):
        user = User("User")

    user >> Edge(label="Access FitFinder application") >> streamlit_app
    youtube_api >> Edge(
        label="Search for videos and send audio to whisper") >> whisper_api
    whisper_api >> Edge(
        label="Transcribe and store the transcript from whisper in S3") >> json
    streamlit_app << Edge(label="Fetch JSON from S3") >> json
    json >> Edge(label="Construct Prompt based on User Query") >> chat_api
    chat_api >> Edge(
        label="Provide user with embedded link and relevant info") >> user

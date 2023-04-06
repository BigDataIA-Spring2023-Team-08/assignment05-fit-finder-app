from google.oauth2 import service_account
from googleapiclient.discovery import build
import openai
import os
from pytube import YouTube
from pydub import AudioSegment
from pydotenvs import load_env

#load local environment
load_env()

# set up Youtube API key and credentials
PATH_TO_SERVICE_ACCOUNT_JSON = 'bdia-hackathon-3c59b20ab4da.json'
api_key = os.environ.get('YOUTUBE_KEY')
scopes = ['https://www.googleapis.com/auth/youtube.force-ssl']
credentials = service_account.Credentials.from_service_account_file(f'bdia-hackathon-3c59b20ab4da.json', scopes=scopes)


# Set up OpenAI API key
openai.api_key = os.environ.get('OPENAI_KEY')

# Set up Whisper model ID
model_id = 'whisper-1'


# set up YouTube Data API client
youtube = build('youtube', 'v3', developerKey=api_key, credentials=credentials)

# make search request for videos related to "core workout"
search_response = youtube.search().list(
    q='5 minute core workout',
    part = 'id,snippet',
    type='video',
    videoDefinition='high',
    maxResults=2
).execute()

# output video IDs and titles
for search_result in search_response.get('items', []):
    video_id = search_result['id']['videoId']
    video_title = search_result['snippet']['title']
    video_link = f'https://www.youtube.com/watch?v={video_id}'
    print(f"Video ID: {search_result['id']['videoId']}")
    print(f"Title: {search_result['snippet']['title']}")
    print(f"Link: {video_link}")

    yt = YouTube(video_link)

    # get YouTube video
    video = YouTube(video_link)

    # # get audio stream and download it
    audio_stream = video.streams.filter(only_audio=True).first()
    audio_file_path = "audiofiles/"
    #audio_file_name = video_title
    file_name = video_title+"_audio.mp3"
    if audio_stream:
        audio_stream.download(output_path='', filename=audio_file_path+file_name)

    # # convert audio to mp3 format
    # try: 
    #     audio_file = AudioSegment.from_file(video_title + '_audio.mp4', format='mp4')
    #     audio_file.export(video.title + '_audio.mp3', format='mp3')
    # except PermissionError:
    #     print("Permission denied to ffprobe, skipping audio download")

    #### delete the original audio file in mp4 format
    #####os.remove(video.title + '_audio.mp4')

    transcription_folder = "transcriptions/"
    transcription_file_path = transcription_folder+video_title+'.txt'
    # audio_file_path = ""

    audio_file = open(audio_file_path+file_name, 'rb')
    model_id = 'whisper-1'
    transcription = openai.Audio.transcribe(api_key=openai.api_key, model=model_id, file=audio_file, response_format='text')
    with open(transcription_file_path, 'w') as f:
        f.write(transcription)

    # # Use Whisper API to transcribe audio
    # try:
    #     response = openai.Completion.create(
    #         engine=model_id,
    #         prompt=f'Transcribe the audio from {video_link}',
    #         max_tokens=500,
    #         n=1,
    #         stop=None,
    #         temperature=0.5,
    #     )
    #     # Save transcription to a text file
    #     transcription = response.choices[0].text
            
    #     filename = f'{video_title}.txt'
    #     with open(filename, 'w') as f:
    #         f.write(transcription)
    #     print(f'Successfully transcribed audio for {video_title} and saved transcription to {os.path.abspath(filename)}')
    # except Exception as e:
    #     print(f"Error transcribing video {video_id}: {str(e)}")
    #     continue

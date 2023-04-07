from google.oauth2 import service_account
from googleapiclient.discovery import build
import openai
import os
from pytube import YouTube
from pydub import AudioSegment
from pydotenvs import load_env
import json 
import boto3

#load local environment
load_env()

#set up Youtube API key and credentials
SERVICE_ACCOUNT_JSON = os.environ.get('SERVICE_ACCOUNT_JSON')   #path to credentials json file
api_key = os.environ.get('YOUTUBE_KEY')
scopes = ['https://www.googleapis.com/auth/youtube.force-ssl']
credentials = service_account.Credentials.from_service_account_file(SERVICE_ACCOUNT_JSON, scopes=scopes)

#set up OpenAI API key
openai.api_key = os.environ.get('OPENAI_KEY')

#set up AWS credentials
aws_access_key = os.environ.get('AWS_KEY')
aws_secret_key = os.environ.get('AWS_SECRET')
user_bucket = os.environ.get('USER_BUCKET')

#set up YouTube Data API client
youtube = build('youtube', 'v3', developerKey=api_key, credentials=credentials)

#authenticate S3 client with your user credentials that are stored in your .env config file
s3resource = boto3.resource('s3',
                        region_name='us-east-1',
                        aws_access_key_id = aws_access_key,
                        aws_secret_access_key = aws_secret_key
                        )

def get_search_scripts():
    #make search request for videos related to "core workout"
    yt_dict = {}    #to store all youtube video titles, link & transcript in a json

    search_queries = ['strengthening', 'balance', 'motion'] ##strengthening, balance & motion
    for query in search_queries:
        search_response = youtube.search().list(
                                                q=f"physiotherapy {query} exercises",
                                                part = 'id,snippet',
                                                type='video',
                                                #videoDefinition='high',
                                                maxResults=4
                                                ).execute()

        #output video IDs and titles
        for search_result in search_response.get('items', []):
            video_id = search_result['id']['videoId']
            video_title = search_result['snippet']['title']
            video_link = f'https://www.youtube.com/watch?v={video_id}'
            #print(f"Video ID: {search_result['id']['videoId']}")
            print(f"Title: {search_result['snippet']['title']}")
            print(f"Link: {video_link}")

            #get YouTube video
            video = YouTube(video_link)

            #get audio stream and download it
            audio_stream = video.streams.filter(only_audio=True).first()
            audio_file_path = "audiofiles/"
            file_name = video_title+"_audio.mp3"
            if audio_stream:
                audio_stream.download(output_path='', filename=audio_file_path+file_name)

            # transcription_folder = "transcriptions/"
            # transcription_file_path = transcription_folder+video_title+'.txt'

            audio_file = open(audio_file_path+file_name, 'rb')
            transcription = openai.Audio.transcribe(api_key=openai.api_key, 
                                                    model='whisper-1', 
                                                    file=audio_file, 
                                                    response_format='text')

            # with open(transcription_file_path, 'w') as f:
            #     f.write(transcription)

            yt_dict[search_result['snippet']['title']] = {  
                                                            'video_id': search_result['id']['videoId'],
                                                            'category': query,
                                                            'link': video_link,
                                                            'transcription': transcription     
                                                        }
        # break
    # print(yt_dict)
    with open("yt_json.json", "w") as outputFile:
        json.dump(yt_dict, outputFile)

    s3resource.Object(user_bucket, "yt_json.json").put(Body=open("yt_json.json", 'rb'))

def refine_search(category):
#############
    content_object = s3resource.Object(user_bucket, "yt_json.json")
    file_content = content_object.get()['Body'].read().decode('utf-8')
    json_content = json.loads(file_content)
    #print(json_content['Details'])
    # with open("yt_json.json","r") as file:
    #     jsonData = json.load(file)

    prompt = ""
    for title in json_content:
        if (json_content[title]['category']==category):
            prompt += "###\nTitle: " + title +"\nText: " + json_content[title]['transcription']
    print(prompt)

    system_prompt = "Your task is to find one which of the four scripts given about exercises best contains the information that the user asks"
    streamlit2 = 'lower body'
    streamlit3 = 'lower body'
    streamlit4 = "strengthening exercises where they cover transverse abdominus"
    streamlit5 = "movement"
    new_response = openai.ChatCompletion.create(model="gpt-3.5-turbo",
                                                        messages=[
                                                            {"role": "system", "content": system_prompt},
                                                            {"role": "user", "content": "Here are the 4 video scripts with titles for each"},
                                                            {"role": "user", "content": prompt},
                                                            {"role": "user", "content": f"Which of these scripts include exercises that involve {streamlit5}"},
                                                            ],
                                                        temperature=0,
                                                        max_tokens=200,
                                                        top_p=1,
                                                        frequency_penalty=0,
                                                        presence_penalty=0)
    new_response = new_response.choices[0].message.content.strip()
    print(new_response)
    for title in json_content:
        if (title in new_response):
            print("URL: ", json_content[title]["link"])
def main():
    #get_search_scripts()
    refine_search("motion")

if __name__ == "__main__":
    main()
# FitFinder Application - Find your stride!

![Smartwatch-amico](https://user-images.githubusercontent.com/46862684/230645366-290d9d0c-87ee-4989-ac75-45a20b9626e3.svg)

##### Image Source: [Storyset](https://storyset.com/)
----- 

> ✅ Active status <br>
> 🚀 Application is locally hosted <br>
> [🎬 Codelab Slides](https://codelabs-preview.appspot.com/?file_id=19JXjVTJK7lAo0XWgxmkERleQjft9QcoUmDpSHXRKSf0) <br>
> [📽️ Application Demo/Usage](https://drive.google.com/file/d/1JTiC1osBSS4qvRr9irH4fNb4Yrf8YlXz/view?usp=sharing)

----- 

## Index
  - [Motivation 🎯](#motivation)
  - [Technical Abstract 📝](#technical-abstract)
  - [Architecture Diagram 🏗](#architecture-diagram)
  - [Repository Components 🗃️](#repository-components)
  - [Project Components 💽](#project-components)
    - [APIs](#apis)
    - [Streamlit](#streamlit)
  - [Application Use Cases 📸](#application-use-cases)
  - [How to run the application 💻](#how-to-run-the-application-locally)
----- 

## Motivation

This app is developed as a part of a hackathon. Leveraging OpenAI's various APIs and any other API, we were asked to build something new and useful. FitFinder is a refined fitness helper which provides you with relevant videos based on things/exercises you are looking for. 

How is this different from YouTube search? Well, when you search for a single type of exercise on YouTube, you probably just get several videos which only contain that 1 exercise. Need more exercise? Sorry, you will have to do a new YouTube search. In comes FitFinder which can provide you with videos which have multiple exercises INCLUDING the exercise you initially searched for. This way you get to see and follow numerous exercises in a single video which is better than searching for videos of each exercise one after another

To build this application we use generative AI APIs such as **Whisper** and **GPT 3.5** APIs as well as **YouTube Data API**, integrated with [Streamlit](https://streamlit.iohttps://streamlit.io) for its user interface to illustrate application workflow.

## Technical Abstract
We narrow our **use-case for this to Physiotherapy.** Physiotherapy exercises are largely divided into 3 categories, namely, Strengthening, Motion & Balance exercises. 

The task involves building a decoupled architecture for the fitness application:
- Provide users with personalized workout plans based on user needs and goals using GPT 3.5 API
- Fetch links to 4 videos for each of these categories by search results from Youtube using YouTube's Data API
- Transcribe them using OpenAI's Whisper API for context based search results
- Store all transcribed details & video details in a JSON object on S3 bucket
- Ask users for more details like which body part/area are they looking to work on? And if they wish, what particular exercise they also wish to include?
- Use the details provided by the user to generate a relevant prompt 
- Send this prompt to GPT 3.5 API along with context of all 4 videos of the category
- Return the best matched video (embedded on streamlit UI) which has most content related to the body area user asked for & contains the exercise the user mentioned

## Architecture Diagram

![fit_finder_app_architecture](https://user-images.githubusercontent.com/46862684/230658753-b24a6c84-c2a0-436b-b5d8-167ff0115513.png)

## Repository Components

```
  ├── application-use-test-cases            # images for use cases
  │   ├── ff-balance-2.png
  │   ├── ff-balance.png
  │   ├── ff-motion.png
  │   ├── ff-strengthening.png
  │   ├── yt-balance.png
  │   ├── yt-motion.png
  │   └── yt-strengthening.png
  ├── architecture-diagram
  │   ├── arch-diagram.py                   # architectural diagram python code    
  │   └── fit_finder_app_architecture.png   # architectural diagram png
  ├── main
  │   ├── get_videos.py                     # code to get videos of from YouTube, process them with Whisper API & store JSON on S3
  │   └── requirements.txt                  # relevant package requirements file for main
  └──  streamlit-app
      ├── fitfinder-icon.png                # image for FitFinder application
      ├── fitfinder.py                      # application code for FitFinder
      ├── requirements.txt                  # relevant package requirements file for streamlit-app
      └── workout-app.jpeg                  # icon for tab view of FitFinder application
```

## Project Components

### APIs
**Whisper API:** API for [Whisper](https://openai.com/research/whisper) speech-to-text open-source model which provides two endpoints for transcriptions and translations and accepts variety of formats (m4a, mp3, mp4, mpeg, mpga, wav, webm). 

For the purpose of this assignment, Whisper API has been implemented to transcribe audio from Youtube Search results to later use them in context based matches with user requests using GPT 3.5 API.

**GPT 3.5 API:** API for [ChatGPT 3.5](https://openai.com/research/whisper) model which takes sequence of messages coupled with metadata as tokens to generate text completion which can either be natural language or code.

For the purpose of this assignment, GPT 3.5 API has been implemented to ask user for workout plans as well as build a query engine complemented by the transcripts of YouTube search results generated by Whisper to fetch best match to address user needs.

**YouTube Data API:** API for [YouTube](https://developers.google.com/youtube/v3) has been implemented to add YouTube's search functionality into our application. The API enables the application to search for the best 5 YouTube video searches based on search terms provided by users.

### Streamlit
Python library [Streamlit](https://streamlit.iohttps://streamlit.io) has been implemented in this application for its user interface. Streamlit offers user friendly experience to assist users in :

>  Request for best workout plans based on user goals and needs 

> Use these inputs to optimize searches

>  List videos related to physiotherapy based on user requests

## Application Use Cases

#### USE CASE 1

User wants to work on **strengthening** in which they wish to focus on the **core**. User also wants to have the exercise **transverse abdominus** included.

![ff-strength](https://github.com/BigDataIA-Spring2023-Team-08/assignment05-fit-finder-app/blob/main/application-use-test-cases/ff-strengthening.png)

<i>Notice how FitFinder provides a video which has **strengthening** physiotherapy exercise for the **core** but also contains the **transverse abdominus** exercise. This way a user can focus on their initial primary goal of training for strengthening core but also involve the transverse abdominus exercise rather than only show transverse abdominus exercise videos (which you get on a normal YouTube search as shown in next pic).</i>

#### TESTING RESULTS ON YOUTUBE:

<i>As you notice, YouTube results will only focus on that one exercise, in this case **transverse abdominus** and provide multiple videos plainly relating to this one exercise despite entering **physiotherapy strengthening transverse abdominus** as the search query</i>

![yt-strength](https://github.com/BigDataIA-Spring2023-Team-08/assignment05-fit-finder-app/blob/main/application-use-test-cases/yt-strengthening.png)

#### USE CASE 2

User wants to work on **motion** in which they wish to focus on the **legs**. User also wants to have the exercise **knee flexion** included.

![ff-motion](https://github.com/BigDataIA-Spring2023-Team-08/assignment05-fit-finder-app/blob/main/application-use-test-cases/ff-motion.png)

<i>Notice how FitFinder provides a video which has **motion** physiotherapy exercise for **legs** but also contains the **knee flexion** exercise. This way a user can focus on their initial primary goal of training for motion of legs but also involve the knee flexion exercise rather than only show knee flexion exercise videos (which you get on a normal YouTube search as shown in next pic).</i>

#### TESTING RESULTS ON YOUTUBE:

<i>As you notice, YouTube results will only focus on that one exercise, in this case **knee flexion** and provide multiple videos plainly relating to this one exercise **despite entering physiotherapy motion knee flexion** as the search query</i>

![yt-motion](https://github.com/BigDataIA-Spring2023-Team-08/assignment05-fit-finder-app/blob/main/application-use-test-cases/yt-motion.png)

#### USE CASE 3

User wants to work on **balancing** in which they wish to focus on the **legs**. User also wants to have the exercise **single leg balance** included.

![ff-balance](https://github.com/BigDataIA-Spring2023-Team-08/assignment05-fit-finder-app/blob/main/application-use-test-cases/ff-balance.png)

<i>Notice how FitFinder provides a video which has **balancing** physiotherapy exercise for the **legs** but also contains the **single leg balance** exercise. This way a user can focus on their initial primary goal of training for balancing legs but also involve the single leg balance exercise rather than only show single leg balance exercise videos (which you get on a normal YouTube search as shown in next pic).
</i>

#### TESTING RESULTS ON YOUTUBE:

<i>As you notice, YouTube results will only focus on that one exercise, in this case **single leg balance** and provide multiple videos plainly relating to this one exercise **despite entering physiotherapy single leg balance** as the search query</i>

![yt-balance](https://github.com/BigDataIA-Spring2023-Team-08/assignment05-fit-finder-app/blob/main/application-use-test-cases/yt-balance.png)

## How to run the application locally

1. Clone the repo to get all the source code on your machine

2. Lets look at the `main` folder first & run that code

  - First, create a virtual environment and install all requirements from the [`requirements.txt`](https://github.com/BigDataIA-Spring2023-Team-08/assignment05-fit-finder-app/blob/main/main/requirements.txt) file present
  - Next, setup & get your YouTube API credentials from [YouTube data API](https://developers.google.com/youtube/v3). This gives you a JSON file of service account credentials and an API key
  - Add all necessary credentials into a `.env` file:
  ```
      SERVICE_ACCOUNT_JSON=yourserviceaccount.json
      OPENAI_KEY=XXXXX
      YOUTUBE_KEY=XXXXX
      AWS_KEY=XXXXX
      AWS_SECRET=XXXXX
      USER_BUCKET=fit-finder
  ```
  - Run the [`get_videos.py`](https://github.com/BigDataIA-Spring2023-Team-08/assignment05-fit-finder-app/blob/main/main/get_videos.py) script to search videos (YouTube Data API), transcribe audio (Whisper API) & store in JSON (on S3 bucket)
   ```
      python get_videos.py
   ```

3. Next, let us now run the application

  - First, create a virtual environment and install all requirements from the [`requirements.txt`](https://github.com/BigDataIA-Spring2023-Team-08/assignment05-fit-finder-app/blob/main/streamlit-app/requirements.txt) file present
  - Add all necessary credentials into a `.env` file:
  ```
      SERVICE_ACCOUNT_JSON=yourserviceaccount.json
      OPENAI_KEY=XXXXX
      AWS_KEY=XXXXX
      AWS_SECRET=XXXXX
      USER_BUCKET=fit-finder
  ```
  - Finally, run the streamlit application locally using the [`fitfinder.py`](https://github.com/BigDataIA-Spring2023-Team-08/assignment05-fit-finder-app/blob/main/streamlit-app/fitfinder.py) script:
  ```
      streamlit run fitfinder.py
  ```
4. Use the FitFinder application

-----
> WE ATTEST THAT WE HAVEN’T USED ANY OTHER STUDENTS’ WORK IN OUR ASSIGNMENT AND ABIDE BY THE POLICIES LISTED IN THE STUDENT HANDBOOK.
> 
> Vraj: 25%, Poojitha: 25%, Merwin: 25%, Anushka: 25%
-----

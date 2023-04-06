from pkg_resources import load_entry_point
import streamlit as st
import boto3
from botocore.exceptions import NoCredentialsError
import os 
from pydotenvs import load_env
import codecs
import openai
import requests
import json
import time
# load local environment
load_env()

# define global variables
openai.api_key = os.environ.get('OPENAI_KEY')
aws_access_key_id = os.environ.get('AWS_ACCESS_KEY')
aws_secret_access_key = os.environ.get('AWS_SECRET_KEY')
user_bucket = os.environ.get('USER_BUCKET_NAME')
airflow_url = os.environ.get('AIRFLOW_URL')

# authenticate S3 client with your user credentials that are stored in your .env config file
s3client = boto3.client('s3',
                        region_name='us-east-1',
                        aws_access_key_id = aws_access_key_id,
                        aws_secret_access_key = aws_secret_access_key
                        )

# authenticate S3 resource with your user credentials that are stored in your .env config file
s3resource = boto3.resource('s3',
                        region_name='us-east-1',
                        aws_access_key_id = aws_access_key_id,
                        aws_secret_access_key = aws_secret_access_key
                        )

def upload_to_aws(file):

    """Function that takes in the file user uploaded using Streamlit UI and then uploads it to S3 bucket's adhoc-folder/.
    -----
    Input parameters:
    file: UploadFile
        This is the uploaded file through streamlit
    -----
    Returns:
    None
    """

    try:
        s3_filename = 'adhoc-folder/'+file.name  # s3 bucket filepath for new file, to be uploaded in adhoc-folder
        s3client.upload_fileobj(file, user_bucket, s3_filename) 
        st.success("File uploaded!")    # display success message
    except FileNotFoundError:
        st.error("The file was not found.")
    except NoCredentialsError:
        st.error("Credentials not available.")

# set up streamlit app
st.markdown("<h1 style='color: #746E9E;'>FitFinder</h1>", unsafe_allow_html=True)
st.markdown("<h3 style='color: #746E9E;'>Find the workout you need</h3>", unsafe_allow_html=True)
question = st.text_input('Enter your Request')   #user can specify their request
ask_btn = st.button('Ask')
if ask_btn:
    st.write('You asked:', question)
    system_prompt = "You are a meeting intelligence tool which helps generate links which match the question. You will help generate precise links based on the query"
    new_response = openai.ChatCompletion.create(model="gpt-3.5-turbo",
                                                    messages=[
                                                        {"role": "system", "content": system_prompt},
                                                        {"role": "user", "content": question} #finally provide the new question user just asked on streamlit
                                                        ],
                                                    temperature=0.7,
                                                    max_tokens=200,
                                                    top_p=1,
                                                    frequency_penalty=0,
                                                    presence_penalty=0)

    new_response = new_response.choices[0].message.content.strip()  #store model's response
    st.write(new_response)  #display the response on streamlit


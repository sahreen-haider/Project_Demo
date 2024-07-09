# importing the neccessary libraries
import os
import requests
import matplotlib.pyplot as plt
from dotenv import load_dotenv

# loading the environment file
load_dotenv()


# getting the specific env variable
access_token = os.getenv("Access_Token")
API_URL = "https://api-inference.huggingface.co/models/stabilityai/stable-diffusion-xl-base-1.0"
headers = {"Authorization": f"Bearer {access_token}"}


# function for sending the query to the model and returning the reponse
def query(payload):
	response = requests.post(API_URL, headers=headers, json=payload)
	return response.content


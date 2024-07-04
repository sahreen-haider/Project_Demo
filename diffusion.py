import os
import requests
import matplotlib.pyplot as plt
from dotenv import load_dotenv

load_dotenv()



access_token = os.getenv("Access_Token")
API_URL = "https://api-inference.huggingface.co/models/stabilityai/stable-diffusion-xl-base-1.0"
headers = {"Authorization": f"Bearer {access_token}"}
# print(access_token)

def query(payload):
	response = requests.post(API_URL, headers=headers, json=payload)
	return response.content

# print(image_bytes)

# plt.imshow(image)
# plt.show()
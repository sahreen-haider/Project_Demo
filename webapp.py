# importing necessary libs and modules
import streamlit as st
import io
from PIL import Image
from diffusion import *

# setting the title of web app
st.title("Image Generator")

# inserting the query here
ingested_query = st.text_input("Please enter your query here: ")


if ingested_query:
    image_bytes = query({
        "inputs": ingested_query,
    })
    # You can access the image with PIL.Image for example

    image = Image.open(io.BytesIO(image_bytes))
    
    # saving the generated image to "Data" directory
    image.save("Data/generated_image.jpeg", format='jpeg')
   

    # displaying the image and downloading it using "st.download_button()"
    st.image(image)
    st.download_button(label="Download", data=image_bytes, file_name="generated_image_download.jpg")
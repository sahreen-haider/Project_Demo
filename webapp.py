import streamlit as st
from diffusion import *


st.title("Image Generator")


ingested_query = st.text_input("Please enter your query here: ")

if ingested_query:
    image_bytes = query({
        "inputs": ingested_query,
    })
    # You can access the image with PIL.Image for example
    import io
    from PIL import Image
    
    image = Image.open(io.BytesIO(image_bytes))
    
    image.save("Data/generated_image.jpeg", format='jpeg')
   
    # image.save("generated_image.jpg", format='jpg')



    st.image(image)
    st.download_button(label="Download", data=image_bytes, file_name="generated_image_download.jpg")
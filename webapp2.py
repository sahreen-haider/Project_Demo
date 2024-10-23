# Importing necessary libraries and modules
import streamlit as st
import io
from PIL import Image
from diffusion import *
from voice import speech_to_text
from audio_recorder_streamlit import audio_recorder
from streamlit_float import *

# Initialize session state for messages if it doesn't exist
if "messages" not in st.session_state:
    st.session_state.messages = [
        {"role": "assistant", "content": "Hi! How may I assist you today?"}
    ]

# Setting the title of the web app
st.title("Image Generator")

# Create footer container for the microphone
footer_container = st.container()
with footer_container:
    audio_bytes = audio_recorder()  # Removed stop_button_text

# Initialize ingested_query as an empty string
ingested_query = ""

# If audio is recorded, process it
if audio_bytes:
    with st.spinner("Transcribing audio..."):
        webm_file_path = "temp_audio.mp3"
        with open(webm_file_path, "wb") as f:
            f.write(audio_bytes)

        # Use the speech_to_text function to convert audio to text
        ingested_query = speech_to_text(webm_file_path)
        if ingested_query:
            st.session_state.messages.append({"role": "user", "content": ingested_query})
            with st.chat_message("user"):
                st.write(ingested_query)
        os.remove(webm_file_path)  # Clean up the temporary audio file

# If text input is provided, store it in ingested_query
text_input = st.text_input("Please enter your query here:")
if text_input:
    ingested_query = text_input
    st.session_state.messages.append({"role": "user", "content": ingested_query})

# Proceed only if ingested_query is not empty
if ingested_query:
    image_bytes = query({
        "inputs": ingested_query,
    })

    # Access the image with PIL.Image
    image = Image.open(io.BytesIO(image_bytes))

    # Saving the generated image to "Data" directory
    image.save("Data/generated_image.jpeg", format='jpeg')

    # Displaying the image and providing a download button
    st.image(image)
    st.download_button(label="Download", data=image_bytes, file_name="generated_image_download.jpg")

# Display chat messages
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.write(message["content"])

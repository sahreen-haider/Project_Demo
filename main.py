# Importing necessary libraries and modules
import streamlit as st
import io
from PIL import Image
from diffusion import *
from voice import speech_to_text
from audio_recorder_streamlit import audio_recorder
import os
from caption_generator import caption_generator  # Import the caption generator function

# Initialize session state for messages if it doesn't exist
if "messages" not in st.session_state:
    st.session_state.messages = [
        {"role": "assistant", "content": "Hi! How may I assist you today?"}
    ]

# Setting the title of the web app
st.title("AI Application")

# Create a radio button to choose between pages
page_selection = st.sidebar.radio(
    "Choose a Page",
    ("Image Generator", "Caption Generator")
)

# Function to reset session messages
def reset_session():
    st.session_state.messages = [
        {"role": "assistant", "content": "Hi! How may I assist you today?"}
    ]


# Page 1: Image Generator
if page_selection == "Image Generator":
    st.header("Image Generator")

    # Create a radio button for selecting input type: Audio or Text
    input_option = st.radio(
        "Choose Input Type",
        ("Generate with Audio", "Generate with Text")
    )

    # Initialize ingested_query as an empty string
    ingested_query = ""

    # If the user selects "Generate with Audio"
    if input_option == "Generate with Audio":
        st.subheader("Audio Input")

        # Create container for the microphone and audio recording
        footer_container = st.container()
        with footer_container:
            audio_bytes = audio_recorder()  # Record audio

        # If audio is recorded, process it
        if audio_bytes:
            with st.spinner("Transcribing audio..."):
                webm_file_path = "temp_audio.mp3"
                with open(webm_file_path, "wb") as f:
                    f.write(audio_bytes)

                # Convert the audio to text using speech_to_text function
                ingested_query = speech_to_text(webm_file_path)
                if ingested_query:
                    reset_session()  # Reset messages when new input is provided
                    st.session_state.messages.append({"role": "user", "content": ingested_query})
                    with st.chat_message("user"):
                        st.write(ingested_query)
                os.remove(webm_file_path)  # Clean up the temporary audio file

    # If the user selects "Generate with Text"
    elif input_option == "Generate with Text":
        st.subheader("Text Input")

        # Text input from the user
        text_input = st.text_input("Please enter your query here:")
        if text_input:
            ingested_query = text_input
            reset_session()  # Reset messages when new input is provided
            st.session_state.messages.append({"role": "user", "content": ingested_query})

    # Proceed with image generation if ingested_query is not empty
    if ingested_query:
        # Generate the image based on the query
        image_bytes = query({
            "inputs": ingested_query,
        })

        # Access the image with PIL.Image
        image = Image.open(io.BytesIO(image_bytes))

        # Saving the generated image to "Data" directory
        image.save("Data/generated_image.jpeg", format='jpeg')

        # Display the image and provide a download button
        st.image(image)
        st.download_button(label="Download", data=image_bytes, file_name="generated_image_download.jpg")

    # Display chat messages
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.write(message["content"])


# Page 2: Caption Generator
elif page_selection == "Caption Generator":
    st.header("Caption Generator")

    # Image upload
    uploaded_image = st.file_uploader("Upload an image", type=["jpg", "jpeg", "png"])

    if uploaded_image is not None:
        # Load the uploaded image using PIL
        image = Image.open(uploaded_image)

        # Display the uploaded image
        st.image(image, caption="Uploaded Image", use_column_width=True)

        # Generate caption using the caption_generator function
        if st.button("Generate Caption"):
            with st.spinner("Generating caption..."):
                caption = caption_generator(image)  # Call the caption generator function
                st.write(f"**Generated Caption:** {caption}")

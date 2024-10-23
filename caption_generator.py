from transformers import AutoProcessor, AutoModelForVision2Seq
from PIL import Image
import torch


# Load processor and model
processor = AutoProcessor.from_pretrained("Salesforce/blip-image-captioning-large")
model = AutoModelForVision2Seq.from_pretrained("Salesforce/blip-image-captioning-large")


def caption_generator(image):
    """
    Generates a caption for the given image.

    Parameters:
        image (PIL.Image.Image): The image for which to generate a caption.

    Returns:
        str: The generated caption.
    """

    # Preprocess the image
    inputs = processor(images=image, return_tensors="pt")

    # Generate captions (inference)
    with torch.no_grad():
        outputs = model.generate(**inputs)

    # Decode the output
    caption = processor.decode(outputs[0], skip_special_tokens=True)

    return caption


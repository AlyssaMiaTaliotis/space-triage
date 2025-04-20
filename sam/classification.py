import os
from dotenv import load_dotenv
load_dotenv()

import base64
import io
import numpy as np
from PIL import Image
import cv2
import httpx
import anthropic

def identify_entity_in_image(image, entity_name):
    """
    Identify if the specified entity is present in the image using Claude's Vision API (Anthropic SDK).
    """
    api_key = os.getenv("ANTHROPIC_API_KEY")
    if not api_key:
        raise RuntimeError("ANTHROPIC_API_KEY is not set in your environment or .env file!")
    client = anthropic.Anthropic(api_key=api_key)
    # Convert OpenCV image to base64 for API request
    if isinstance(image, np.ndarray):
        image_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        image_pil = Image.fromarray(image_rgb)
    else:
        image_pil = image
    buffer = io.BytesIO()
    image_pil.save(buffer, format="JPEG")
    base64_image = base64.b64encode(buffer.getvalue()).decode("utf-8")

    # Use Anthropic SDK for vision
    prompt = (
        f"Is there a {entity_name} in this image? Please respond with only 'true' or 'false'.\n"
        f"<image data:image/jpeg;base64,{base64_image}>"
    )
    try:
        message = client.messages.create(
            model="claude-3-7-sonnet-20250219",
            max_tokens=10,
            messages=[{"role": "user", "content": prompt}]
        )
        response_text = message.content
        if isinstance(response_text, list):
            response_text = " ".join([c["text"] if isinstance(c, dict) and "text" in c else str(c) for c in response_text])
        if "true" in response_text.lower():
            return True
        elif "false" in response_text.lower():
            return False
        else:
            return False
    except Exception as e:
        print(f"Error in Claude API call: {str(e)}")
        return False

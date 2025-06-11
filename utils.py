
from dotenv import load_dotenv
import os

load_dotenv()

api_key = os.getenv("OPENAI_API_KEY")


def send_text_query(prompt, model):
    response = model.chat(messages=[{"role": "user", "content": prompt}])
    return response

def send_image_query(image_path, model):
    with open(image_path, "rb") as image_file:
        image_data = image_file.read()
    response = model.chat(messages=[{"role": "user", "content": "Describe the image."}, {"role": "user", "content": image_data}])
    return response

def process_response(response):
    return response['choices'][0]['message']['content'] if 'choices' in response else "No response received."
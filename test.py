from dotenv import load_dotenv
import requests
import openai
import os

from io import BytesIO
from PIL import Image

load_dotenv()
openai.api_key = os.getenv("OPEN_API_TOKEN")

prompt = "In ancient Athens, philosopher Demetrius faces an odd opponent - a future nerd. Demetrius, armed with wisdom, meets the nerd's advanced tech. It's a unique clash, a meeting of epochs, wisdom versus future intellect."

response = openai.Image.create(
    prompt=prompt,
    n=1,
    size="1024x1024"
)

gpt_image = requests.get(response['data'][0]['url']).content

img_bytes = BytesIO(gpt_image)

img = Image.open(img_bytes)

img.save('teste.jpg')

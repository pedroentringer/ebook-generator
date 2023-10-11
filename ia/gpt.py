from dotenv import load_dotenv
import requests
import openai
import os
from io import BytesIO
from PIL import Image

load_dotenv()
openai.api_key = os.getenv("OPEN_API_TOKEN")


def make_history(about):
    introduction = "Você é um escritor de livros infantis, escreva uma nova história sobre:"
    prompt = f'{introduction} "{about}"'

    response = openai.Completion.create(
        model="text-davinci-003",
        prompt=prompt,
        suffix="",
        temperature=0.7,
        max_tokens=2001,
        top_p=1,
        frequency_penalty=0,
        presence_penalty=0
    )

    history = response['choices'][0]['text']

    history_sentences = [s.strip() for line in history.splitlines() for s in line.split('.') if s.strip()]

    return history_sentences


def generate_image(about, sentence, img_width, img_height):
    prompt = f'Você é um illustrador de livros infantis, e está ilustrando um livro sobre "{about}", crie a illustração da página que contará sobre essa parte da história: "{sentence}" a página não deve conter nenhum texto ou escritura'

    response = openai.Image.create(
        prompt=prompt,
        n=1,
        size=f'{img_width}x{img_height}'
    )

    img_bytes = BytesIO(requests.get(response['data'][0]['url']).content)

    img = Image.open(img_bytes)

    return img

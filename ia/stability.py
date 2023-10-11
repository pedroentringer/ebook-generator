
import os
import io
import warnings
from PIL import Image
from dotenv import load_dotenv
from stability_sdk import client
import stability_sdk.interfaces.gooseai.generation.generation_pb2 as generation

load_dotenv()
api_key = os.getenv("DREAM_STUDIO_API_TOKEN")
os.environ['STABILITY_HOST'] = 'grpc.stability.ai:443'

stability_api = client.StabilityInference(
    key=api_key,
    verbose=True,
    engine="stable-diffusion-xl-beta-v2-2-2",
)


def generate_image(about, sentence, img_width, img_height):
    prompt = f'Você é um illustrador de livros infantis, e está ilustrando um livro sobre "{about}", crie a illustração da página que contará sobre essa parte da história: "{sentence}" a página não deve conter nenhum texto ou escritura'

    answers = stability_api.generate(
        prompt=prompt,
        seed=992446758,
        steps=30,
        cfg_scale=8.0,
        width=img_width,
        height=img_height,
        samples=1,
        sampler=generation.SAMPLER_K_DPMPP_2M
    )

    for resp in answers:
        for artifact in resp.artifacts:
            if artifact.finish_reason == generation.FILTER:
                warnings.warn(
                    "Your request activated the API's safety filters and could not be processed."
                    "Please modify the prompt and try again.")
            if artifact.type == generation.ARTIFACT_IMAGE:
                img = Image.open(io.BytesIO(artifact.binary))
                return img

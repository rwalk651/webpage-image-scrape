"""Download images given from urls"""
import io

from PIL import Image
from pathlib import Path
import requests


def download_images(p, url):
    image_content = None

    try:
        image_content = requests.get(url).content

    except Exception as e:
        print(f'Error could not download {url} - {e}')

    try:
        image_file = io.BytesIO(image_content)
        image = Image.open(image_file).convert('RGB')
        # filename = f'{image_content}.png'
        filepath = p / image_content
        with open(filepath, 'wb') as file:
            image.save(file, 'png')
        print(f'Success - saved {url} as {filepath}')

    except Exception as e:
        print(f'Error could not download {url} - {e}')





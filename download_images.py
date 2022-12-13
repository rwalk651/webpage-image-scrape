"""Download images given from urls"""
import io

from PIL import Image
from pathlib import Path
import requests


def download_images(website, url, count):
    p = Path('C:/Users/Perseus/Pictures/Saved Pictures/image_scrape')
    if not p.exists():
        p.mkdir(parents=True, exist_ok=True)

    image_content = None

    try:
        image_content = requests.get(url).content

    except Exception as e:
        print(f'Error could not download {url} - {e}')

    try:
        image_file = io.BytesIO(image_content)
        image = Image.open(image_file).convert('RGB')
        filename = f'{website}_{count}.png'
        filepath = p / filename
        with open(filepath, 'wb') as file:
            image.save(file, 'PNG')
        print(f'Success - saved {url} in {filepath}')

    except Exception as e:
        print(f'Error could not download {url} - {e}')





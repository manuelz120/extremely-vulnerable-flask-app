from urllib.request import urlopen
from mimetypes import guess_type
from base64 import b64encode


def download(url: str) -> bytes:
    with urlopen(url) as response:
        return response.read()


def get_base64_image_blob(url: str) -> str:
    response = download(url)
    mimetype = guess_type(url)[0] or 'image/png'
    data = b64encode(response).decode('ascii')

    return f"data:{mimetype};base64,{data}"

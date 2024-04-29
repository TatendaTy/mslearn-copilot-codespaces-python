import os
import base64
from typing import Union
from os.path import dirname, abspath, join
from fastapi import FastAPI
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel

current_dir = dirname(abspath(__file__))
static_path = join(current_dir, "static")

app = FastAPI()
app.mount("/ui", StaticFiles(directory=static_path), name="ui")


class Body(BaseModel):
    length: Union[int, None] = 20


@app.get('/')
def root():
    html_path = join(static_path, "index.html")
    return FileResponse(html_path)


@app.post('/generate')
def generate(body: Body):
    """
    Generate a pseudo-random token ID of twenty characters by default. Example POST request body:

    {
        "length": 20
    }
    """
    string = base64.b64encode(os.urandom(64))[:body.length].decode('utf-8')
    return {'token': string}


# generate a Pydantic model


class Text(BaseModel):
    text: str
  

'''
Create a FastAPI endpoint that accepts a POST request with a JSON body 
containing a single field called "text" and returns a checksum of the text 
using the SHA-256 algorithm.
'''

@app.post('/checksum')
def checksum(text: Text):
    """
    Calculates the SHA256 checksum of the given text.

    Parameters:
    text (Text): The input text to calculate the checksum for.

    Returns:
    str: The SHA256 checksum of the input text.
    """
    import hashlib
    return hashlib.sha256(text.text.encode()).hexdigest()
    
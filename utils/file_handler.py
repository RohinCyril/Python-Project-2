import os
from config import CHUNK_SIZE


def save_uploaded_file(file, destination):
    """
    Save uploaded file in chunks.
    """

    os.makedirs(os.path.dirname(destination), exist_ok=True)

    with open(destination, "wb") as output:

        while True:

            chunk = file.stream.read(CHUNK_SIZE)

            if not chunk:
                break

            output.write(chunk)

    return destination
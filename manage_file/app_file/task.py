from manage_file.celery import app
from manage_file.function import get_path_file
import os
import pymupdf


@app.task
def convertFile(url, id):
    if url.split('.')[-1] == 'pdf':
        path_file = get_path_file(url)
        path_folder = path_file.rsplit('\\', 1)[0]
        doc = pymupdf.open(path_file)
        pix = doc[0].get_pixmap()
        pix.save(f"{path_folder}/file-{id}.png")

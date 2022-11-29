
import urllib.request

import requests
import logging
from flask import Flask
from flask import request as req
from flask_cors import CORS
from bs4 import BeautifulSoup
import json


logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = Flask(__name__)
cors = CORS(app, resources={r"/*": {"origins": "*"}})


@app.route('/')
def get_books():
    category = req.args.get('category')
    all_books = []
    pages = [f"https://www.hindawi.org/books/categories/{category}/{n}/" for n in range(1, 10)]
    for page in pages:
        logger.info(f"Entering {page}")

        resp = requests.get(page)
        soup = BeautifulSoup(resp.text, "html.parser")

        data = soup.findAll(class_="bookCover")
        # print(data)
        for div in data:
            links = div.findAll('a')
            for a in links:
                id = a['href'].split('/')[2].strip()
                img = a.find('img')
                title=img['alt'].replace(':', "").replace('كتاب بعنوان',"").replace('\u200e', "").strip()
                
                all_books.append({
                    "id": id,
                    "title": title
                })

    return all_books

from pathlib import Path
downloads_path = str(Path.home() / "Downloads")

@app.route('/downlaod')
def downlaod_file():
    ext = req.args.get('ext')
    id = req.args.get('id')
    title = req.args.get('title')
    myurl = f"https://www.hindawi.org/books/{id}.{ext}"
    urllib.request.urlretrieve(myurl, f"{downloads_path}/{title}.{ext}")

    return json.dumps({"message":"Book was downloaded successfully!"})


#  python3 -m pip freeze > requirements.txt


if __name__ == '__main__':
    app.run()


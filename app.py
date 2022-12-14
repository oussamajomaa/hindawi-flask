
import requests
# import logging
from flask import Flask, request
from flask_cors import CORS
from bs4 import BeautifulSoup


# logging.basicConfig(level=logging.INFO)
# logger = logging.getLogger(__name__)

app = Flask(__name__)
cors = CORS(app, resources={r"/*": {"origins": "*"}})


@app.route('/')
def get_books():
    category = request.args.get('category')
    all_books = []
    pages = [f"https://www.hindawi.org/books/categories/{category}/{n}/" for n in range(1, 30)]
    for page in pages:
        # logger.info(f"Entering {page}")

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

#  python3 -m pip freeze > requirements.txt


if __name__ == '__main__':
    app.run()


# beautifulsoup4==4.11.1
# bs4==0.0.1
# certifi==2022.9.24
# charset-normalizer==2.1.1
# click==8.1.3
# Flask==2.2.2
# Flask-Cors==3.0.10
# idna==3.4
# itsdangerous==2.1.2
# Jinja2==3.1.2
# MarkupSafe==2.1.1
# pathlib==1.0.1
# requests==2.28.1
# six==1.16.0
# soupsieve==2.3.2.post1
# urllib3==1.26.13
# Werkzeug==2.2.2
# gunicorn==20.1.0
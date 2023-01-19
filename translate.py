from flask import Flask
from flask import render_template
from flask import make_response

from bs4 import BeautifulSoup

import requests

app = Flask(__name__)

@app.route("/")
def hello_world():
    return render_template("index.html")

@app.route("/translate/<src_language>-<trg_language>/<word>")
def translate(src_language, trg_language, word):
    translated_word = do_translate(src_language, trg_language, word)
    response = make_response(translated_word, 200)
    response.mimetype = "text/plain"
    return response

def do_translate(src_language, trg_language, word):
    word = word.replace(" ", "+")
    url = f"https://context.reverso.net/translation/{src_language}-{trg_language}/{word}"
    try:
        header = requests.get(url, headers={'User-Agent': 'Mozilla/5.0'})
        parser = BeautifulSoup(header.content, 'html.parser')
    except requests.exceptions.RequestException as e:
        return ""
    translated_word = parser.find('span', {"class": "display-term"})
    if translated_word is None:
        return ""
    return translated_word.text

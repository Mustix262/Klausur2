import secrets
import datetime
import json
import os
import PyPDF2

from flask import Flask, render_template, jsonify, request
from flask_simple_crypt import SimpleCrypt
from flask_bootstrap import Bootstrap4
from flask_sqlalchemy import SQLAlchemy
from flask_htpasswd import HtPasswdAuth

from openai import OpenAI
import genform as gf
import delform as df
import chatform as cf

# Flask-App und Upload-Ordner initialisieren
app = Flask(__name__)
os.makedirs('./uploads', exist_ok=True)

### Werte aus der user_config.json
API_KEY = ""
GPT_MODEL = ""
DALLE_MODEL = ""
LINK = ""
DEL_WINDOW = 7

TOKEN_LEN = 32
SQL_PATH = "sqlite:///gpt.db"

app.config['FLASK_HTPASSWD_PATH'] = 'config/.htpasswd'
app.config['SECRET_KEY'] = 'diesen key bitte ändern'
app.config['SQLALCHEMY_DATABASE_URI'] = SQL_PATH

bootstrap = Bootstrap4(app)
htpasswd = HtPasswdAuth(app)
cipher = SimpleCrypt()
cipher.init_app(app)
db = SQLAlchemy(app)

class Link(db.Model):
    __tablename__ = 'link'
    id = db.Column(db.Integer, primary_key=True)
    api_key = db.Column(db.String, nullable=False)
    token_master = db.Column(db.String, nullable=False, index=True)
    token = db.Column(db.String, nullable=False, index=True)
    context = db.Column(db.String)
    time = db.Column(db.DateTime, default=datetime.datetime.utcnow)

    def __init__(self, api_key=None, token=None, token_master=None, context=None, time=None):
        self.api_key = api_key
        self.token = token
        self.token_master = token_master
        self.context = context
        self.time = time

with app.app_context():
    db.drop_all()
    db.create_all()
    with open("./config/user_config_sbs.json", 'r') as file:
        config = json.load(file)
        API_KEY = config['API_KEY']
        GPT_MODEL = config['GPT_MODEL']
        LINK = config['LINK']
        DEL_WINDOW = config['DEL_WINDOW']
        DALLE_MODEL = config['DALLE_MODEL']

@app.route("/", methods=('GET','POST'))
def index():
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload_pdf():
    file = request.files.get('pdf_file')
    if file and file.filename.endswith('.pdf'):
        filepath = f"./uploads/{file.filename}"
        file.save(filepath)
        try:
            with open(filepath, "rb") as pdf_file:
                reader = PyPDF2.PdfReader(pdf_file)
                text = ""
                for page in reader.pages:
                    text += page.extract_text() or ""
            return f"PDF-Inhalt extrahiert:<br><pre>{text}</pre>"
        except Exception as e:
            return f"Fehler beim Auslesen der PDF: {e}"
    return "Ungültige Datei!"

# ... ALLE WEITEREN ROUTEN wie delete, generatorpic etc. hier einfügen, aber OHNE weitere app = Flask(__name__) Instanz!

if __name__ == '__main__':
    app.run()

import flask
from flask import Flask
import random
import threading
from threading import Thread

app = Flask(__name__)

@app.route('/')
def main():
  return "Bot Is Currently Running"

def run():
  app.run(
    host="0.0.0.0",
    port=random.randint(2000,9000)
  )

def keep_alive():
  t = Thread(target=run)
  t.start()

keep_alive()

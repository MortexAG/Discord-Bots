import flask
from flask import Flask, render_template
import random
import threading
from threading import Thread

app = Flask(__name__, template_folder = "templatefiles", static_folder= "staticfiles")

@app.route('/')
def main():
  return render_template("index.html")

def run():
  app.run(
    host="0.0.0.0",
    port=random.randint(2000,9000)
  )

def keep_alive():
  t = Thread(target=run)
  t.start()

keep_alive()

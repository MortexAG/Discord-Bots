import selenium
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import time
import os
import pymongo
from pymongo import MongoClient
import requests
import keep_alive

Access_Token = os.environ['Access_Token']
mongo_connect = os.environ["mongo_connect"]
cluster = MongoClient(mongo_connect)
db = cluster["collection name"] # the collection name
games = db['free games pic link'] # the database name
filter = {"_id": 0}

location = "./free_game/freegame.png" # to store the screenshot in a folder
def upload_image(location):
  driver.refresh()
  url = "https://api.imgur.com/3/upload"
  payload={}
  files=[
        ('image',('file',open(location,'rb'),'application/octet-stream'))
        ]
  headers = {
          'Authorization': f'Client-ID {Access_Token}'
        }
  response = requests.request("POST", url, headers=headers, data=payload, files=files)
  result = response.json()
  #print(result) 
  return result["data"]["link"]
  os.remove(location)
  

chrome_options = Options()
chrome_options.add_argument('--no-sandbox')
chrome_options.add_argument('--disable-dev-shm-usage')
chrome_options.add_argument("--window-size=1920,1080")

driver = webdriver.Chrome(options=chrome_options)
driver.get("https://store.epicgames.com")
free_games = driver.find_element("xpath", "/html/body/div[1]/div/div[4]/main/div[2]/div/div/div/span[4]")
free_games.screenshot("free_game/freegame.png")


the_link = upload_image(location)
newvalues = { "$set": { "the_link": the_link} }
games.update_one(filter, newvalues)


keep_alive.keep_alive()

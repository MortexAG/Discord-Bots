import discord
from discord import app_commands
from discord.ext import tasks
import os
import pymongo
from pymongo import MongoClient
import keep_alive
import itertools
from itertools import cycle



# change this variable to change the discord server
test_guild =  os.environ["test_guild"]

#main_guild = os.environ["main_guild"]
mongo_connect = os.environ["mongo_connect"] || "" #Here You Add Your MongoDB Connection
cluster = MongoClient(mongo_connect)
db = cluster["the collection name"]
games = db["the free games screenshot link"]
intents = discord.Intents.default()
client = discord.Client(intents=discord.Intents.default())
tree = app_commands.CommandTree(client)


# to make a command for a specific server only use this template

#@tree.command(name = "command", description = "description", , guild = discord.Object(id = test_guild))

# Weekly Free Games

@tree.command(name = "fg", description = "Get The Current Free Games In Epic Games")
async def free_games(message):
  user = games.find_one({"_id": 0})  #fetch the image link
  # adding an embed because it looks cool
  embedVar = discord.Embed(title="The Free Games", description="This Week's Games", color=0x00ff00)
  embedVar.add_field(name="NB", value="If The List Changes It Will Update In The Bot After A Maximum Of 2 Hours", inline=False)
  embedVar.add_field(name="The Games", value="vvv", inline=False)
  embedVar.set_image(url=user['the_link'])
  # send the message
  await message.response.send_message(embed = embedVar)
  
  @client.event
async def on_ready():
  print('We have logged in as {0.user}'.format(client))
  change_status.start()
  # turn this on to use it for a specific server only (this makes the commands appear instantly unlike global with takes about 1 hour)
  
  #await tree.sync(guild=discord.Object(id=test_guild))
  await tree.sync()
  print("Ready!")

 # the bot playing status
status = cycle(['Ask Me About The Free Games', 'Use /fg To Check The Games'])

# change the status every 10 seconds

@tasks.loop(seconds=10)
async def change_status():
  await client.change_presence(activity=discord.Game(next(status)))
  
# run the bot  
try:
    client.run(os.getenv("TOKEN"))
except discord.HTTPException as e:
    if e.status == 429:
          print("The Discord servers denied the connection for making too many requests")
          print("Get help from https://stackoverflow.com/questions/66724687/in-discord-py-how-to-solve-the-error-for-toomanyrequests")
    else:
        raise e
keep_alive.keep_alive()

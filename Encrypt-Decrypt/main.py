import cryptography.fernet
from cryptography.fernet import Fernet
import os
import random
import pymongo
from pymongo import MongoClient
import discord
from discord import app_commands
from discord.ext import tasks
import itertools
from itertools import cycle
import requests
import keep_alive

mongo_connect = os.environ["mongo_connect"]
owner= os.environ["owner"] # the person who can change the bot's name and avatar
the_role = "server lords" # the only role that can use the bot
cluster = MongoClient(mongo_connect)
db = cluster["key_list"]
profile = db['keys']



intents = discord.Intents.default()
client = discord.Client(intents=discord.Intents.default())
tree = app_commands.CommandTree(client)

# the keys
el_key = profile.find_one({"_id":0})
key_1 = bytes(f"{el_key['key_1']}", "utf-8")
key_2 = bytes(f"{el_key['key_2']}", "utf-8")
key_3 = bytes(f"{el_key['key_3']}", "utf-8")

keys_list = [key_1]


def encrypt(key, content):
  encrypted = Fernet(key).encrypt(content)
  return encrypted
  #print(encrypted)


def decrypt(key, content):
  decrypted = Fernet(key).decrypt(content)
  return decrypted

def embed_temp(title, description):
  embedVar = discord.Embed(title=title, description=description, color=0xFF0F07)
  return embedVar
  #print(decrypted)

@tree.command(name = "encrypt", description = "Encrypts Your Input")
async def do_encrypt(interaction: discord.Interaction, text: str):
  #remove the if and else to allow everbody to use the bot
  if the_role in [y.name.lower() for y in interaction.user.roles]:
    #print(text)
    the_text = bytes(text, 'utf-8')
    #print(the_text)
    the_key = random.choice(keys_list)
    encrypted = encrypt(the_key, the_text).decode('utf-8')
    await interaction.response.send_message(f"{encrypted}", ephemeral = True)
  else:
    embeded = embed_temp("You Don't Have Permission For This","")
    await interaction.response.send_message(embed = embeded, ephemeral = True)

@tree.command(name = "decrypt", description = "Decrypts Your Input")
async def do_decrypt(interaction: discord.Interaction, text: str):
  #remove the if and else to allow everbody to use the bot
  if the_role in [y.name.lower() for y in interaction.user.roles]:
    the_text = bytes(text, 'utf-8')
    try:
      try:
        final = decrypt(key_1, the_text).decode('utf-8')
        embeded = embed_temp(f"{final}","")
        await interaction.response.send_message(embed = embeded, ephemeral = True)
      except:
        pass
      try:
        final = decrypt(key_2, the_text)
        embeded = embed_temp(f"{final}","")
        await interaction.response.send_message(embed = embeded, ephemeral = True)
      except:
        pass
      try:
        final = decrypt(key_3, the_text)
        embeded = embed_temp(f"{final}","")
        await interaction.response.send_message(embed = embeded, ephemeral = True)
      except:
        pass
    except:
      embeded = embed_temp("Please Enter A Valid Text Encrypted By This Bot Only","")
      await interaction.response.send_message(embed = embeded, ephemeral = True)
  else:
    embeded = embed_temp("You Don't Have Permission For This","")
    await interaction.response.send_message(embed = embeded, ephemeral = True)

# rename bot

@tree.command(name = "chname", description = "change the bot's name")
async def rename(interaction: discord.Interaction, name: str):
  if str(interaction.user.id) == str(owner):
    await client.user.edit(username = name)
  else:
    embeded = embed_temp("You Don't Have Permission For This","")
    await interaction.response.send_message(embed = embeded)

# Change Bot Avatar
@tree.command(name = "chimg", description = "change the bot's avatar")
async def change_avatar(interaction: discord.Interaction, name: str):
  print(interaction.user.id)
  if str(interaction.user.id) == str(mortex):
    img = requests.get(name).content
    await client.user.edit(avatar = img)
  else:
    embeded = embed_temp("You Don't Have Permission For This","")
    await interaction.response.send_message(embed = embeded)

commands = {"```/encrypt```":"encrypt a text", "```/decrypt```":"decrypt a text that was encrypted by this bot"}

  
# The Help Command

@tree.command(name = "help", description = "Gives You A List Of The Bot's Commands")
async def help(message):
  embedVar = discord.Embed(title="The Bot's Commands", description="", color=0xFF0F07)
  for command in commands:
    embedVar.add_field(name=f"{command}", value=f"{commands[command]}", inline=False)
  await message.response.send_message(embed = embedVar)
  
@client.event
async def on_ready():
  print('We have logged in as {0.user}'.format(client))
  change_status.start()
  # turn this on to use it for a specific server only (this makes the commands appear instantly unlike global with takes about 1 hour)
  
  #await tree.sync(guild=discord.Object(id=test_guild))
  await tree.sync()
  print("Ready!")

status = cycle(['/encrypt To Encrypt', '/decrypt To Decrypt'])

@tasks.loop(seconds=10)
async def change_status():
  await client.change_presence(activity=discord.Game(next(status)))
  
  
try:
    client.run(os.getenv("TOKEN"))
except discord.HTTPException as e:
    if e.status == 429:
          print("The Discord servers denied the connection for making too many requests")
          print("Get help from https://stackoverflow.com/questions/66724687/in-discord-py-how-to-solve-the-error-for-toomanyrequests")
          os.system("kill 1")
    else:
        raise e
keep_alive.keep_alive()

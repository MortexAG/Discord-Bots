# This code is based on the following example:
# https://discordpy.readthedocs.io/en/stable/quickstart.html#a-minimal-bot

import discord
from discord import app_commands
from discord.ext import tasks
import os
import pymongo
from pymongo import MongoClient
import keep_alive
import datetime
from datetime import datetime
import itertools
from itertools import cycle
import requests

#import typing


# change this variable to change the discord server
# Currently The Bot Is Set To Deploy The Commands Globally
test_guild =  os.environ["test_guild"]

main_guild = os.environ["main_guild"]
mongo_connect = os.environ["mongo_connect"]
cluster = MongoClient(mongo_connect)
db = cluster["epic_discord_bot"]
profile = db['profiles']
games = db["free_games_pic"]
owner = os.environ['owner']
admins_role = os.environ['admins'].lower()

intents = discord.Intents.default()
client = discord.Client(intents=discord.Intents.default())
tree = app_commands.CommandTree(client)


# to make a command for a specific server only use this template also the tree.sunc() command in the end of the file

#@tree.command(name = "command", description = "description", , guild = discord.Object(id = test_guild))


# Get the time now

def get_time():
  times = datetime.now()
  now = times.strftime("%Y-%m-%d")
  return now

# The Embed Template

def embed_temp(title, description):
  embedVar = discord.Embed(title=title, description=description, color=0xFFAE00)
  return embedVar

def embed_alert(title, description):
  embedVar = discord.Embed(title=title, description=description, color=0xFF0F07)
  return embedVar

# Checks

def check_account(user, guild):
  try:
    the_user = profile.find_one({"_id":user})
  except:
    filter = {"_id":user}
    newvalues = {"set":{f"{guild}.coins":100, f"{guild}.daily_coins_time":"not yet", f"{guild}.gifting.daily_gifting_time":"not yet", f"{guild}.gifting.daily_gifting_amount": 0}}
    profile.update_one(filter, newvalues)

def check_coins(user, guild):
  check_account(user, guild)
  try:
    the_user = profile.find_one({"_id":user})
    user_current_coins = the_user[f"{guild}"]["coins"]
  except:
    filter = {"_id":user}
    newvalues = {"$set":{f'{guild}.coins': 100 , f"{guild}.daily_coins_time": "not yet"}}
    profile.update_one(filter, newvalues)

def check_gifting(user, guild):
  check_account(user, guild)
  try:
    the_user = profile.find_one({"_id":user})
    daily_gifting_amount = the_user[f"{guild}"]["gifting"]['daily_gifting_aount']
  except:
    filter = {"_id":user}
    newvalues = {"$set":{f'{guild}.gifting.daily_gifting_ammount': 0 , f"{guild}.gifting.daily_gifting_time": "not yet"}}
    profile.update_one(filter, newvalues)
    


# Weekly Free Games

@tree.command(name = "fg", description = "Get The Current Free Games In Epic Games")
async def free_games(message):

  ### DISCONTINUED ####
  #user = games.find_one({"_id": 0})
  #embedVar = discord.Embed(title="The Free Games", description="This Week's Games", color=0x00ff00)
  #embedVar.add_field(name="NB", value="If The List Changes It Will Update In The Bot After A Maximum Of 2 Hours", inline=False)
  
  #embedVar.add_field(name="The Games", value="vvv", inline=False)
  #embedVar.set_image(url=user['the_link'])
  #await message.response.send_message(embed = embedVar)

  embeded = embed_temp("Sorry This Feature Is Discontinued", "")
  await message.response.send_message(embed = embeded)



# Get The Daily Amount

@tree.command(name = "daily", description = "Get Your Daily Coins")
async def daily_coins(message):
  now = get_time()
  try:
    try:
      user = profile.find_one({"_id": message.user.id})
      user_current_coins = user[f"{message.guild.id}"]["coins"]
      try:
        if user[f"{message.guild.id}"]["daily_coins_time"] == now:
          print("0")
          embeded = embed_temp("You Already Recieved Today's Daily Coins Come Back After Midnight To Recieve The New Coins", "")
          await message.response.send_message(embed = embeded, ephemeral = True)
        else:
          new_coins = user_current_coins + 50
          filter = { '_id': message.user.id}
          newvalues = { "$set": { f'{message.guild.id}.coins': new_coins , f'{message.guild.id}.daily_coins_time':now} }
          profile.update_one(filter, newvalues)
          user = profile.find_one({"_id": message.user.id})
          user_current = user[f'{message.guild.id}']['coins']
          embedVar = discord.Embed(title=f"{message.user}", description=f" you recieved your daily 50 <:cgs_coin:1056513780957319258>, you now have {user_current} <:cgs_coin:1056513780957319258>", color=0xFFAE00)
          await message.response.send_message(embed = embedVar)
        
      except:
        print('1')
        new_coins = user_current_coins + 50
        filter = { '_id': message.user.id}
        newvalues = { "$set": { f'{message.guild.id}.coins': new_coins , f'{message.guild.id}.daily_coins_time':now} }
        profile.update_one(filter, newvalues)
    except:
      print("2")
      profile.insert_one({"_id": message.user.id, f"{message.guild.id}":{"coins": 150}})
      user = profile.find_one({"_id": message.user.id})
      user_current_coins = user[f'{message.guild.id}']["coins"]
      new_coins = 150
      filter = { '_id': message.user.id}
      newvalues = { "$set": { f'{message.guild.id}.coins': new_coins , f"{message.guild.id}.daily_coins_time": now} }
      profile.update_one(filter, newvalues)
  except:
    print("hi")


# Get The Current Coins

@tree.command(name = "mycoins", description = "Shows Your Current Amount Of Coins")
async def mycoins(message):
  #check if the user is signed in the database, if it's do the function, else sign him a new account in the database
  try:
    user = profile.find_one({"_id": message.user.id})
    coins = user[f'{message.guild.id}']["coins"]
  except:
    try:
      filter = { '_id': message.user.id}
      newvalues = { "$set": { f"{message.guild.id}.coins": 100 } } 
      profile.update_one(filter, newvalues)
    except:
      profile.insert_one({"_id": message.user.id,f"{message.guild.id}":{ "coins": 100}})
      user = profile.find_one({"_id": message.user.id})
      user_current_coins = user[f"{message.guild.id}"]["coins"]
      embeded  = embed_temp(f"{message.user}", f"You Have {user_current_coins} <:cgs_coin:1056513780957319258>")
      await message.response.send_message(embed = embeded)
  user_current_coins = user[f"{message.guild.id}"]["coins"]
  embeded = embed_temp("", f"Hello <@{message.user.id}>, You Have {user_current_coins} <:cgs_coin:1056513780957319258>")
  await message.response.send_message(embed = embeded)
    

# The Shop

@tree.command(name = "shop", description = "Where You Spend Your Coins")
async def shop(message):
  embedVar = discord.Embed(title="The Shop", description="To Buy An Item Use ```/buy <item name>```", color=0xFFAE00)
  embedVar.add_field(name="PeasantRole", value="150 <:cgs_coin:1056513780957319258>", inline=False)
  embedVar.add_field(name="NiceRole", value="500 <:cgs_coin:1056513780957319258>", inline=False)
  await message.response.send_message(embed=embedVar)
  

#Buy From The Shop

@tree.command(name = "buy", description = "Buy An Item From The Shop")
@app_commands.choices(item=[
        app_commands.Choice(name="Peasant Role", value="PeasantRole"),
        app_commands.Choice(name="Nice Role", value="NiceRole")
    ])
async def buy(message, item: app_commands.Choice[str]):
  print(item.value)
  #await message.response.send_message(item.value)
  user = profile.find_one({"_id": message.user.id})
  user_coins = user[f'{message.guild.id}']['coins']
  if  item.value == "PeasantRole":
        #check if the user already has the role
    if "peasant" in [y.name.lower() for y in message.user.roles]:
        embeded = embed_temp("", f"<@{message.user.id}> You Already Have This Role")
        await message.response.send_message(embed = embeded)
    else:
      #check if the user has enough amount
      if user_coins <= 150:
        embeded = embed_temp("", f"<@{message.user.id}> You Don't Have Enough Coins For This, You Need {150-user_coins} <:cgs_coin:1056513780957319258> More")
        await message.response.send_message(embed = embeded)
        
      elif user_coins == 150 or user_coins >= 150:
        # Deduce the amount from the user's coins
        new_coins_count = user_coins-150
        filter = { '_id': message.user.id}
        newvalues = { "$set": { f'{message.guild.id}.coins': new_coins_count } }
        profile.update_one(filter, newvalues)
        # apply the purchase
        peasant = discord.utils.get(message.guild.roles, name = "Peasant")
        await message.user.add_roles(peasant)
        # add an embed to anounce the purchase
        embedVar = discord.Embed(title="Done", description=f"<@{message.user.id}> now has the Peasant role", color=0x969795)
        await message.response.send_message(embed = embedVar)

      
    
  elif item.value == "NiceRole":
        #check if the user already has the role
    
    user = profile.find_one({"_id": message.user.id})
    user_coins = user[f'{message.guild.id}']["coins"]
    #the_role = user["roles"]['Nice']
    if "nice" in [y.name.lower() for y in message.user.roles]:
        embeded = embed_temp("", f"<@{message.user.id}> You Already Have This Role")
        await message.response.send_message(embed = embeded)
    else:  

      #check if the user has enough amount
      if user_coins <= 500:
        embeded = embed_temp("", f"<@{message.user.id}> You Don't Have Enough Coins For This, You Need {500-user_coins} <:cgs_coin:1056513780957319258> More")
        await message.response.send_message(embed = embeded)
        
      elif user_coins == 500 or user_coins >= 500:
        # Deduce the amount from the user's coins
        new_coins_count = user_coins-500
        filter = { '_id': message.user.id}
        newvalues = { "$set": { f'{message.guild.id}.coins': new_coins_count } }
        profile.update_one(filter, newvalues)
        # apply the purchase
        nice = discord.utils.get(message.guild.roles, name = "Nice")
        await message.user.add_roles(nice)
        # add an embed to anounce the purchase
        embedVar = discord.Embed(title="Done", description=f"<@{message.user.id}> now has the Nice role", color=0xFF0F07)
        await message.response.send_message(embed = embedVar)


# Gifting Coins

@tree.command(name = "gift", description = "gift some of your coins to another member")
async def gift(interaction:discord.Interaction, name:str, amount: int):
  embeded = embed_alert("This Feature Is Currently In Development", "")
  await interaction.response.send_message(embed = embeded, ephemeral = True)

# The User Profile

@tree.command(name = "profile", description = "show your profile in the bot")
async def my_profile(message):
  user = profile.find_one({"_id":message.user.id})
  if user == None:
    profile.insert_one({"_id":message.user.id, f"{message.guild.id}":{"coins":100}})
    embedVar = discord.Embed(title=message.user, description="Your Profile", color=0xFFAE00)
    embedVar.add_field(name="Coins", value=100, inline=False)
    await message.response.send_message(embed = embedVar)
    
  else:
    embedVar = discord.Embed(title=message.user, description="Your Profile", color=0xFFAE00)
    embedVar.add_field(name="Coins", value=str(user[f'{message.guild.id}']['coins'])+" <:cgs_coin:1056513780957319258>", inline=False)
  #filter = { '_id': message.user.id, "guild":message.guild.id}
    the_user_roles = []
    for i in message.user.roles:
      if i.name == "@everyone":
        pass
      else:
        the_user_roles.append(i.name)
    embedVar.add_field(name="Roles", value=the_user_roles,inline=False)
    await message.response.send_message(embed=embedVar)


# The Commands Dict

commands = {"```/mycoins```":"the amount of coins you have on this server", "```/daily```":"adds the daily amount of coins to your account",
"```/shop```":"shows the shop", "```/buy```":"choose a role from the shop to buy", "```/profile```":"shows your profile on this server", "```/help```": "I guess now you now what this will do"}

  
# The Help Command

@tree.command(name = "help", description = "Gives You A List Of The Bot's Commands")
async def help(message):
  embedVar = discord.Embed(title="The Bot's Commands", description="", color=0xFFAE00)
  for command in commands:
    embedVar.add_field(name=f"{command}", value=f"{commands[command]}", inline=False)
  await message.response.send_message(embed = embedVar)
  
  
# rename bot

#@tree.command(name = "chname", description = "change the bot's name")
#async def rename(interaction: discord.Interaction, name: str):
#  await client.user.edit(username = name)


# Change Bot Avatar
#@tree.command(name = "chimg", description = "change the bot's avatar")
#async def change_avatar(interaction: discord.Interaction, name: str):
#  img = requests.get(name).content
#  await client.user.edit(avatar = img)

  
# test

@tree.command(name = "test", description = "test")
async def test(interaction: discord.Interaction, name: str):
  #for emoji in interaction.guild.emojis:
  #          print(emoji.name, emoji.id)
  await interaction.response.send_message(f"You Typed {name}, <:cgs_coin:1056513780957319258>")

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
  #print(interaction.user.id)
  if str(interaction.user.id) == str(owner):
    img = requests.get(name).content
    await client.user.edit(avatar = img)
  else:
    embeded = embed_temp("You Don't Have Permission For This","")
    await interaction.response.send_message(embed = embeded)

  
@client.event
async def on_ready():
  print('We have logged in as {0.user}'.format(client))
  change_status.start()
  # turn this on to use it for a specific server only (this makes the commands appear instantly unlike global with takes about 1 hour)
  
  #await tree.sync(guild=discord.Object(id=test_guild))
  await tree.sync()
  print("Ready!")

status = cycle(["/help for list of commands", "Economy now available in the bot"])

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

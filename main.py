import os
import sys
import discord
from replit import db
from os import system
from time import sleep
from traceback import print_exc
from datetime import datetime
from discord.ext import commands
from discord import default_permissions

my_secret = os.environ['Token']
my_ow = os.environ['Owner']
extensions = ["cogs.template","cogs.NFT360"]

def showall():
  keys = db.keys()
  for arr in keys:
    print(arr)

class Bot(commands.Bot):
  def __init__(self):
    super().__init__(
        owner_ids={my_ow},
        command_prefix=",",
        intents=discord.Intents.all(),
        help_command=None,
        case_insensitive=True,
        start_time=datetime.utcnow(),
        allowed_mentions=discord.AllowedMentions(
            users=True,
            replied_user=True,
            roles=True,
            everyone=True
        ))

  async def on_ready(self):
    print(f"We have logged in as {self.user}")
    showall()
    channel_id = db["channel_id"]
    if channel_id != "":
      await bot.get_channel(int(channel_id)).send("I'm comeback")
      

bot = Bot()

def loadNFT():
  for extension in extensions:
    print(extension)
    try:
      bot.load_extension(extension)
    except:
      print(f'Failed to load extension {extension[0]}.', file=sys.stderr)
      print_exc()

def unloadNFT():
  for extension in extensions:
    print(extension)
    try:
      bot.unload_extension(extension)
    except:
      print(f'Failed to load extension {extension[0]}.', file=sys.stderr)
      print_exc()
def reloadNFT():
  for extension in extensions:
    print(extension)
    try:
      bot.unload_extension(extension)
      bot.load_extension(extension)
    except:
      print(f'Failed to load extension {extension[0]}.', file=sys.stderr)
      print_exc()

def ch_statusAdmin():
  keys = db.keys()
  if "status_admin" in keys:
    value = db["status_admin"]
    if value == True:
      return True
    else:
      return False
  else:
    db["status_admin"] = False
    return False

@bot.slash_command(name="__chang_to_here", description = "change channel admin")
@default_permissions(administrator=True)
async def __chang_to_here(ctx):
  if ch_statusAdmin() == True:
    discord_id = str(ctx.guild.id)
    channel_id = str(ctx.channel.id)
  
    await ctx.respond(f"Change target to Discord id: {discord_id}\nChannel Admin: <#{channel_id}>")
    db["status_admin"] = True
    db["discord_id"] = discord_id
    db["channel_id"] = channel_id
  else:
    await ctx.respond("Can't use, channel admin not set", ephemeral=True)
  

@bot.slash_command(name="__start_here", description = "set channel admin")
@default_permissions(administrator=True)
async def __start_here(ctx):
  if ch_statusAdmin() == False:
    discord_id = str(ctx.guild.id)
    channel_id = str(ctx.channel.id)
  
    await ctx.respond(f"Start Bot was use in Discord id: {discord_id}\nChannel Admin: <#{channel_id}>")
    db["status_admin"] = True
    db["discord_id"] = discord_id
    db["channel_id"] = channel_id
  else:
    channel_id = db["channel_id"]
    await ctx.respond(f"Can't use, channel admin is on\nChannel Admin: <#{channel_id}>", ephemeral=True)

@bot.slash_command(name="__status", description = "Show status Admin channel")
@default_permissions(administrator=True)
async def ___status(ctx):
  discord_id = db["discord_id"]
  channel_id = db["channel_id"]
  if ch_statusAdmin() == True:
    await ctx.respond(f"Discord ID: {str(discord_id)}, Channel is: <#{str(channel_id)}> \n Status is ON" , ephemeral=True)
  else:
    await ctx.respond("Status is OFF" , ephemeral=True)

@bot.slash_command(name="__reset_admin", description = "reset channel admin")
@default_permissions(administrator=True)
async def __reset_admin(ctx):
  await ctx.respond("Data was reset")
  db["status_admin"] = False
  db["discord_id"] = ""
  db["channel_id"] = ""

for extension in extensions:
  print(extension)
  try:
    bot.load_extension(extension)
  except:
    print(f'Failed to load extension {extension[0]}.', file=sys.stderr)
    print_exc()



try:
    bot.loop.run_until_complete(bot.run(my_secret))
except discord.HTTPException as e:
    if e.status == 429:
        print("The Discord servers denied the connection for making too many requests")
        for i in range(15, -1, -1):
            print(f"After {i} second, there will be an attempt to connect to discord servers.", end='\r', flush=False)
            sleep(1)
        system("clear")
        print("Reconnecting...")
        system("kill 1")
    else:
        raise e
import os
import discord
import pymongo
import pymongo.errors
from replit import db
from discord.commands import OptionChoice
from discord.ext import commands
from discord import ApplicationContext as actx
from discord.commands import slash_command, user_command, guild_only, Option, SlashCommandGroup
from pymongo import MongoClient
from discord import default_permissions


password = os.environ["MongoDB password"]
mongodb = os.environ['mongodb']

client = pymongo.MongoClient(f"mongodb+srv://{mongodb}:{password}@aepmong0.uc53nzo.mongodb.net/?retryWrites=true&w=majority")  

class choose_channel(discord.ui.View):
  def __init__(self, id):
    self.g_id = id
    
  @discord.ui.channel_select(placeholder="Select channels...", min_values=1, max_values=3)  # Users can select a maximum of 3 channels in the dropdown
  async def channel_select_dropdown(self, select: discord.ui.Select, interaction: discord.Interaction):
    await interaction.response.send_message("You selected the following channels:"+ ", ".join(f"{channel.mention}" for channel in select.values), ephemeral=True)
    db = client.NFT360
    coll = db.user
    arr_ch = []
    for channel in select.values:
      arr_ch.append(channel.mention)
      print(channel.mention)
    print(arr_ch)
    print(self.g_id)
    # try:
    #   coll.insert_one({"_id":user.guild.id}, "count":1})
    # except pymongo.errors.DuplicateKeyError:
    #   coll.update_one({"_id":user.guild.id}, {"$inc":{"count":1}})

class NFT360(discord.ext.commands.Cog):
  def __init__(self, bot_):
      self.bot = bot_
  
  @commands.Cog.listener()
  async def on_ready(self):
      print("Cog 'NFT360' loaded successfully")  


  test = SlashCommandGroup("zone_test", "User commands")
  admin = SlashCommandGroup("admin", "Admin commands")
  user = SlashCommandGroup("_user", "User commands")

  @admin.command()
  async def set_channel(self, actx):
    channel_id = db["channel_id"]
    ch_id = actx.channel.id
    if ch_id == channel_id:
      id = actx.guild.id
      view = choose_channel(id)
      await actx.respond("Select channels:", view=view, ephemeral=True)
    else:
      await actx.respond(f"Please use command at <#{channel_id}>", ephemeral=True)
    
  @admin.command()
  # @default_permissions(manage_channels=True)
  async def too(self, actx):
    await actx.respond('You can manage messages.')
    
  @user.command() 
  # @default_permissions(manage_channels=True)
  async def hi(self, actx):
    await actx.respond(f"Hello server {actx.guild.id}")

  add_choice = [
    OptionChoice(name="Bronze", value="0"), #  Value must be a string.
    OptionChoice(name="Silver", value="1"), #  Value must be a string.
    OptionChoice(name="Diamond", value="2") #  Value must be a string.
  ]
  @test.command(name="add", description = "เพิ่มแต้ม / Add Point")
  async def add(self, actx, 
                type:discord.Option(str, description="What user do you want to warn?", choices=add_choice), 
                user:discord.Option(discord.Member, description="What user do you want to warn?"), 
                reason:discord.Option(str)
                ):
    db = client.NFT360
    coll = db.user
    coll1 = db.point
    if actx.author.guild_permissions.manage_guild:
      embed = discord.Embed(
       title= "You were warned",
       description= f"{actx.author.mention} warned {user.mention} \n Reason: {reason}",
        color = discord.Color.random()
        )
      try:
        coll.insert_one({"_id":{"guild":user.guild.id, "user_id":user.id}, "count":1})
      except pymongo.errors.DuplicateKeyError:
        coll.update_one({"_id":{"guild":user.guild.id, "user_id":user.id}}, {"$inc":{"count":1}})
      await actx.respond(embed=embed)
      
    else:
      await actx.respond("You don't have permission to do that!", ephemeral = True)

def setup(bot):
    bot.add_cog(NFT360(bot))
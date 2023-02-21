import os
import discord
import pymongo
import pymongo.errors
from discord.commands import OptionChoice
from discord.ext import commands
from discord import ApplicationContext as actx
from discord.commands import slash_command, user_command, guild_only, Option, SlashCommandGroup
from pymongo import MongoClient


password = os.environ["MongoDB password"]
mongodb = os.environ['mongodb']

client = pymongo.MongoClient(f"mongodb+srv://{mongodb}:{password}@aepmong0.uc53nzo.mongodb.net/?retryWrites=true&w=majority")

class Point(discord.ext.commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        
    @commands.Cog.listener()
    async def on_ready(self):
        print("Cog 'Point' loaded successfully")  
    admin = discord.SlashCommandGroup("admin", "Admin commands")
  
    @slash_command() 
    async def hi(self, actx):
      await actx.respond(f"Hello server {actx.guild.id}")

    add_choice = [
      OptionChoice(name="Bronze", value="0"), #  Value must be a string.
      OptionChoice(name="Silver", value="1"), #  Value must be a string.
      OptionChoice(name="Diamond", value="2") #  Value must be a string.
    ]
    @slash_command(name="add", description = "เพิ่มแต้ม / Add Point")
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
    bot.add_cog(Point(bot))
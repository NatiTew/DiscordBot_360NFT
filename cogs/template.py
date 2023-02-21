import discord

from discord.ext import commands
from discord import ApplicationContext as actx
from discord.commands import slash_command, user_command, guild_only, Option, SlashCommandGroup


class Template(discord.ext.commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        
    @commands.Cog.listener()
    async def on_ready(self):
        print("Cog 'Template' loaded successfully")  

    @slash_command() 
    async def hello(self, actx):
        await actx.respond("Hello!")

def setup(bot):
    bot.add_cog(Template(bot))
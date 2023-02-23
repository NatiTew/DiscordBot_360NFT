import os
import sys
import discord
from os import system
from time import sleep
from traceback import print_exc
from datetime import datetime
from discord.ext import commands

my_secret = os.environ['Token']
my_ow = os.environ['Owner']
extensions = ["cogs.template","cogs.NFT360"]


class Bot(commands.Bot):
    def __init__(self):
        super().__init__(
            owner_ids={my_ow},
            command_prefix="-",
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
      

bot = Bot()

# # class MyView(discord.ui.View):
# #   @discord.ui.select( # the decorator that lets you specify the properties of the select menu
# #     placeholder = "Choose a Flavor!", # the placeholder text that will be displayed if nothing is selected
# #     min_values = 1, # the minimum number of values that must be selected by the users
# #     max_values = 1, # the maximum number of values that can be selected by the users
# #     options = [ # the list of options from which users can choose, a required field
# #       discord.SelectOption(
# #         label="template",
# #         description="Pick this if you like vanilla!"
# #       ),
# #       discord.SelectOption(
# #         label="unload",
# #         description="Pick this if you like chocolate!"
# #       ),
# #       discord.SelectOption(
# #         label="Strawberry",
# #         description="Pick this if you like strawberry!"
# #       )
# #     ]
# #   )
# #   async def select_callback(self, select, interaction): # the function called when the user is done selecting options
# #     await interaction.response.send_message(f"Awesome! I like {select.values[0]} too!")

# # @bot.slash_command(name="flavor", description = "test")
# # async def flavor(ctx, wallet:discord.Option(str, description="test2")):
# #   await ctx.respond("Choose a flavor!", view=MyView())


@bot.slash_command(name="__start_here", description = "set channel for admin")
async def __start_here(ctx):
  await ctx.respond(str(ctx.guild.id) + " " + str(ctx.channel.id))

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
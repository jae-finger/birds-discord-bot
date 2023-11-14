import discord
from discord.ext import commands
import os
from dotenv import load_dotenv

# ENV variables
load_dotenv()

BIRB_RESCUE_TOKEN = str(os.getenv('BIRB_DISCORD_TOKEN'))

intents = discord.Intents.default()
intents.message_content = True

# TODO: Update this description
description = '''Rescue the birds bot!!!!'''

# Change only the no_category default string
help_command = commands.DefaultHelpCommand(
    no_category = 'Commands'
)

bot = commands.Bot(command_prefix='?', description=description, intents=intents, help_command = help_command)

@bot.event
async def on_ready():
    print(f'We have logged in as {bot.user}')
    print('--------------------------------')

@bot.command()
async def hello(ctx):
    await ctx.send('Ahoy!')

initial_extensions = ['cogs.welcome_cog']

for extension in initial_extensions:
    bot.load_extension(extension)

bot.run(token=BIRB_RESCUE_TOKEN)
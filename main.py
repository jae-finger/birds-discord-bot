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

for extension in ['cogs.welcome_cog']:
    bot.load_extension(extension)
    # bot.load_extension('cogs.welcome_cog')

@bot.command()
async def hello(ctx):
    await ctx.send('Ahoy!')

bot.run(token=BIRB_RESCUE_TOKEN)
import discord
from discord.ext import commands
import os
from dotenv import load_dotenv

# ENV variables
load_dotenv()

BIRB_RESCUE_TOKEN = str(os.getenv('BIRB_DISCORD_TOKEN'))

intents = discord.Intents.default()
intents.message_content = True

client = discord.Client(intents=intents, command_prefix='?')

@client.event
async def on_ready():
    print(f'We have logged in as {client.user}')

@client.command()
async def hello(ctx):
    await ctx.send('Ahoy!')

client.run(token=BIRB_RESCUE_TOKEN)
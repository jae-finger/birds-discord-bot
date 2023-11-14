import discord
from discord.ext import commands
import os
from dotenv import load_dotenv

# ENV variables
load_dotenv()
BIRB_RESCUE_TOKEN = os.getenv('BIRB_RESCUE_TOKEN')

intents = discord.Intents.default()
intents.message_content = True

client = discord.Client(intents=intents)

@client.event
async def on_ready():
    print(f'We have logged in as {client.user}')

@client.event
async def on_message(message):
    if message.author == client.user:
        return

    if message.content.startswith('$hello'):
        await message.channel.send('Hello!')

client.run(BIRB_RESCUE_TOKEN)
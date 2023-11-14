import discord
from discord.ext import commands
import os
from dotenv import load_dotenv

# ENV variables
load_dotenv()
BIRB_RESCUE_TOKEN = os.getenv('BIRB_RESCUE_TOKEN')

# Bot setup
bot = commands.Bot(command_prefix="!")

# Event example: Print a message when the bot is ready
@bot.event
async def on_ready():
    print(f"{bot.user.name} has connected to Discord!")

# Command example: Respond to the !hello command
@bot.command(name='hello')
async def hello(ctx):
    await ctx.send("Hello!")

# Run the bot
bot.run(BIRB_RESCUE_TOKEN)
intents = discord.Intents.default()
intents.members = True

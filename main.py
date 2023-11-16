import discord
from discord.ext import commands
import os
from dotenv import load_dotenv

# ENV variables
load_dotenv()

BIRB_RESCUE_TOKEN = str(os.getenv('BIRB_DISCORD_TOKEN'))
GENERAL_CHANNEL_ID = int(os.getenv('GENERAL_CHANNEL_ID'))
DEFAULT_DISCORD_ID = int(os.getenv('DEFAULT_DISCORD_ID'))

# Check and create the data directory and file if not exists
if not os.path.exists('data'):
    os.makedirs('data')
if not os.path.isfile('data/greeted_members.txt'):
    with open('data/greeted_members.txt', 'w') as file:
        file.write(f'{DEFAULT_DISCORD_ID}\n')  # Adding your Discord user ID


# Helper Functions TODO: Put these in a utility folder
# Function to check if a member's ID is in the file
def is_member_greeted(member_id):
    with open('data/greeted_members.txt', 'r') as file:
        greeted_members = file.read().splitlines()
    return str(member_id) in greeted_members

# Function to add a member's ID to the file
def add_greeted_member(member_id):
    with open('data/greeted_members.txt', 'a') as file:
        file.write(f'{member_id}\n')

# Set the bot's permissions
intents = discord.Intents.default()
intents.message_content = True
intents.members = True
intents.guilds = True

# Create the bot
bot = commands.Bot(
    command_prefix='?',
    description='''Jon's Rescue the Birds! discord bot. Please ping him with any questions or kudos!''',
    intents=intents,
    help_command=commands.DefaultHelpCommand(no_category = 'Commands')
)

# Events
# On Ready Event
@bot.event
async def on_ready():
    print(f'We have logged in as {bot.user}')
    print(f'General Channel ID: {GENERAL_CHANNEL_ID}')
    print('--------------------------------')

@bot.event
async def on_member_join(member):
    if not is_member_greeted(member.id):
        general_channel = bot.get_channel(GENERAL_CHANNEL_ID)
        if general_channel is not None:
            welcome_message = f'''Welcome {member.mention} to Rescue the Birds!\n Please take a chance to look around. If you have any questions, please ping Jon!'''
            await general_channel.send(welcome_message)
            add_greeted_member(member.id)

# Commands
# Hello Command
@bot.command(description="Say hello to the bot")
async def hello(ctx):
    hello_message = f'''Ahoy, {ctx.author.name}! to Rescue the Birds!\n Please take a chance to look around. If you have any questions, please ping Jon!'''

# Source Code
@bot.command(description="")
async def source_code(ctx):
    hello_embed = discord.Embed(title="Source Code!", description=f"Thanks for your interest in the Bird Bot. Check out the source code!", url="https://github.com/jae-finger/birds-discord-bot")
    await ctx.send(embed=hello_embed)

bot.run(token=BIRB_RESCUE_TOKEN)
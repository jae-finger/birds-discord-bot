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

# Help function
class SimpleHelpCommand(commands.HelpCommand):
    async def send_bot_help(self, mapping):
        help_message = discord.Embed(title="Help! Jon's Rescue the Birds Bot", description=f"Please ping Jon with any questions or kudos :]\n```commands:\n- ?hello - say hi to the bot\n- ?help - this help menu\n- ?source_code - link to bot source code\n```")
        channel = self.get_destination()
        await channel.send(embed=help_message)

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
    # help_command=commands.DefaultHelpCommand(no_category = 'Misc', sort_commands=True)
    help_command=SimpleHelpCommand(no_category = 'Misc', sort_commands=True)
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
            welcome_message = f'''Welcome {member.mention} to Rescue the Birds!\n We hope you're ready to help some birds! Please take a look around and introduce yourself!'''
            await general_channel.send(welcome_message)
            add_greeted_member(member.id)

# Commands
# Hello Command
@bot.command(description="!")
async def hello(ctx):
    hello_message = f'''Ahoy, {ctx.author.name}! This discord bot was created by: <@{DEFAULT_DISCORD_ID}>. If you have any questions or kudos then ping him :)"'''
    await ctx.send(hello_message)

# Source Code
@bot.command(description="!")
async def source_code(ctx):
    hello_embed = discord.Embed(title="Source Code!", description=f"Thanks for your interest in the Bird Bot. Check out the source code on github :)", url="https://github.com/jae-finger/birds-discord-bot")
    hello_embed.set_image(url="https://raw.githubusercontent.com/jae-finger/birds-discord-bot/main/data/birb_logo_dalle.png")
    await ctx.send(embed=hello_embed)

bot.run(token=BIRB_RESCUE_TOKEN)
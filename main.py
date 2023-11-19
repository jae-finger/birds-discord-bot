import discord
from discord.ext import commands
import os
from dotenv import load_dotenv
import utils
from datetime import datetime, timedelta, timezone

# ENV variables
load_dotenv()

BIRB_RESCUE_TOKEN = str(os.getenv('BIRB_DISCORD_TOKEN'))
GENERAL_CHANNEL_ID = int(os.getenv('GENERAL_CHANNEL_ID'))
DEFAULT_DISCORD_ID = int(os.getenv('DEFAULT_DISCORD_ID'))
DISCORD_GUILD_ID = int(os.getenv('DISCORD_GUILD_ID'))

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
    help_command=SimpleHelpCommand(no_category = 'Misc', sort_commands=True)
)

# Events
# On Ready Event
@bot.event
async def on_ready():
    await bot.change_presence(status=discord.Status.idle, activity=discord.Game('CAW!'))
    print(f'We have logged in as {bot.user}')
    print(f'General Channel ID: {GENERAL_CHANNEL_ID}')
    print('--------------------------------')

@bot.event
async def on_member_join(member):
    if not utils.is_member_greeted(member.id):
        general_channel = bot.get_channel(GENERAL_CHANNEL_ID)
        if general_channel is not None:
            welcome_message = f"Welcome to Rescue the Birds, {member.mention}!\n We hope you're ready to help some birds🦜 Please take a look around and introduce yourself! More information about the bot can be foiund by typing: `?help`"
            await general_channel.send(welcome_message)
            utils.add_greeted_member(member.id)

# Commands
# Hello Command
@bot.command(description="!")
async def hello(ctx):
    hello_message = f"Ahoy, {ctx.author.name}! This discord bot was created by: <@{DEFAULT_DISCORD_ID}>. It uses python3.11 and runs on a raspberrypi 4. Find out more about the bot by typing: `?help`"
    await ctx.send(hello_message)

# Source Code
@bot.command(description="!")
async def source_code(ctx):
    hello_embed = discord.Embed(title="Source Code!", description=f"Thanks for your interest in the Bird Bot. Check out the source code on github :)", url="https://github.com/jae-finger/birds-discord-bot")
    hello_embed.set_image(url="https://raw.githubusercontent.com/jae-finger/birds-discord-bot/main/data/birb_logo_dalle.png")
    await ctx.send(embed=hello_embed)

@bot.command()
async def list_meetings(ctx):
    if ctx.message.author.id == DEFAULT_DISCORD_ID:
        guild = bot.get_guild(DISCORD_GUILD_ID)
        if not guild:
            await ctx.send('Guild not found.')
            return

        events = guild.scheduled_events
        if not events:
            await ctx.send('No scheduled events found.')
            return

        # Formatting the list of events
        event_list = '\n'.join([f'{event.name} - {event.start_time.strftime("%Y-%m-%d %H:%M")}' for event in events])
        await ctx.send(f'Scheduled Events:\n{event_list}')

from datetime import datetime, timedelta
import discord

from datetime import datetime, timedelta
import discord

@bot.command()
async def add_meeting(ctx, name: str, start_time_str: str, end_time_str: str, description: str = None, location: str = None):
    if ctx.message.author.id == DEFAULT_DISCORD_ID:
        guild = bot.get_guild(DISCORD_GUILD_ID)
        if not guild:
            await ctx.send('Guild not found.')
            return

        # Define the format for date and time input
        dt_format = "%Y-%m-%d %H:%M"

        try:
            # Convert start_time_str and end_time_str from string to UTC datetime object
            start_time_utc = datetime.strptime(start_time_str, dt_format)
            end_time_utc = datetime.strptime(end_time_str, dt_format)

            # Convert the datetime objects to UTC timezone-aware datetime objects
            utc_timezone = timezone.utc
            start_time_aware = start_time_utc.replace(tzinfo=utc_timezone)
            end_time_aware = end_time_utc.replace(tzinfo=utc_timezone)

            # Adjust the time to CST by subtracting 6 hours (UTC-6)
            start_time_cst = start_time_aware - timedelta(hours=6)
            end_time_cst = end_time_aware - timedelta(hours=6)

            # Ensure start time is in the future
            if start_time_cst < datetime.now(utc_timezone) - timedelta(hours=6):
                raise ValueError("Start time must be in the future.")

        except ValueError as e:
            await ctx.send(f'Invalid date format or time: {str(e)}')
            return

        # Create the scheduled event
        event = await guild.create_scheduled_event(
            name=name, 
            start_time=start_time_cst, 
            end_time=end_time_cst, 
            description=description, 
            location=location, 
            entity_type=discord.EntityType.external,
            privacy_level=discord.PrivacyLevel.guild_only
        )
        await ctx.send(f'Event "{name}" created successfully!')

        # Create the scheduled event
        # image_url = "https://raw.githubusercontent.com/jae-finger/birds-discord-bot/main/data/birb_logo_dalle.png"
        # image=image_url

@bot.command()
async def announce_next_meeting(ctx):
    if ctx.message.author.id != DEFAULT_DISCORD_ID:
        await ctx.send("You do not have permission to use this command.")
        return

    guild = bot.get_guild(DISCORD_GUILD_ID)
    if not guild:
        await ctx.send('Guild not found.')
        return

    # Get the list of scheduled events and find the next one
    events = sorted(guild.scheduled_events, key=lambda e: e.start_time)
    next_event = None
    for event in events:
        if event.start_time > discord.utils.utcnow():
            next_event = event
            break

    if not next_event:
        await ctx.send('No upcoming events found.')
        return

    # Format the announcement message
    cst_start_time = next_event.start_time + timedelta(hours=6)
    announcement = f"Hey @everyone! Just a heads up that our next meeting is: '{next_event.name}' on {cst_start_time.strftime('%Y-%m-%d at %I:%M CST')} 🦜 May your bugs be few and your commits be many 🦜"

    # Send the announcement to the general channel
    general_channel = bot.get_channel(GENERAL_CHANNEL_ID)
    if general_channel:
        await general_channel.send(announcement)
    else:
        await ctx.send('General channel not found.')




if __name__ == '__main__':
    # Run the bot
    bot.run(token=BIRB_RESCUE_TOKEN)
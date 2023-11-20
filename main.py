import discord
from discord.ext import commands, tasks
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

# load cogs
async def setup():
    await bot.load_extension('event_reminder_cog')


# Events
# On Ready Event
@bot.event
async def on_ready():
    await bot.change_presence(status=discord.Status.idle, activity=discord.Game('CAW!'))
    print(f'We have logged in as {bot.user}')
    print(f'General Channel ID: {GENERAL_CHANNEL_ID}')
    print('--------------------------------')
    event_check.start()

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


# Meetings
async def check_next_event(bot):
    guild = bot.get_guild(DISCORD_GUILD_ID)  # Replace with your guild ID
    if guild:
        next_event = await get_next_event(guild)  # Ensure this is an async function
        if next_event:
            time_until_event = next_event.start_time - datetime.now(timezone.utc)
            if time_until_event <= timedelta(hours=1):
                channel = bot.get_channel(GENERAL_CHANNEL_ID)
                if channel:
                    await channel.send(f"Reminder @everyone: our {next_event.name} is happening in less than an hour!")
                else:
                    print(f"Unable to find channel with ID: {GENERAL_CHANNEL_ID}")
            else:
                print(f"Found an upcoming event: '{next_event.name}'. Will announce 1 hour before the event.")
        else:
            print("No upcoming events found at this time.")

async def get_next_event(guild):
    # Fetch the list of scheduled events for the guild
    events = await guild.fetch_scheduled_events()

    # Filter out events that have already started
    future_events = [event for event in events if event.start_time > datetime.now(timezone.utc)]

    # Sort them by start time
    future_events.sort(key=lambda x: x.start_time)

    # Return the next event or None if there are no future events
    return future_events[0] if future_events else None


@tasks.loop(minutes=60)
async def event_check():
    await check_next_event(bot)

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
            # CST timezone offset (UTC-6), adjust for daylight saving if necessary
            cst_offset = timedelta(hours=-6)
            # Create a naive datetime object from the input strings
            start_time_naive = datetime.strptime(start_time_str, dt_format)
            end_time_naive = datetime.strptime(end_time_str, dt_format)

            # Determine if daylight saving time is in effect for the input dates
            # Adjust the offset to UTC-5 if daylight saving is in effect
            if start_time_naive.month > 3 and start_time_naive.month < 11:
                cst_offset = timedelta(hours=-5)  # CDT (Daylight Saving Time)

            # Make the times timezone-aware (CST or CDT)
            start_time_cst = start_time_naive.replace(tzinfo=timezone(cst_offset))
            end_time_cst = end_time_naive.replace(tzinfo=timezone(cst_offset))

            # Convert to UTC
            start_time_utc = start_time_cst.astimezone(timezone.utc)
            end_time_utc = end_time_cst.astimezone(timezone.utc)

            # Ensure start time is in the future
            if start_time_utc < datetime.now(timezone.utc):
                raise ValueError("Start time must be in the future.")

        except ValueError as e:
            await ctx.send(f'Invalid date format or time: {str(e)}')
            return

        # Create the scheduled event
        # image_url = "https://raw.githubusercontent.com/jae-finger/birds-discord-bot/main/data/birb_logo_dalle.png"
        event = await guild.create_scheduled_event(
            name=name, 
            start_time=start_time_utc, 
            end_time=end_time_utc, 
            description=description, 
            location=location, 
            entity_type=discord.EntityType.external,
            privacy_level=discord.PrivacyLevel.guild_only,
            # image=image_url
        )
        await ctx.send(f'Event "{name}" created successfully!')

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

bot.run(token=BIRB_RESCUE_TOKEN)
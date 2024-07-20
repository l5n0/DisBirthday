import discord
from discord.ext import commands, tasks
from datetime import datetime
import json
import os
from dotenv import load_dotenv
from apscheduler.schedulers.asyncio import AsyncIOScheduler
import logging

# Load environment variables
load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
COMMAND_PREFIX = os.getenv('COMMAND_PREFIX', '!')
BIRTHDAY_CHANNEL = os.getenv('BIRTHDAY_CHANNEL', 'general')

# Set up logging
logging.basicConfig(level=logging.INFO)

intents = discord.Intents.default()
intents.messages = True
intents.guilds = True
intents.message_content = True  # Request message content intent

bot = commands.Bot(command_prefix=COMMAND_PREFIX, intents=intents, help_command=None)

BIRTHDAYS_FILE = 'birthdays.json'

def load_birthdays():
    if os.path.exists(BIRTHDAYS_FILE):
        with open(BIRTHDAYS_FILE, 'r') as f:
            return json.load(f)
    return {}

def save_birthdays(birthdays):
    with open(BIRTHDAYS_FILE, 'w') as f:
        json.dump(birthdays, f, indent=4)

birthdays = load_birthdays()

@bot.event
async def on_ready():
    logging.info(f'Logged in as {bot.user.name}')
    check_birthdays.start()

@bot.command()
async def birthday(ctx, user: discord.Member, date: str):
    """Sets the birthday of a user. Usage: !birthday @user DD.MM.YYYY"""
    logging.info(f'birthday command called by {ctx.author} for {user} with date {date}')
    try:
        datetime.strptime(date, '%d.%m.%Y')
    except ValueError:
        await ctx.send("Date format is incorrect. Please use DD.MM.YYYY format.")
        return

    birthdays[str(user.id)] = date
    save_birthdays(birthdays)
    await ctx.send(f"Birthday for {user.mention} set to {date}")

@bot.command(name='help')
async def custom_help(ctx):
    """Displays the help message with available commands."""
    logging.info(f'help command called by {ctx.author}')
    help_message = (
        "Here are the available commands:\n"
        f"{COMMAND_PREFIX}birthday @user DD.MM.YYYY - Set the birthday for the user.\n"
        f"{COMMAND_PREFIX}help - Display this help message.\n"
        f"{COMMAND_PREFIX}test_birthday - Test the birthday message sending functionality."
    )
    await ctx.send(help_message)

@bot.command()
async def test_birthday(ctx):
    """Test the birthday message sending functionality."""
    logging.info(f'test_birthday command called by {ctx.author}')
    today = datetime.today().strftime('%d.%m')
    for user_id, birthday in birthdays.items():
        logging.info(f'Checking birthday for user_id {user_id} with birthday {birthday}')
        if today == birthday[:5]:  # Only compare day and month
            logging.info(f'Birthday match found for user_id {user_id}')
            user = await bot.fetch_user(int(user_id))
            logging.info(f'Fetched user: {user}')
            for guild in bot.guilds:
                if user in guild.members:
                    logging.info(f'User {user} is a member of guild {guild}')
                    channel = discord.utils.get(guild.text_channels, name=BIRTHDAY_CHANNEL)
                    if channel:
                        try:
                            await channel.send(f"@everyone Happy Birthday {user.mention}! 🎉🎂")
                            await ctx.send(f"Test: Happy Birthday message sent for {user.mention}.")
                            logging.info(f'Birthday message sent to {channel.name} in guild {guild.name}')
                        except Exception as e:
                            logging.error(f'Failed to send message to {channel.name} in guild {guild.name}: {e}')
                    else:
                        logging.warning(f'Channel "{BIRTHDAY_CHANNEL}" not found in guild {guild.name}')

@tasks.loop(minutes=1)
async def check_birthdays():
    today = datetime.today().strftime('%d.%m')
    for user_id, birthday in birthdays.items():
        if today == birthday[:5]:  # Only compare day and month
            user = await bot.fetch_user(int(user_id))
            for guild in bot.guilds:
                if user in guild.members:
                    channel = discord.utils.get(guild.text_channels, name=BIRTHDAY_CHANNEL)
                    if channel:
                        await channel.send(f"@everyone Happy Birthday {user.mention}! 🎉🎂")

@check_birthdays.before_loop
async def before_check_birthdays():
    await bot.wait_until_ready()

bot.run(TOKEN)
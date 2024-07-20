import discord
from discord.ext import commands, tasks
from datetime import datetime
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
intents.members = True  # Request member intent
intents.message_content = True  # Request message content intent

bot = commands.Bot(command_prefix=COMMAND_PREFIX, intents=intents, help_command=None)

def get_channel(guild, channel_identifier):
    # Try to find channel by ID first
    channel = discord.utils.get(guild.text_channels, id=int(channel_identifier)) if channel_identifier.isdigit() else None
    if channel is None:
        # Fallback to find channel by name
        channel = discord.utils.get(guild.text_channels, name=channel_identifier)
    return channel

@bot.event
async def on_ready():
    logging.info(f'Logged in as {bot.user.name}')
    for guild in bot.guilds:
        logging.info(f'Bot is connected to guild: {guild.name} (ID: {guild.id})')
        logging.info(f'Guild member count: {len(guild.members)}')
        logging.info(f'Available channels:')
        for channel in guild.text_channels:
            logging.info(f' - {channel.name} (ID: {channel.id})')
    check_birthdays.start()

@tasks.loop(minutes=1)
async def check_birthdays():
    from commands import birthday_data, get_channel

    today = datetime.today().strftime('%d.%m')
    for user_id, birthday in birthday_data.items():
        if today == birthday[:5]:  # Only compare day and month
            user = await bot.fetch_user(int(user_id))
            for guild in bot.guilds:
                member = guild.get_member(int(user_id))
                if member:
                    channel = get_channel(guild, BIRTHDAY_CHANNEL)
                    if channel:
                        await channel.send(f"@everyone Happy Birthday {user.mention}! 🎉🎂")

@check_birthdays.before_loop
async def before_check_birthdays():
    await bot.wait_until_ready()

async def main():
    async with bot:
        await bot.load_extension("commands")
        await bot.start(TOKEN)

if __name__ == "__main__":
    import asyncio
    asyncio.run(main())

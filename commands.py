import discord
from discord.ext import commands
from datetime import datetime
import logging
import json
import os

BIRTHDAYS_FILE = 'birthdays.json'

def load_birthday_data():
    if os.path.exists(BIRTHDAYS_FILE):
        with open(BIRTHDAYS_FILE, 'r') as f:
            return json.load(f)
    return {}

def save_birthday_data(birthday_data):
    with open(BIRTHDAYS_FILE, 'w') as f:
        json.dump(birthday_data, f, indent=4)

birthday_data = load_birthday_data()

def get_channel(guild, channel_identifier):
    # Try to find channel by ID first
    channel = discord.utils.get(guild.text_channels, id=int(channel_identifier)) if channel_identifier.isdigit() else None
    if channel is None:
        # Fallback to find channel by name
        channel = discord.utils.get(guild.text_channels, name=channel_identifier)
    return channel

class BirthdayCommands(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def birthday(self, ctx, user: discord.Member, date: str):
        """Sets the birthday of a user. Usage: !birthday @user DD.MM.YYYY"""
        logging.info(f'birthday command called by {ctx.author} for {user} with date {date}')
        try:
            datetime.strptime(date, '%d.%m.%Y')
        except ValueError:
            await ctx.send("Date format is incorrect. Please use DD.MM.YYYY format.")
            return

        birthday_data[str(user.id)] = date
        save_birthday_data(birthday_data)
        await ctx.send(f"Birthday for {user.mention} set to {date}")

    @commands.command(name='help')
    async def custom_help(self, ctx):
        """Displays the help message with available commands."""
        logging.info(f'help command called by {ctx.author}')
        help_message = (
            "Here are the available commands:\n"
            f"{ctx.prefix}birthday @user DD.MM.YYYY - Set the birthday for the user.\n"
            f"{ctx.prefix}help - Display this help message.\n"
            f"{ctx.prefix}test_birthday - Test the birthday message sending functionality.\n"
            f"{ctx.prefix}birthdays - Display all logged birthdays."
        )
        await ctx.send(help_message)

    @commands.command()
    async def birthdays(self, ctx):
        """Displays all logged birthdays."""
        logging.info(f'birthdays command called by {ctx.author}')
        if not birthday_data:
            await ctx.send("No birthdays logged.")
        else:
            embed = discord.Embed(title="Logged Birthdays", color=discord.Color.blue())
            for user_id, date in birthday_data.items():
                user = await self.bot.fetch_user(int(user_id))
                embed.add_field(name=f"{user.name}#{user.discriminator}", value=date, inline=False)
            await ctx.send(embed=embed)

    @commands.command()
    async def test_birthday(self, ctx):
        """Test the birthday message sending functionality."""
        logging.info(f'test_birthday command called by {ctx.author}')
        today = datetime.today().strftime('%d.%m')
        for user_id, birthday in birthday_data.items():
            logging.info(f'Checking birthday for user_id {user_id} with birthday {birthday}')
            if today == birthday[:5]:  # Only compare day and month
                logging.info(f'Birthday match found for user_id {user_id}')
                user = await self.bot.fetch_user(int(user_id))
                logging.info(f'Fetched user: {user}')
                for guild in self.bot.guilds:
                    member = guild.get_member(int(user_id))
                    if member:
                        logging.info(f'User {user} is a member of guild {guild}')
                        channel = get_channel(guild, os.getenv('BIRTHDAY_CHANNEL', 'general'))
                        if channel:
                            logging.info(f'Found channel {channel.name} in guild {guild.name}')
                            try:
                                await channel.send(f"@everyone Happy Birthday {user.mention}! 🎉🎂")
                                await ctx.send(f"Test: Happy Birthday message sent for {user.mention}.")
                                logging.info(f'Birthday message sent to {channel.name} in guild {guild.name}')
                            except Exception as e:
                                logging.error(f'Failed to send message to {channel.name} in guild {guild.name}: {e}')
                        else:
                            logging.warning(f'Channel "{os.getenv("BIRTHDAY_CHANNEL", "general")}" not found in guild {guild.name}')
                    else:
                        logging.info(f'User {user} is not a member of guild {guild}')

async def setup(bot):
    await bot.add_cog(BirthdayCommands(bot))

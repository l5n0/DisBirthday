# Discord Birthday Bot

A Discord bot that allows users to set and manage birthdays. The bot can announce birthdays in a specified channel and provide a list of all registered birthdays.

## Features

- Set a user's birthday with a command.
- Announce birthdays in a specified channel.
- Display all registered birthdays.
- Provide a help command with usage instructions.

## Prerequisites

- Python 3.8+
- Discord bot token
- `pip` for installing dependencies

## Installation

1. **Clone the repository:**

   ```sh
   git clone https://github.com/yourusername/DisBirthday.git
   cd DisBirthday
    ```
2. Install the required dependencies:
   ```sh
    pip install -r requirements.txt
   ```
3. Create a `.env` file in the project directory with the following contents:
   ```sh
    DISCORD_TOKEN=YOUR_DISCORD_BOT_TOKEN
    COMMAND_PREFIX=!
    BIRTHDAY_CHANNEL=general
    ```
# Usage

## Run the bot:

```sh

python bot.py
```
## Commands:
### Set a birthday:

```sh
!birthday @user DD.MM.YYYY
```
Sets the birthday of the mentioned user.

### Display all birthdays:

```sh

!birthdays
```
Displays all registered birthdays in an embedded message.

### Test birthday announcement:

```sh

!test_birthday
```
Sends a test birthday announcement for today's date.

### Help:

```sh

        !help
```
Displays the help message with all available commands in an embedded format.

File Structure

- bot.py: Main bot script that initializes the bot and loads commands.
- commands.py: Contains the command definitions and related logic.
- .env: Environment variables file for configuration (not included in the repository).


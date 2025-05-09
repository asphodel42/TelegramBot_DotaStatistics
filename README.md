# Dota 2 Last Match Statistics Bot

> **Note:** This is a fun project created for a friend to track their Dota 2 matches, but you can easily modify it to track any player's statistics according to your needs.

A Telegram bot that automatically tracks and posts statistics from a Dota 2 player's most recent matches using the OpenDota API.

## Example of a message
![зображення](https://github.com/user-attachments/assets/1aa2e1c8-7541-47f7-be32-bd908a15558d)

## Features

- Automatically checks for new Dota 2 matches every 30 minutes
- Posts detailed match statistics to Telegram chats when a new match is detected
- Includes hero information with images
- Displays player rank information
- Persists active chats between bot restarts

## Available Commands

- `/start` - Activate the bot in the current chat
- `/rank` - Display the player's current rank with medal image
- `/cheer` - Send a motivational message

## Setup Guide

1. Clone the repository:

   ```
   git clone https://github.com/yourusername/dota-last-match-statistics-bot.git
   cd dota-last-match-statistics-bot
   ```

2. Install dependencies:

   ```
   pip install -r requirements.txt
   ```

3. Create a `.env` file in the root directory with the following variables:

   ```
   TG_BOT_TOKEN=your_telegram_bot_token
   PLAYER_ID=your_dota_player_id
   ```

   - To get a Telegram bot token, talk to [@BotFather](https://t.me/BotFather) on Telegram
   - To find your Dota 2 player ID, search your username on [OpenDota](https://www.opendota.com/)

4. Customize the bot (optional):

   - Modify the messages in `main.py` to change what the bot sends
   - Update the player name in the message templates

5. Run the bot:
   ```
   python main.py
   ```

## Customizing For A Different Player

To adapt this bot for tracking a different player:

1. Change the `PLAYER_ID`
2. Update the message templates in `main.py`
3. Customize the bot messages to suit your preferences

## Dependencies

- aiogram - Telegram bot framework
- requests - HTTP requests to OpenDota API
- asyncio - Asynchronous I/O

## Notes

- The bot logs activities to `bot_log.txt`
- Match statistics are saved to `game_statistics.json`
- Active chat IDs are stored in `chats.json`
- The last processed match ID is saved in `last_match_id.txt`

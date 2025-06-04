import os
import json
import asyncio
from dotenv import load_dotenv
from aiogram import Bot, Dispatcher, types
from aiogram.types import Message, ChatMemberUpdated, InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.filters import Command
from opendota_api import getLastMatchId, getMatchStats, saveStatsToJSON, getHeroInfo, getRankImage, log_message

# Load environment variables
load_dotenv()

BOT_TOKEN = os.getenv("TG_BOT_TOKEN")
PLAYER_ID = int(os.getenv("PLAYER_ID"))

# Initialize bot and dispatcher
bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()

# File for saving chat_id
CHAT_FILE = "chats.json"

# Loading saved chats


def load_chats():
    if os.path.exists(CHAT_FILE):
        with open(CHAT_FILE, "r") as file:
            return set(json.load(file))
    return set()

# Saving chats to file


def save_chats():
    with open(CHAT_FILE, "w") as file:
        json.dump(list(active_chats), file)


active_chats = load_chats()


@dp.my_chat_member()
async def on_chat_member_update(update: ChatMemberUpdated):
    """Handler for chat member updates"""
    new_status = update.new_chat_member.status  # Get the new status

    if update.new_chat_member.user.id == (await bot.me()).id and new_status in {"member", "administrator"}:
        chat_id = update.chat.id
        active_chats.add(chat_id)  # Adding chat to set
        save_chats()  # Update file

        log_message(f"Bot added to chat {chat_id}")
        await bot.send_message(chat_id, "Бот активований!👾")


async def check_matches():
    """Check new matches and send updates in every active chat"""
    try:
        with open("last_match_id.txt", "r", encoding="utf-8") as file:
            file_content = file.read().strip()
            last_match_id = None if file_content == "" else int(file_content)
    except Exception as e:
        last_match_id = None
        log_message(f"Error reading last match ID: {e}")

    while True:
        try:
            match_id = getLastMatchId(PLAYER_ID)

            if last_match_id != match_id:
                last_match_id = match_id
                stats = getMatchStats(PLAYER_ID, match_id)
                saveStatsToJSON(stats)
                hero_name, hero_image = getHeroInfo(stats['hero_id'])

                message = (
                    f"{'😎 Легкі +25' if stats['win'] else '💢 Знову -25 '} за {stats['duration']//60}.{stats['duration']%60}\n"
                    f"🤍 {'<u>Radiant</u>' if stats['team'] == 'radiant' else 'Radiant'}   {stats['radiant_score']} / {stats['dire_score']}   {'<u>Dire</u>' if stats['team'] == 'dire' else 'Dire'}🖤\n\n"
                    f"🙄 Hero: {hero_name}\n"
                    f"💯 K/D/A: {stats['kills']}/{stats['deaths']}/{stats['assists']}\n\n"
                    f"Networth: {stats['net_worth']}\n"
                    f"GPM: {stats['gold_per_min']} | XPM: {stats['xp_per_min']}\n"
                    f"Hero dmg: {stats['hero_damage']}\nTower dmg: {stats['tower_damage']}\n\n"
                )
                keyboard = InlineKeyboardMarkup(inline_keyboard=[
                    [InlineKeyboardButton(
                        text="🔍 Детальніше про матч", url=f"https://www.opendota.com/matches/{match_id}")]
                ])

                # Відправлення повідомлення у всі активні чати
                for chat_id in active_chats:
                    await bot.send_photo(
                        chat_id,
                        photo=hero_image,
                        caption=message,
                        parse_mode="HTML",
                        reply_markup=keyboard)

                log_message(
                    f"New match {match_id} detected and sent to chats.")
            else:
                log_message("No new match yet, checking again...")

        except Exception as e:
            log_message(f"Error: {e}")

        await asyncio.sleep(30*60)


@dp.message(Command('start'))
async def start_command(message: Message):
    """Handler for /start"""
    active_chats.add(message.chat.id)  # Adding chat to set
    save_chats()  # Update file
    await message.answer("Бот активований!👾")


@dp.message(Command('cheer'))
async def cheer_command(message: Message):
    """Handler for /cheer"""
    await message.answer("ЛУПИ ИХ ЛЕХА💪🏻😈🤙🏻 МЕСИ ИХ ЛЕХА💪🏻😈🤙🏻ЛОМАЙ ИХ ЛЕХА👿🤜🏻💀🤛🏻🤬 ГАСИ ИХ ЛЕХА💪🏻😈🤙🏻 ГНОБИ ИХ ЛЕХА👊🏻😼👊🏻ТОПЧИ ИХ ЛЕХА👊🏻🤬👊🏻ДАВИ ИХ ЛЕХА😾🤜🏻🐷🤛🏻😤РУБИ ИХ ЛЕХА👊🏻😎🤙🏻ЕБИ ИХ ЛЕХА")


@dp.message(Command('rank'))
async def rank_command(message: Message):
    """Handler for /rank"""
    rank_tier_name, rank_tier_star, url_rank = getRankImage(PLAYER_ID)

    await message.answer_photo(photo=url_rank, caption=f'Ранг Олексія: {rank_tier_name} {rank_tier_star}')


async def main():
    """Start the bot and start checking matches in the background."""
    asyncio.create_task(check_matches())  # Start checking matches
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())  # Run the bot

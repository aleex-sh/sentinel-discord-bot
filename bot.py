import discord
from discord.ext import commands
from discord import app_commands
from dotenv import load_dotenv
import os
import re
import logging
import cogs

# Logging configuration (file + console)
logging.basicConfig(
    level=logging.INFO,
    format='[%(asctime)s] [%(levelname)s] %(message)s',
    handlers=[
        logging.FileHandler("logs/bot.log", encoding="utf-8"),
        logging.StreamHandler()
    ],
    force=True
)

# Load environment variables
load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')

if not TOKEN:
    logging.critical("DISCORD_TOKEN is missing in the .env file.")
    exit(1)

# Load banned words from a file
def load_banned_words():
    try:
        with open("data/badwords.txt", "r") as file:
            return [line.strip().lower() for line in file if line.strip()]
    except FileNotFoundError:
        logging.warning("The file 'badwords.txt' was not found.")
        return []

banned_words = load_banned_words()

# Compile regex pattern for filtering messages with banned words
banned_words_pattern = re.compile(r'\b(' + '|'.join(re.escape(word) for word in banned_words) + r')\b', re.IGNORECASE)

# Main bot class
class MyBot(commands.Bot):
    def __init__(self):
        intents = discord.Intents.default()
        intents.message_content = True
        intents.members = True
        super().__init__(command_prefix='/', intents=intents)

    async def setup_hook(self): # Método que carga el archivo niveles.py
        extensions = ["cogs.moderation", "cogs.utility"]
        for ext in extensions:
            try:
                await self.load_extension(ext)
                logging.info(f"Extension loaded successfully: {ext}")
            except Exception as error:
                logging.error(f"Error loading extension {ext}: {error}")
        await self.tree.sync()
        logging.info("Commands synchronized successfully.")

bot = MyBot()

# Event triggered when the bot is ready
@bot.event
async def on_ready():
    logging.info(f"{bot.user} has connected successfully.")

# Automatically filter messages containing banned words
@bot.event
async def on_message(message):
    if message.author.bot:
        return

    logging.debug(f"Message received: {message.content}")

    if banned_words_pattern.search(message.content):
        await message.delete()
        await message.channel.send(
            "Please avoid using inappropriate language. Your message has been removed.",
            delete_after=5
        )
        logging.warning("Banned word detected.")
        return

    await bot.process_commands(message)

# Run the bot
bot.run(TOKEN)

import discord
from discord.ext import commands
import os
import asyncio
from dotenv import load_dotenv, find_dotenv


# Set up the bot with intents
intents = discord.Intents.all()
intents.members = True
bot = commands.Bot(command_prefix='!', intents=intents)

load_dotenv(find_dotenv())

TOKEN = os.getenv("TOKEN")f

# Event: on ready
@bot.event
async def on_ready():
    print('Logged in as {0.user}'.format(bot))

# LOADING EXTENSIONS
async def load_extensions():
    for filename in os.listdir("./cogs"):
        if filename.endswith(".py"):
            # cut off the .py from the file name
            await bot.load_extension(f"cogs.{filename[:-3]}")

#MAIN THING
async def main():
    async with bot:
        await load_extensions()
        await bot.start(TOKEN)

asyncio.run(main())

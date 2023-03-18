import discord
import os
from dotenv import load_dotenv, find_dotenv

load_dotenv(find_dotenv())

TOKEN = os.getenv("TOKEN")


bot = discord.Bot(intents=discord.Intents.all())
starting = bot.create_group("starting", "starts games")

@bot.event
async def on_ready():
    print('Logged in as {0.user}!'.format(bot))

#create a command

@starting.command()
async def start(ctx, user: discord.Member):
  
  #thread stuff

  thread = await ctx.channel.create_thread(name="ghost", auto_archive_duration=60, type=discord.ChannelType.private_thread)

  global thread_id
  thread_id = thread.id

  await thread.add_user(ctx.author)
  await thread.add_user(user)
  await ctx.send(f"Thread '{thread.name}' created!")

  await thread.send(f"This is a private thread between {ctx.author.mention} and {user.mention}!")
  #thread stuff

@bot.event
async def on_thread_create(thread):
   print("thread was created")

bot.run(TOKEN)

#TODO read all threads under general then get the thread id's then do the thing

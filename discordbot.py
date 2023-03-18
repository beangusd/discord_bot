import discord
import os
from dotenv import load_dotenv, find_dotenv

load_dotenv(find_dotenv())

TOKEN = os.getenv("TOKEN")


bot = discord.Bot()
greetings = bot.create_group("greetings", "Greet people")

@bot.event
async def on_ready():
    print('Logged in as {0.user}!'.format(bot))

#create a command

@greetings.command()
async def start(ctx, user: discord.Member):
  thread = await ctx.channel.create_thread(name="ghost", auto_archive_duration=60, type=discord.ChannelType.private_thread)
  await thread.add_user(ctx.author)
  await thread.add_user(user)
  await ctx.send(f"Thread '{thread.name}' created!")

  await thread.send(f"This is a private thread between {ctx.author.mention} and {user.mention}!")

bot.run(TOKEN)
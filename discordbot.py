import discord
import os
from dotenv import load_dotenv, find_dotenv
import requests
import json 

url = ""
url2 = ""
game_list = []
game_string = ""



#Loading TOKEN
load_dotenv(find_dotenv())
TOKEN = os.getenv("TOKEN")

#SETTING UP INTENTS
bot = discord.Bot(intents=discord.Intents.all())
starting = bot.create_group("starting", "starts games")

@bot.event
async def on_ready():
    print('Logged in as {0.user}!'.format(bot))

@starting.command()
async def start(ctx, user: discord.Member):
  
  thread = await ctx.channel.create_thread(name="ghost", auto_archive_duration=60, type=discord.ChannelType.private_thread)

  global thread_id
  thread_id = thread.id

  await thread.add_user(ctx.author)
  await thread.add_user(user)
  await ctx.send(f"Thread '{thread.name}' created!")

  await thread.send(f"This is a private thread between {ctx.author.mention} and {user.mention}!")

@bot.event
async def on_thread_create(thread):
   print("thread was created")
   #print(thread.id)

@bot.event
async def on_message(message):
    # if message.author == bot.user:
    #     return 
    if isinstance(message.channel, discord.Thread) and message.channel.id == thread_id:
        print(f'Message received in thread {thread_id}: {message.content}')
    
        if len(message.content) == 1:
            print("Letter typed: " + message.content)
            game_list.append(message.content)
            game_string = ''.join(game_list)            
            url = f'https://api.datamuse.com/words?sp={game_string}*&max=1'
            r = requests.get(url)
            data = json.loads(r.text)

            try:
                for word in data:
                    name = word['word']
                print(name)
            except:
                print("YOU LOST BAFOONO")

        else:
            print("bignus you suck")
            


        # data = json.loads(r.text)

        # word_list = []

        # for word in data:
        #     name = word['word']
        #     word_list.append(name)

        # l = len(word_list)

        # for l in word_list:
        #     print(l)

bot.run(TOKEN)

#TODO manage games & listen for the correct threads.

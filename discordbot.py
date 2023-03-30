import discord
import os
from dotenv import load_dotenv, find_dotenv
import requests
import json 
import time

url = ""
url2 = ""
game_list = []
game_string = ""
player1 = None
player2 = None

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
async def start(ctx, player1: discord.Member, player2: discord.Member):

  thread = await ctx.channel.create_thread(name="ghost", auto_archive_duration=60, type=discord.ChannelType.private_thread)
  global thread_id
  thread_id = thread.id
  name = None
  game_string = None
#   player1_role = discord.utils.get(ctx.guild.roles, name="Player 1")
#   player2_role = discord.utils.get(ctx.guild.roles, name="Player 2")

#   await player1.add_roles(player1_role)
#   await player2.add_roles(player2_role)
  await thread.add_user(player1)
  await thread.add_user(player2)
  await ctx.send(f"Thread '{thread.name}' created!")
  await thread.send(f"This is a private thread between {player1.mention} and {player2.mention}!")
  
  current_player = player1
  winner = None
  await thread.send(f"{current_player.mention}'s turn")

  while not winner:
     message = await bot.wait_for('message', check=lambda m: m.author == current_player and m.channel.id == thread_id)
     
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
                print(game_string)
                if name == game_string:
                    print(current_player.name + " Lost")
                    await thread.send(f"{current_player.mention} Lost!!")
                    winner = True
                    await thread.send("Deleting in 3 seconds")
                    time.sleep(3)
                    await thread.delete()
                del name
                
            except:
                print(current_player.name + " Lost")
                await thread.send(f"{current_player.mention} Lost!!")
                winner = True
                await thread.send("Deleting in 3 seconds")
                time.sleep(3)
                await thread.delete()
        else:
            await thread.send("SEND THE RIGHT LENGTH OF TING")
                
                
            current_player = player2 if current_player == player1 else player1


#   await player1.remove_roles(player1_role)
#   await player2.remove_roles(player2_role)
# @bot.event
# async def on_thread_create(thread):
#    print("thread was created")

# @bot.event
# async def on_message(message):

#     if isinstance(message.channel, discord.Thread) and message.channel.id == thread_id:
#         print(f'Message received in thread {thread_id}: {message.content}')
    
#         if len(message.content) == 1:
#             print("Letter typed: " + message.content)
#             game_list.append(message.content)
#             game_string = ''.join(game_list)            
#             url = f'https://api.datamuse.com/words?sp={game_string}*&max=1'
#             r = requests.get(url)
#             data = json.loads(r.text)

#             try:
#                 for word in data:
#                     name = word['word']
#                 print(name)
#             except:
#                 print("YOU LOST BAFOONO")
#         else:
#             print("Invalid input")

            


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

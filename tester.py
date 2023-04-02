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

class Game:
    def __init__(self, name):
        self.name = name
        self.players = []
        self.current_turn = None
        self.is_started = False
        self.is_ended = False

    def add_player(self, player):
        if not self.is_started and not self.is_ended:
            self.players.append(player)
        else:
            raise ValueError("Cannot add player after the game has started or ended.")

    def remove_player(self, player):
        if not self.is_started and not self.is_ended:
            self.players.remove(player)
        else:
            raise ValueError("Cannot remove player after the game has started or ended.")

    def start(self):
        if len(self.players) < 2:
            raise ValueError("At least two players are required to start the game.")
        self.is_started = True
        self.current_turn = self.players[0]

    def end(self):
        self.is_ended = True

    def next_turn(self):
        if not self.is_started or self.is_ended:
            raise ValueError("Cannot take a turn before the game has started or after it has ended.")
        current_index = self.players.index(self.current_turn)
        next_index = (current_index + 1) % len(self.players)
        self.current_turn = self.players[next_index]
class GameManager:
    def __init__(self):
        self.games = {}

    def create_game(self, name):
        if name in self.games:
            raise ValueError("Game with the same name already exists.")
        game = Game(name)
        self.games[name] = game

    def get_game(self, name):
        if name not in self.games:
            raise ValueError("Game with the given name does not exist.")
        return self.games[name]

    def delete_game(self, name):
        if name not in self.games:
            raise ValueError("Game with the given name does not exist.")
        del self.games[name]

@starting.command()
async def start(ctx, player1: discord.Member, player2: discord.Member):

  thread = await ctx.channel.create_thread(name="ghost", auto_archive_duration=60, type=discord.ChannelType.private_thread)
  global thread_id
  thread_id = thread.id
  name = None
  game_string = None
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



bot.run(TOKEN)

#TODO manage games & listen for the correct threads.

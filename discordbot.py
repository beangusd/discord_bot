import discord
import os
from dotenv import load_dotenv, find_dotenv
import requests
import json 
import time

url = ""

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
    def __init__(self, thread, winner):
        self.game_list = []
        self.not_real_word = None
        self.game_string = ""
        self.thread = thread
        self.winner = winner

    def changeWord(self, message):
 
        if len(message.content) == 1:
            print(message.channel.id)
            if message.channel.id == self.thread:
                print("Letter typed: " + message.content)
                self.game_list.append(message.content)
                self.game_string = ''.join(self.game_list)            
                url = f'https://api.datamuse.com/words?sp={self.game_string}*&max=1'
                r = requests.get(url)
                data = json.loads(r.text)

                try:
                    for word in data:
                        name = word['word']
                    print(name)
                    print(self.game_string)
                    if name == self.game_string:
                        print("Someone Lost")
                        self.winner = True
                except:
                    print("not a real word")
                    self.winner = False
        else:
            self.not_real_word = True
                


class GameManager:
    def __init__(self):
        self.games = {}
    def create_game(self, name, winner):
        if name in self.games:
            raise ValueError("Game with the same name already exists.")
        game = Game(thread=name, winner=winner)
        self.games[name] = game

    def get_game(self, name):
        if name not in self.games:
            raise ValueError("Game with the given name does not exist.")
        return self.games[name]

    def delete_game(self, name):
        if name not in self.games:
            raise ValueError("Game with the given name does not exist.")
        del self.games[name]


game_manager = GameManager()

@starting.command()
async def start(ctx, player1: discord.Member, player2: discord.Member):
  thread = await ctx.channel.create_thread(name="ghost", auto_archive_duration=60, type=discord.ChannelType.private_thread)
  global thread_id
  winner = None
  thread_id = thread.id
  print(thread_id)
  current_player = player1
  await thread.add_user(player1)
  await thread.add_user(player2)
  await ctx.send(f"Thread '{thread.name}' created!")
  await thread.send(f"This is a private thread between {player1.mention} and {player2.mention}!")
  await thread.send(f"{current_player.mention}'s turn")
  game_manager.create_game(name=thread_id, winner=winner)
  currentGame = game_manager.get_game(name=thread_id)

  while not winner:
    message = await bot.wait_for('message', check=lambda m: m.author == current_player)

    currentGame.changeWord(message=message)
    await thread.send("The current word is: " + currentGame.game_string)
    current_player = player2 if current_player == player1 else player1

    if currentGame.winner == True:
        await thread.send(current_player.mention + " Won")
        break
    if currentGame.winner == False:
        await thread.send(current_player.mention + "Lost")
    if currentGame.not_real_word == True:
        await thread.send("Not a valid word")




bot.run(TOKEN)

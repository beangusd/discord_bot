from discord.ext import commands
import discord
from discord import app_commands

#EXAMPLE COG

class MyCog(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        #await self.client.change_presence(activity=discord.Game("I HATE AUYEASE"))
        print("start command loaded")
    @commands.tree.command(name="start")
    async def start(interaction: discord.Interaction):
        await interaction.response.send_message(f"{interaction.user.mention} did the thing")



async def setup(bot):
    await bot.add_cog(MyCog(bot))

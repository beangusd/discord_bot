from discord.ext import commands
import discord
from discord import app_commands

#EXAMPLE COG

intents = discord.Intents.all()

class MyCog(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        #await self.client.change_presence(activity=discord.Game("I HATE AUYEASE"))
        print("start command loaded")
        
    @commands.command()
    async def sync(self, ctx) -> None:
        fmt = await ctx.bot.tree.sync(guild=ctx.guild)

        await ctx.sned(f'Synced {len(fmt)} commands.')

    @app_commands.command(name="questions", description="questions form")
    async def questions(self, interaction: discord.Interaction, question :str):
        await interaction.response.send_message('Answered')

async def setup(bot):
    await bot.add_cog(MyCog(bot))

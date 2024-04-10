import discord
from discord import app_commands
from discord.ext import commands

from typing import Optional


class DefaultCog(commands.Cog):
    def __init__(self, bot: commands.Bot) -> None:
        self.bot = bot

    @app_commands.command(name='hello-there')
    async def hello_there(self, interaction: discord.Interaction) -> None:
        await interaction.response.send_message(f'General, {interaction.user.mention}')

    @app_commands.command(name='getting-started')
    async def getting_started(self, interaction: discord.Interaction) -> None:
        await interaction.response.send_message(f'I am only getting started')


async def setup(bot: commands.Bot) -> None:
    await bot.add_cog(DefaultCog(bot))

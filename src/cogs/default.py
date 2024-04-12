import logging

import discord
from discord import app_commands
from discord.ext import commands

from utils.time_logger import Time_logger
from utils.utils_manager import Utils_manager

logger = logging.getLogger('default-cog')
logging.basicConfig(encoding='utf-8', level=logging.INFO)


class DefaultCog(commands.Cog):
    def __init__(self, bot: commands.Bot) -> None:
        self.bot = bot

    @app_commands.command(name='hello-there', description='Is this The Star Wars reference?')
    async def hello_there(self, interaction: discord.Interaction) -> None:
        await interaction.response.send_message(f'General, {interaction.user.mention}')

    @app_commands.command(name='report-my-playtime', description='Send your gaming time as message')
    async def report_my_playtime(self, interaction: discord.Interaction) -> None:
        global logger
        ceo: Utils_manager = Utils_manager()
        user: discord.Member = None
        name: str = ''
        if interaction and interaction.user:
            user = interaction.user
            name = user.name
        time = int(ceo.time_logger.get_event_duration(
            f'{name}_playing', 's'))
        logger.info(f'DefaultCog::report_my_playtime - got time')
        logger.debug(
            f'DefaultCog::report_my_playtime - name: {name}')
        logger.debug(
            f'DefaultCog::report_my_playtime - time: {time}')

        message_str = ''
        emoji_str = ''
        command_data = ceo.constants.try_get_value_at(
            'cogs/default/commands/report_my_playtime')
        time_slices = command_data['time_slices'] if 'time_slices' in command_data else None
        negative_slice = command_data['negative_slice'] if 'negative_slice' in command_data else None
        if time <= 0:
            if negative_slice:
                ''' warning:
                    test_guild emoji in json'''
                emoji = ceo.guild_helper.get_emoji_by_name(
                    negative_slice['emoji_name'])
                if emoji:
                    emoji_str = f'<:{emoji.name}:{emoji.id}>'
                message_str = str(negative_slice['message']).format(emoji_str)
        else:
            if time_slices:
                for slice in time_slices:
                    if time > slice['time']:
                        ''' warning:
                            test_guild emoji in json'''
                        emoji = ceo.guild_helper.get_emoji_by_name(
                            slice['emoji_name'])
                        if emoji:
                            emoji_str = f'<:{emoji.name}:{emoji.id}>'
                        message_str = str(slice['message']).format(
                            time, emoji_str)
                        break
        if not message_str:
            _emoji_str = ''
            emoji = ceo.guild_helper.get_emoji_by_name('despairge')
            if emoji:
                _emoji_str = f'<:{emoji.name}:{emoji.id}>'
            message_str = f'something broke on our side {_emoji_str}'
        logger.debug((f'DefaultCog::report_my_playtime - report_my_playtime.message_str: '
                      f'{message_str}'))
        await interaction.response.send_message(message_str)
        logger.info(f'DefaultCog::report_my_playtime - sent response')


async def setup(bot: commands.Bot) -> None:
    await bot.add_cog(DefaultCog(bot))

import logging

import discord
from discord import app_commands
from discord.ext import commands

from utils.utils_manager import Utils_manager

logger = logging.getLogger('experimantal-cog')
logging.basicConfig(encoding='utf-8', level=logging.INFO)

ceo = Utils_manager()
PROD_GUILD = discord.Object(id=ceo.constants.env['PROD_GUILD_ID'])


class ExperimentalCog(commands.Cog):
    def __init__(self, bot: commands.Bot) -> None:
        self.bot = bot

    def is_test_guild(interaction: discord.Interaction) -> bool:
        global logger
        logger.debug((f'ExperimentalCog::is_test_guild: interaction.guild_id: '
                     f'{interaction.guild_id}'))
        logger.debug((f'ExperimentalCog::is_test_guild: ceo.constants.env[TEST_GUILD_ID] '
                     f'{ceo.constants.env['TEST_GUILD_ID']}'))
        return interaction.guild_id == int(ceo.constants.env['TEST_GUILD_ID'])

    @app_commands.command(name='hello-there-test', description='Is this The Star Wars reference?')
    @app_commands.check(is_test_guild)
    async def hello_there(self, interaction: discord.Interaction) -> None:
        await interaction.response.send_message(f'General, {interaction.user.mention}')

    @app_commands.command(name='report-my-playtime-test', description='Send your gaming time as message')
    @app_commands.check(is_test_guild)
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
        logger.info(f'ExperimentalCog::report_my_playtime - got time')
        logger.debug(
            f'ExperimentalCog::report_my_playtime - name: {name}')
        logger.debug(
            f'ExperimentalCog::report_my_playtime - time: {time}')

        message_str = ''
        emoji_str = ''
        command_data = ceo.constants.try_get_value_at(
            'cogs/experimental/commands/report_my_playtime')
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
        logger.debug((f'ExperimentalCog::report_my_playtime - report_my_playtime.message_str: '
                      f'{message_str}'))
        await interaction.response.send_message(message_str)
        logger.info(f'ExperimentalCog::report_my_playtime - sent response')

    @app_commands.command(name='bar-test', description='Send your gaming time as message')
    @app_commands.check(is_test_guild)
    async def bar_meister(self, interaction: discord.Interaction) -> None:
        ceo = Utils_manager()
        _emoji_str = ceo.guild_helper.get_emoji_str_by_name(
            'krutoi_perchik', False)
        message_str = f'meister {_emoji_str}{_emoji_str}{_emoji_str}'
        await interaction.response.send_message(message_str)


async def setup(bot: commands.Bot) -> None:
    await bot.add_cog(ExperimentalCog(bot))

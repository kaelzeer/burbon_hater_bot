import logging

import discord
from discord import app_commands
from discord.ext import commands

from utils.utils_manager import Utils_manager

logger = logging.getLogger('default-cog')
logging.basicConfig(encoding='utf-8', level=logging.INFO)

ceo = Utils_manager()
PROD_GUILD = discord.Object(id=ceo.constants.env['PROD_GUILD_ID'])


class DefaultCog(commands.Cog):
    def __init__(self, bot: commands.Bot) -> None:
        self.bot = bot

    def is_prod_guild(interaction: discord.Interaction) -> bool:
        logger.debug((f'DefaultCog::is_test_guild: interaction.guild_id: '
                     f'{interaction.guild_id}'))
        logger.debug((f'DefaultCog::is_test_guild: PROD_GUILD.id '
                     f'{PROD_GUILD.id}'))
        return interaction.guild_id == PROD_GUILD.id

    @commands.Cog.listener(name='on_presence_update')
    async def on_presence_update(self, before: discord.Member, after: discord.Member):
        '''
        Check for activity updated from and to playing some game.

        Works only in `Prod guild`
        '''
        if after.guild.id != PROD_GUILD.id or before.guild.id != PROD_GUILD.id:
            return
        _after_activity_type = None
        _before_activity_type = None

        if after and after.activity:
            _after_activity_type = after.activity.type
        if before and before.activity:
            _before_activity_type = before.activity.type

        if _before_activity_type != _after_activity_type:
            if _after_activity_type == discord.ActivityType.playing:
                logger.info((f'on_presence_update '
                             f'{after.name}: STARTED PLAYING'))
                logging
                ceo.time_logger.start_timer_for_event(
                    f'{after.name}_playing')
            else:
                logger.info((f'on_presence_update '
                             f'{before.name}: FINISHED PLAYING'))
                ceo.time_logger.mark_timestamp_for_event(
                    f'{before.name}_playing', True)
                logger.info(f'{ceo.time_logger.get_event_duration(
                    f'{before.name}_playing', 's')} seconds')

    @app_commands.command(name='hello-there', description='Is this The Star Wars reference?')
    @app_commands.check(is_prod_guild)
    async def hello_there(self, interaction: discord.Interaction) -> None:
        interaction.guild_id
        await interaction.response.send_message(f'General, {interaction.user.mention}')

    @app_commands.command(name='report-my-playtime', description='Send your gaming time as message')
    @app_commands.check(is_prod_guild)
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
                emoji_str = ceo.guild_helper.get_emoji_str_by_name(
                    negative_slice['emoji_name'])
                message_str = str(negative_slice['message']).format(emoji_str)
        else:
            if time_slices:
                for slice in time_slices:
                    if time > slice['time']:
                        ''' warning:
                            test_guild emoji in json'''
                        emoji_str = ceo.guild_helper.get_emoji_str_by_name(
                            slice['emoji_name'])
                        message_str = str(slice['message']).format(
                            time, emoji_str)
                        break
        if not message_str:
            _emoji_str = ''
            emoji_str = ceo.guild_helper.get_emoji_str_by_name('despairge')
            message_str = f'something broke on our side {_emoji_str}'
        logger.debug((f'DefaultCog::report_my_playtime - report_my_playtime.message_str: '
                      f'{message_str}'))
        await interaction.response.send_message(message_str)
        logger.info(f'DefaultCog::report_my_playtime - sent response')

    @app_commands.command(name='bar', description='Brewor')
    @app_commands.check(is_prod_guild)
    async def bar_meister(self, interaction: discord.Interaction) -> None:
        ceo = Utils_manager()
        _emoji_str = ceo.guild_helper.get_emoji_str_by_name(
            'krutoi_perchik')
        message_str = f'meister {_emoji_str}'
        await interaction.response.send_message(message_str)


async def setup(bot: commands.Bot) -> None:
    await bot.add_cog(DefaultCog(bot))

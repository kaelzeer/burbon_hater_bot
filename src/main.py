from dotenv import load_dotenv
from os import environ
import logging

import discord
from discord.ext import tasks, commands

from utils.utils_manager import Utils_manager


load_dotenv()
TEST_GUILD = discord.Object(id=environ['TEST_GUILD_ID'])
BOT_TOKEN = environ['TOKEN']
logger = logging.getLogger('main')
logging.basicConfig(encoding='utf-8', level=logging.INFO)

ceo = Utils_manager()


class BHBot(commands.Bot):

    async def on_ready(self):
        '''
        Print out successfull connection.

        Fetch `Test guild` by `id` in `.env` file.
        '''
        global logger
        s = f'Logged in as {self.user} :hehecat:'
        print(s)
        for _ in range(len(s)):
            print('_', end='')
        print()

        # wait until cache is populated
        await self.wait_until_ready()
        logger.info('guilds cache is populated')

        test_guild = self.get_guild(TEST_GUILD.id)
        if not test_guild:
            return

        ceo.guild_helper.set_guild(test_guild)
        for m in test_guild.members:
            self.check_initial_activity(m)

    def check_initial_activity(self, member: discord.Member) -> None:
        global ceo
        if member.activity:
            if member.activity.type == discord.ActivityType.playing:
                logger.info((f'check_initial_activity '
                             f'{member.name}: STARTED PLAYING'))
                ceo.time_logger.start_timer_for_event(
                    f'{member.name}_playing')

    async def setup_hook(self) -> None:
        '''
        Setup command tree.
        '''
        await self.load_initial_extensions()
        # test guild
        self.tree.copy_global_to(guild=TEST_GUILD)
        await self.tree.sync(guild=TEST_GUILD)

    async def on_presence_update(self, before: discord.Member, after: discord.Member):
        '''
        Check for activity updated from and to playing some game.

        Works only in `Test guild`
        '''
        if after.guild.id != TEST_GUILD.id or before.guild.id != TEST_GUILD.id:
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

    async def load_initial_extensions(self):
        cogs = ['cogs.default']
        for cog in cogs:
            await self.load_extension(cog)


intents = discord.Intents.default()
intents.message_content = True
intents.members = True
intents.guilds = True
intents.presences = True

bot = BHBot(command_prefix='/', intents=intents)
bot.run(BOT_TOKEN)

import logging

import discord
from discord.ext import tasks, commands

from utils.utils_manager import Utils_manager


logger = logging.getLogger('main')
logging.basicConfig(encoding='utf-8', level=logging.INFO)

ceo = Utils_manager()
PROD_GUILD = discord.Object(id=ceo.constants.env['PROD_GUILD_ID'])
TEST_GUILD = discord.Object(id=ceo.constants.env['TEST_GUILD_ID'])


class BHBot(commands.Bot):

    async def on_ready(self):
        '''
        Print out successfull connection.

        Fetch `Test guild` by `id` in `.env` file.
        '''
        global logger
        global ceo
        s = f'Logged in as {self.user} :hehecat:'
        print(s)
        for _ in range(len(s)):
            print('_', end='')
        print()

        # wait until cache is populated
        await self.wait_until_ready()
        logger.info('guilds cache is populated')

        test_guild = self.get_guild(TEST_GUILD.id)
        prod_guild = self.get_guild(PROD_GUILD.id)
        if not test_guild and not prod_guild:
            return

        ceo.guild_helper.set_guild(test_guild, prod_guild)
        # disable test for now:
        # for m in test_guild.members:
        #     self.check_initial_activity(m)
        for m in prod_guild.members:
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
        # clear global command palette, i guess
        await self.load_initial_extensions()
        await self.tree.sync(guild=None)
        # test guild
        # self.tree.copy_global_to(guild=TEST_GUILD)
        await self.tree.sync(guild=TEST_GUILD)
        # prod guild
        # self.tree.copy_global_to(guild=PROD_GUILD)
        await self.tree.sync(guild=PROD_GUILD)

    async def load_initial_extensions(self):
        prod_cogs = ['cogs.default']
        for cog in prod_cogs:
            await self.load_extension(cog)
        # disable experimental aka test for now:
        # test_cogs = ['cogs.experimental']
        # for cog in test_cogs:
        #     await self.load_extension(cog)


intents = discord.Intents.default()
intents.message_content = True
intents.members = True
intents.guilds = True
intents.presences = True

bot = BHBot(command_prefix='/', intents=intents)
bot.run(ceo.constants.env['BOT_TOKEN'])

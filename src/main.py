from dotenv import load_dotenv
from os import environ

import discord
from discord.ext import tasks, commands

from utils.time_logger import Time_logger


load_dotenv()

MY_GUILD = discord.Object(id=environ['TEST_GUILD_ID'])


class BHBot(commands.Bot):

    async def on_ready(self):
        '''
        Print out successfull connection.

        Fetch `Test guild` by `id` in `.env` file.
        '''
        s = f'Logged in as {self.user} :hehecat:'
        print(s)
        for _ in range(len(s)):
            print('_', end='')
        print()

        test_guild = await self.fetch_guild(MY_GUILD.id)
        if test_guild:
            print(f'test guild fetched successfully')
            print(f'g.name: {test_guild.name}')
            print(f'g.id: {test_guild.id}')
        else:
            print(f'ERR: Couldn\'t fetch the Test guild')

    async def setup_hook(self) -> None:
        '''
        Setup command tree.
        '''
        await self.load_initial_extensions()
        self.tree.copy_global_to(guild=MY_GUILD)
        await self.tree.sync(guild=MY_GUILD)

    async def on_presence_update(self, before: discord.Member, after: discord.Member):
        '''
        Check for activity updated from and to playing some game.

        Works only in `Test guild`
        '''
        if after.guild.id != MY_GUILD.id or before.guild.id != MY_GUILD.id:
            return
        _after_activity_type = None

        if after and after.activity:
            _after_activity_type = after.activity.type

        if _after_activity_type == discord.ActivityType.playing:
            print(f'on_presence_update {after.name}: STARTED PLAYING')
            Time_logger.get_instance().start_timer_for_event(
                f'{after.name}_playing')
        else:
            print(f'on_presence_update {before.name}: FINISHED PLAYING')
            Time_logger.get_instance().mark_timestamp_for_event(
                f'{before.name}_playing', True)
            print(f'{Time_logger.get_instance().get_event_duration(
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
bot_token = environ['TOKEN']
bot.run(bot_token)

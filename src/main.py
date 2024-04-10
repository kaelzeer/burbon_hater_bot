from dotenv import load_dotenv
from os import environ
import discord
from discord.ext import tasks

from utils.time_logger import Time_logger


load_dotenv()

test_guild: discord.Guild


class BHClient(discord.Client):
    async def on_ready(self):
        '''
        Print out successfull connection.

        Fetch `Test guild` by `id` in `.env` file.
        '''
        global test_guild
        s = f'Logged in as {self.user} :hehecat:'
        print(s)
        for _ in range(len(s)):
            print('_', end='')
        print()

        test_guild_id = environ['TEST_GUILD_ID']
        test_guild = await self.fetch_guild(test_guild_id)
        if test_guild:
            print(f'test guild fetched successfully')
            print(f'g.name: {test_guild.name}')
            print(f'g.id: {test_guild.id}')
        else:
            print(f'ERR: Couldn\'t fetch the Test guild')

    async def on_presence_update(self, before: discord.Member, after: discord.Member):
        '''
        Check for activity updated from and to playing some game.

        Works only in `Test guild`
        '''
        if before.guild != test_guild:
            return
        if before and after:
            _after_activity_type = None
            _before_activity_type = None

            if after.activity:
                _after_activity_type = after.activity.type
            if before.activity:
                _before_activity_type = before.activity.type

            if _after_activity_type != _before_activity_type:
                if _after_activity_type == discord.ActivityType.playing:
                    print(f'on_presence_update: PLAYING')
                    Time_logger.get_instance().start_timer_for_event(
                        f'{after.name}_playing')
                else:
                    print(f'on_presence_update: FINISHED PLAYING')
                    Time_logger.get_instance().mark_timestamp_for_event(
                        f'{after.name}_playing', True)


intents = discord.Intents.default()
intents.message_content = True
intents.members = True
intents.guilds = True
intents.presences = True

client = BHClient(intents=intents)
bot_token = environ['TOKEN']
client.run(bot_token)

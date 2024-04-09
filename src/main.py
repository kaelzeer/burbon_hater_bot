from dotenv import load_dotenv
from os import environ
import discord
from discord.ext import tasks


load_dotenv()


class BHClient(discord.Client):
    async def on_ready(self):
        global test_guild
        s = f'Logged in as {self.user} :hehecat:'
        print(s)
        for _ in range(len(s)):
            print('_', end='')
        print()

    async def on_presence_update(self, before: discord.Member, after: discord.Member):
        '''
        Check for activity updated from and to playing some game
        '''
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
                else:
                    print(f'on_presence_update: FINISHED PLAYING')


intents = discord.Intents.default()
intents.message_content = True
intents.members = True
intents.guilds = True
intents.presences = True

client = BHClient(intents=intents)
bot_token = environ['TOKEN']
client.run(bot_token)

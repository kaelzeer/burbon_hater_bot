import discord
from discord import Guild


class Guild_helper(object):

    _guild = None
    _instance = None

    def __new__(cls):
        if not cls._instance:
            cls._instance = super(Guild_helper, cls).__new__(cls)
        return cls._instance

    def set_guild(self, guild: Guild) -> None:
        self._guild = guild

    def get_emoji_by_name(self, emoji_name: str) -> discord.Emoji:
        if not self._guild:
            return
        for emoji in self._guild.emojis:
            if emoji.name == emoji_name:
                return emoji


'''
Example usage:

# through Utils_Manager aka CEO
ceo = Utils_Manager()
ceo.guild_helper

# set main Guild once
ceo.guild_helper.set_guild(guild=<..>)

emoji_str = ''
emoji = ceo.guild_helper.get_emoji_by_name(emoji_name=<..>)
if emoji:
    emoji_str = f'<:{emoji.name}:{emoji.id}>'
'''

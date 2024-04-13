import discord
from discord import Guild


class Guild_helper(object):

    _prod_guild = None
    _test_guild = None
    _instance = None

    def __new__(cls):
        if not cls._instance:
            cls._instance = super(Guild_helper, cls).__new__(cls)
        return cls._instance

    def set_guild(self, test_guild: Guild, prod_guild: Guild) -> None:
        self._test_guild = test_guild
        self._prod_guild = prod_guild

    def get_emoji_by_name(self, emoji_name: str, is_prod: bool = True) -> discord.Emoji:
        target_guild = None
        if is_prod and self._prod_guild:
            target_guild = self._prod_guild
        elif not is_prod and self._test_guild:
            target_guild = self._test_guild

        if not target_guild:
            return

        for emoji in target_guild.emojis:
            if emoji.name == emoji_name:
                return emoji

    def get_emoji_str_by_name(self, emoji_name: str, is_prod: bool = True) -> str:
        _emoji_str = ''
        _emoji = self.get_emoji_by_name(
            emoji_name, is_prod)
        if _emoji:
            _emoji_str = f'<:{_emoji.name}:{_emoji.id}>'
        return _emoji_str


'''
Example usage:

# through Utils_Manager aka CEO
ceo = Utils_Manager()
ceo.guild_helper

# set main Guild once
ceo.guild_helper.set_guild(guild=<..>)

# use this:
emoji_str = ceo.guild_helper.get_emoji_str_by_name(emoji_name=<..>)

# old way:
emoji_str = ''
emoji = ceo.guild_helper.get_emoji_by_name(emoji_name=<..>)
if emoji:
    emoji_str = f'<:{emoji.name}:{emoji.id}>'
'''

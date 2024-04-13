import json
import pathlib
from dotenv import load_dotenv
from os import environ


class Constants(object):

    _instance = None
    data = dict()
    env = dict()

    def __new__(cls):
        if not cls._instance:
            cls._instance = super(Constants, cls).__new__(cls)
        return cls._instance

    def parse_constants(self, path: str = '') -> None:
        default_path = pathlib.Path('assets/configs/constants.json').absolute()
        if not path.__len__():
            path = default_path
        else:
            path = pathlib.Path(path).absolute

        with open(path, 'r') as f:
            data = json.load(f)
            self.data = data

    def parse_dotenv(self) -> None:
        load_dotenv()
        self.env['BOT_TOKEN'] = environ['TOKEN']
        self.env['TEST_GUILD_ID'] = environ['TEST_GUILD_ID']
        self.env['PROD_GUILD_ID'] = environ['PROD_GUILD_ID']

    def try_get_value_at(self, path: str = '') -> dict | None:
        paths_list = path.split('/')
        error_caused = False
        needed_data = self.data.copy()
        for i in range(len(paths_list) - 1):
            if not paths_list[i] in needed_data:
                error_caused = True
            else:
                needed_data = needed_data[paths_list[i]]
        if not error_caused:
            return needed_data[paths_list[len(paths_list) - 1]]
        else:
            return None


'''
Example usage:

# through Utils_Manager aka CEO
ceo = Utils_Manager()
ceo.guild_helper

# parse once (you can choose custom path)
ceo.constants.parse_constants(path=<..>)

# you can get rid of `if key in json[key]` check:
if 'key_1' in data and 'key_2' in data['key_1'] and 'key_3' in data['key_2']:
    data = ceo.constants.data['key_1']['key_2']['key_3']

# by using`try_get_value_at()` method:
data = ceo.constants.try_get_value_at(path='key_1/key_2/key_3')
'''

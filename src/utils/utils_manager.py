from utils.guild_helper import Guild_helper
from utils.constants import Constants
from utils.time_logger import Time_logger


class Utils_manager(object):

    _instance = None
    guild_helper: Guild_helper = None
    constants: Constants = None
    time_logger: Time_logger = None

    def __new__(cls):
        if not cls._instance:
            cls._instance = super(Utils_manager, cls).__new__(cls)
            cls.guild_helper = Guild_helper()
            cls.constants = Constants()
            cls.time_logger = Time_logger()

            cls.constants.parse_dotenv()
            cls.constants.parse_constants()
        return cls._instance

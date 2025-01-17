import json
from logging import Logger

from disnake.abc import MISSING
from disnake.ext.commands import Bot as OriginalBot
from lavalink import Client

from core.sources.source import SourceManager


class Bot(OriginalBot):
    def __init__(self, logger: Logger, **kwargs):
        super().__init__(**kwargs)

        self.logger = logger

        self.lavalink: Client = MISSING

        with open("configs/icons.json", "r", encoding="utf-8") as f:
            self.icons = json.load(f)

    async def on_ready(self):
        self.logger.info("The bot is ready! Logged in as %s" % self.user)

        self.__setup_lavalink_client()

    def __setup_lavalink_client(self):
        """
        Sets up the lavalink client for the bot
        :return: Lavalink Client
        """
        self.logger.info("Setting up lavalink client...")

        self.lavalink = Client(self.user.id)

        self.logger.info("Loading lavalink nodes...")

        with open("configs/lavalink.json", "r") as f:
            config = json.load(f)

        for node in config['nodes']:
            self.logger.debug("Adding lavalink node %s", node['host'])

            self.lavalink.add_node(**node)

        self.logger.info("Done loading lavalink nodes!")

        self.lavalink.register_source(SourceManager())

    def get_text(self, key: str, locale: str, default: str = None) -> str:
        """
        Gets a text from i18n files by key
        :param key: The key of the text
        :param locale: The locale of the text
        :param default: The default value to return if the text is not found
        :return: The text
        """
        return self.i18n.get(key).get(locale, default)

    def get_icon(self, name: str, default: any) -> any:
        """
        Get an icon
        :param name: The name of the icon
        :param default: The default value to return if the icon is not found
        :return: The icon
        """
        dct = self.icons.copy()

        for key in name.split("."):
            try:
                dct = dct[key]
            except KeyError:
                return default

        return dct

import unittest
import discord
from unittest.mock import MagicMock, mock_open
from cogs.welcome_cog import WelcomeCog
from discord.ext import commands

class TestWelcomeCog(unittest.TestCase):
    def setUp(self):
        intents = discord.Intents.default()
        intents.message_content = True
        self.bot = commands.Bot(command_prefix='?', intents=intents)
        
        self.welcome_cog = WelcomeCog(self.bot)
        self.member_mock = MagicMock()
        self.channel_mock = MagicMock()

    def test_check_first_join_new_member(self):
        with unittest.mock.patch('builtins.open', mock_open(read_data='')):
            result = self.welcome_cog.check_first_join('123456789')
            self.assertTrue(result)

    def test_check_first_join_existing_member(self):
        with unittest.mock.patch('builtins.open', mock_open(read_data='123456789\n')):
            result = self.welcome_cog.check_first_join('123456789')
            self.assertFalse(result)

    # Additional tests for on_member_join with mocked member and channel objects

if __name__ == '__main__':
    unittest.main()
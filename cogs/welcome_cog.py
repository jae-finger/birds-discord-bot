import discord
from discord.ext import commands

class WelcomeCog(commands.Cog, name='Welcome Cog'):
    def __init__(self, bot):
        self.bot = bot

    def check_first_join(self, member_id, file_path='data/members.txt'):
        with open(file_path, 'a+') as file:
            file.seek(0)
            members = file.read().splitlines()
            if member_id not in members:
                file.write(f'{member_id}\n')
                return True
            return False

    @commands.Cog.listener()
    async def on_member_join(self, member):
        if self.check_first_join(str(member.id)):
            welcome_message = f'Welcome to the save the birds! discord, {member.mention}!'
            # Specify the channel name here
            channel_name = 'general'
            channel = discord.utils.get(member.guild.channels, name=channel_name)
            if channel:
                await channel.send(welcome_message)

def setup(bot):
    bot.add_cog(WelcomeCog(bot))

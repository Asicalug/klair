import discord

from discord.ext import commands
from discord.commands import SlashCommandGroup, Option

intents = discord.Intents.default()
intents.members = True
intents.messages = True
intents.message_content = True
bot = commands.Bot(intents=intents)

class EtaAutoResponse(commands.Cog):
    def __init__(self, bot: commands.Bot) -> None:
        self.bot = bot
        print(f"{self.__class__.__name__} loaded")
        
    @bot.event
    async def on_message(message):
        if 'eta' in message.content:
            await message.reply("The fuckin client is not released yet bitch")

def setup(bot: commands.Bot):
    bot.add_cog(EtaAutoResponse(bot))
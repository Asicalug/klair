from discord.ext import commands
import discord

class UserCommands(commands.Cog):
    def __init__(self, bot: commands.Bot) -> None:
        self.bot = bot
        print(f"{self.__class__.__name__} loaded")
    
    @commands.slash_command()
    async def ping(self, ctx: discord.ApplicationCommand):
        await ctx.response.send_message(f"Pong! {round(self.bot.latency * 1000)}ms")

    
def setup(bot: commands.Bot):
    bot.add_cog(UserCommands(bot))
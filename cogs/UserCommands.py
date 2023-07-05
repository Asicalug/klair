from discord.ext import commands
import discord

class UserCommands(commands.Cog):
    def __init__(self, bot: commands.Bot) -> None:
        self.bot = bot
        print(f"{self.__class__.__name__} loaded")
    
    @commands.command()
    async def ping(
        self,
        ctx : discord.ApplicationContext
    ):
        embed=discord.Embed(title='Pong !', description=f'My ping is {round(self.bot.latency * 1000)}ms')
        await ctx.send(embed=embed)

    
def setup(bot: commands.Bot):
    bot.add_cog(UserCommands(bot))
from discord.ext import commands
import discord
from discord.commands import Option
from discord.ui import View, Button
 
from views.AcceptLinkView import YesLinkAccount
from views.DenyLinkView import NoLinkAccount

from mojang import API
api = API()

class UserCommands(commands.Cog):
    def __init__(self, bot: commands.Bot) -> None:
        self.bot = bot
        print(f"{self.__class__.__name__} loaded")
    
    @commands.slash_command()
    async def ping(self, ctx: discord.ApplicationCommand):
        await ctx.response.send_message(f"Pong! {round(self.bot.latency * 1000)}ms")

    @commands.slash_command()
    async def link(
        self,
        ctx: discord.ApplicationCommand,
        username : Option(str)
    ):
        uuid = api.get_uuid(f"{username}")
        member = ctx.guild.get_member(ctx.user.id)
        self.bot.settings.set(f"Link.Username.{member.id}", username) # type: ignore
        if not uuid:
            embed = discord.Embed(title="Error !", description="Username doesn't exist.\n*Keep in mind that this doesn't work with cracked accounts*")
            await ctx.send_response(embed=embed, ephemeral=True)
        else:
            embed = discord.Embed(title='Is This You ?', description='Confirm that this Minecraft account belongs to you.', color=discord.Color.yellow())
            embed.add_field(name="Minecraft Username", value=f"{username}")
            embed.set_thumbnail(url=f"https://visage.surgeplay.com/bust/128/{uuid}")
            view = View()
            view.add_item(YesLinkAccount(bot=self.bot))
            view.add_item(NoLinkAccount(bot=self.bot))
            await ctx.send_response(embed=embed, view=view, ephemeral=True)


    @commands.slash_command()
    async def unlink(
        self,
        ctx: discord.ApplicationCommand,
    ):
        member = ctx.guild.get_member(ctx.user.id)
        username = self.bot.settings.get(f"Link.Username.{member.id}") # type: ignore
        uuid = api.get_uuid(f"{username}")
        await member.edit(nick=None)
        embed = discord.Embed(title='Account Unlinked !', description='Your Minecraft account has been unlinked', color=discord.Color.yellow())
        embed.set_thumbnail(url=f"https://visage.surgeplay.com/bust/128/{uuid}")
        await ctx.send_response(embed=embed, ephemeral=True)
        channel = self.bot.get_channel(self.bot.settings.get("Logs.Channel"))
        await channel.send(f"<@{ctx.user.id}> unlinked their account ({username})")
    
def setup(bot: commands.Bot):
    bot.add_cog(UserCommands(bot))
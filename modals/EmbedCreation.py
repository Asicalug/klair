import discord
import traceback
from discord.interactions import Interaction

class EmbedCreation(discord.ui.Modal):
    def __init__(self, bot, title="Send an Embeded text", *args, **kwargs):
        self.bot = bot
        super().__init__(
            discord.ui.InputText(
                label="Title",
                placeholder="Title",
                max_length=50,
                style=discord.InputTextStyle.short
            ),
            discord.ui.InputText(
                label="Description",
                placeholder="Description",
                max_length=4000,
                style=discord.InputTextStyle.long
            ),
            title=title,
            *args,
            **kwargs
        )


    async def callback(self, interaction: discord.Interaction):
        embed = discord.Embed(title=self.children[0].value, description=self.children[1].value, color=discord.Color.blurple())
        embed.set_author(name=interaction.user, icon_url=interaction.user.display_avatar) # type: ignore
        embed.timestamp = discord.utils.utcnow() # type: ignore
        await interaction.channel.send(embed=embed)
        await interaction.response.send_message("Embed Sent", ephemeral=True)

    async def on_error(self, error: Exception, interaction: Interaction):
        embed = discord.Embed(title="An Error occured", description="Please screenshot the Error Message and report it to a Staff Member", color=discord.Color.red())
        embed.add_field(name="Error", value=f"```\n{error}\n```")
        await interaction.response.send_message(embed=embed, ephemeral=True)
        traceback.print_exception(type(error), error, error.__traceback__)
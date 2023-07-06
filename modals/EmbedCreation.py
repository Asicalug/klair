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
            discord.ui.InputText(
                label="Red (r)",
                placeholder="00",
                max_length=2,
                style=discord.InputTextStyle.short
            ),
            discord.ui.InputText(
                label="Red (g)",
                placeholder="00",
                max_length=2,
                style=discord.InputTextStyle.short
            ),
            discord.ui.InputText(
                label="Red (b)",
                placeholder="00",
                max_length=2,
                style=discord.InputTextStyle.short
            ),
            title=title,
            *args,
            **kwargs
        )


    async def callback(self, interaction: discord.Interaction):
        embed = discord.Embed(title=self.children[0].value, description=self.children[1].value, color=discord.Color.from_rgb(self.children[2].value, self.children[3].value, self.children[4].value))
        embed.set_author(name=interaction.user, icon_url=interaction.user.display_avatar) # type: ignore
        embed.timestamp = discord.utils.utcnow() # type: ignore
        await interaction.channel.send(embed=embed)
        await interaction.response.send_message("Embed Sent", ephemeral=True)

    async def on_error(self, error: Exception, interaction: Interaction):
        embed = discord.Embed(title="An Error occured", description="Please screenshot the Error Message and report it to a Staff Member", color=discord.Color.red())
        embed.add_field(name="Error", value=f"```\n{error}\n```")
        await interaction.response.send_message(embed=embed, ephemeral=True)
        traceback.print_exception(type(error), error, error.__traceback__)
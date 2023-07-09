import discord
import traceback
from discord.interactions import Interaction

class SuggestionModal(discord.ui.Modal):
    def __init__(self, bot, title="Create a Suggestion", *args, **kwargs):
        self.bot = bot
        super().__init__(
            discord.ui.InputText(
                label="Suggestion",
                placeholder="Your Suggestion",
                max_length=500,
                style=discord.InputTextStyle.long
            ),
            title=title,
            *args,
            **kwargs
        )

    async def callback(self, interaction: discord.Interaction):
        embed = discord.Embed(description=self.children[0].value, color=discord.Color.blurple())
        embed.set_author(name=interaction.user, icon_url=interaction.user.display_avatar) # type: ignore
        embed.timestamp = discord.utils.utcnow() # type: ignore
        channel = self.bot.get_channel(self.bot.settings.get("Suggestions.NewSuggestion")) # type: ignore
        msg = await channel.send(embed=embed)
        await msg.add_reaction("👍")
        await msg.add_reaction("👎")
        await interaction.response.send_message("Suggestion created", ephemeral=True)
        channel = self.bot.get_channel(self.bot.settings.get("Logs.Channel"))
        await channel.send(f"{interaction.user} sent a suggestion")

    async def on_error(self, error: Exception, interaction: Interaction):
        embed = discord.Embed(title="An Error occured", description="Please screenshot the Error Message and report it to a Staff Member", color=discord.Color.red())
        embed.add_field(name="Error", value=f"```\n{error}\n```")
        await interaction.response.send_message(embed=embed, ephemeral=True)
        traceback.print_exception(type(error), error, error.__traceback__)

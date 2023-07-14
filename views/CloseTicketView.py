import discord
from discord.ui import Button, View

class CloseTicket(Button):
    def __init__(self, bot) -> None:
        super().__init__(style=discord.ButtonStyle.danger, label="Close 🔒")
        self.bot = bot

    async def callback(self, interaction: discord.Interaction):
        guild = interaction.guild
        channel = discord.TextChannel(guild=guild)
        await channel.delete()

        embed = discord.Embed(title="Closed!", description="The ticket has been successfully closed.", color=discord.Color.green())
        await interaction.response.send_message(embed=embed, ephemeral=True)
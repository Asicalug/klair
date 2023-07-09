import discord
from discord.ui import Button, View

class YesLinkAccount(Button):
    def __init__(self, bot) -> None:
        super().__init__(style=discord.ButtonStyle.success, label="Yes")
        self.bot = bot

    async def callback(self, interaction: discord.Interaction):
        member = interaction.guild.get_member(interaction.user.id)
        username = self.bot.settings.get(f"Link.Username.{member}")
        await member.edit(nick=f"@{interaction.user.display_name} ({username})")

        embed = discord.Embed(title="Linked!", description="Your account has been successfully linked.", color=discord.Color.green())
        await interaction.response.send_message(embed=embed, ephemeral=True)
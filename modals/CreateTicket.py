import discord
import traceback
from discord.interactions import Interaction
import discord.guild
from discord.ui import View, Button

from views.CloseTicketView import CloseTicket


class TicketModal(discord.ui.Modal):
    def __init__(self, bot, title="Create a Ticket", *args, **kwargs):
        self.bot = bot
        super().__init__(
            discord.ui.InputText(
                label="Ticket",
                placeholder="Your Support Prompt",
                max_length=500,
                style=discord.InputTextStyle.long
            ),
            title=title,
            *args,
            **kwargs
        )

    async def callback(self, interaction: discord.Interaction):
        overwrites = {
             interaction.guild.default_role: discord.PermissionOverwrite(read_messages=False),
             interaction.guild.me: discord.PermissionOverwrite(read_messages=True),
             interaction.user: discord.PermissionOverwrite(read_messages=True), 
        }
        embed = discord.Embed(description=self.children[0].value, color=discord.Color.blurple())
        embed.set_author(name=interaction.user.name, icon_url=interaction.user.display_avatar) # type: ignore
        embed.timestamp = discord.utils.utcnow() # type: ignore
        guild = interaction.guild
        category = discord.utils.get(guild.categories, id=self.bot.settings.get("Tickets.Category"))
        channel = await guild.create_text_channel(name=f"ticket-{interaction.user}", category=category, overwrites=overwrites)
        await channel.send(embed=embed, view=CloseTicket(bot=self.bot))
        self.bot.settings.set(f"Tickets.UserChannel.{interaction.user.id}", channel.id) # type: ignore
        channel1 = self.bot.get_channel(self.bot.settings.get("Logs.Channel"))
        await channel1.send(f"{interaction.user} Created a ticket")

    async def on_error(self, error: Exception, interaction: Interaction):
        embed = discord.Embed(title="An Error occured", description="Please screenshot the Error Message and report it to a Staff Member", color=discord.Color.red())
        embed.add_field(name="Error", value=f"```\n{error}\n```")
        await interaction.response.send_message(embed=embed, ephemeral=True)
        traceback.print_exception(type(error), error, error.__traceback__)

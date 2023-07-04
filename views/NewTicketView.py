import discord

from modals.CreateTicket import TicketModal

class CreateTicket(discord.ui.View):
    def __init__(self, bot) -> None:
        super().__init__(timeout=None)
        self.bot = bot

    @discord.ui.button(label="Create a Ticket", style=discord.ButtonStyle.primary, custom_id="create_ticket", emoji="🤔")
    async def button_callback(self, button, interaction):
        if "Ticket Ban" in [role.name for role in interaction.user.roles]:
            return await interaction.response.send_message("You are banned from creating Tickets", ephemeral=True)
        await interaction.response.send_modal(TicketModal(bot=self.bot))


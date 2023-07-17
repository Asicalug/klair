import discord

from modals.CreateApplication import ApplicationModal

class CreateApplication(discord.ui.View):
    def __init__(self, bot) -> None:
        super().__init__(timeout=None)
        self.bot = bot

    @discord.ui.button(label="Create an Application", style=discord.ButtonStyle.primary, custom_id="create_application")
    async def button_callback(self, button, interaction : discord.Interaction):
        if "Applications Ban" in [role.name for role in interaction.user.roles]:
            return await interaction.response.send_message("You are banned from creating Applications", ephemeral=True)
        await interaction.response.send_modal(ApplicationModal(bot=self.bot))
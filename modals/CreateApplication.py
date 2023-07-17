import discord
import traceback
from discord.interactions import Interaction

class ApplicationModal(discord.ui.Modal):
    def __init__(self, bot, title="Create an Application", *args, **kwargs):
        self.bot = bot
        super().__init__(
            discord.ui.InputText(
                label="First and Last Name",
                placeholder="John Doe",
                max_length=100,
                style=discord.InputTextStyle.short,
            ),
            discord.ui.InputText(
                label="Age",
                placeholder="15",
                max_length=3,
                min_length=1,
                style=discord.InputTextStyle.short,
            ),
            discord.ui.InputText(
                label="How active can you be?",
                placeholder="6-8am",
                max_length=10,
                style=discord.InputTextStyle.short,
            ),
            discord.ui.InputText(
                label="What's your experience ?",
                placeholder="If none, leave this blank",
                max_length=2000,
                style=discord.InputTextStyle.paragraph,
                required=False,
            ),
            discord.ui.InputText(
                label="Why you ?",
                placeholder="Because...\n*At least 100 characters.*",
                max_length=4000,
                min_length=100,
                style=discord.InputTextStyle.long,
                required=True,
            ),
            discord.ui.InputText(
                label="Vouchers",
                placeholder="If you don't have any leave this blank",
                max_length=500,
                required=False
            ),
            title=title,
            *args,
            **kwargs
        )

    async def callback(self, interaction: discord.Interaction):
        log = self.bot.get_channel(self.bot.settings.get("Logs.Channel"))
        channel = self.bot.get_channel(self.bot.settings.get("Applications.Channel"))
        embed = discord.Embed(title=f"Application From {interaction.user.mention}", description="Requirements :\n- 1. Has To Be 13 at least.\n- 2. Has To Have a Good Spelling.\n- 3. Has To Be Able To Speak English Fluently.")
        embed.add_field(name="First and Last Name", value=self.children[0].value, inline=False)
        embed.add_field(name="Age", value=self.children[1].value, inline=False)
        embed.add_field(name="How active can they be", value=self.children[2].value, inline=False)
        embed.add_field(name="Experience", value=self.children[3].value, inline=False)
        embed.add_field(name="Why should we choose them", value=self.children[4].value, inline=False)
        embed.set_author(name=interaction.user.name, icon_url=interaction.user.display_avatar)
        await channel.send(embed=embed)
        await interaction.response.send_message("Application created", ephemeral=True)
        await log.send(f"<@{interaction.user.id}> created an application.")
    async def on_error(self, error: Exception, interaction: Interaction):
        embed = discord.Embed(title="An Error occured", description="Please screenshot the Error Message and report it to a Staff Member", color=discord.Color.red())
        embed.add_field(name="Error", value=f"```\n{error}\n```")
        await interaction.response.send_message(embed=embed, ephemeral=True)
        traceback.print_exception(type(error), error, error.__traceback__)
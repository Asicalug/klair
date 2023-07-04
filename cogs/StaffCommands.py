import discord

from discord.ext import commands
from discord.commands import SlashCommandGroup, Option

from views.NewSuggestionView import CreateSuggestion
from views.NewTicketView import CreateTicket

class StaffCommands(commands.Cog):
    def __init__(self, bot: commands.Bot) -> None:
        self.bot = bot
        print(f"{self.__class__.__name__} loaded")

    setup = SlashCommandGroup(name="setup", description="Various Setup Commands")
    
    @setup.command(name="suggestions", description="Sets up Suggestions")
    async def setup_suggestions(
        self,
        ctx: discord.ApplicationContext,
        panel: Option(discord.TextChannel, "The Channel to send the \"Create a Suggestion\" Panel"), # type: ignore
        suggestion: Option(discord.TextChannel, "The Channel to send the created Suggestion in") # type: ignore
    ):
        if self.bot.settings.get("Suggestions.Panel") != None: # type: ignore
            try:
                channel = await self.bot.fetch_channel(self.bot.settings.get("Suggestions.Panel")) # type: ignore
                message = await channel.history().find(lambda m: m.author == self.bot.user) # type: ignore
                await message.delete() # type: ignore
            except:
                pass
        
        self.bot.settings.set("Suggestions.Panel", panel.id) # type: ignore
        self.bot.settings.set("Suggestions.NewSuggestion", suggestion.id) # type: ignore
        await panel.send(embed=discord.Embed(title="Create a Suggestion", description="Click the button below to create a suggestion"), view=CreateSuggestion(bot=self.bot))
        embed = discord.Embed(title="Setup", description="Suggestion successfully setup")
        embed.add_field(name="Panel Channel", value=panel.mention)
        embed.add_field(name="Suggestion Channel", value=suggestion.mention)
        await ctx.respond(embed=embed)

    @setup.command(name="tickets", description="Sets up Tickets")
    async def setup_tickets(
        self,
        ctx: discord.ApplicationContext,
        panel: Option(discord.TextChannel, "The Channel to send the \"Create a Ticket\" Panel"),
        ticket: Option(discord.CategoryChannel, "The Category to create the Ticket Channel in") 
    ):
        if self.bot.settings.get("Tickets.Panel") != None: # type: ignore
            try:
                channel = await self.bot.fetch_channel(self.bot.settings.get("Tickets.Panel")) # type: ignore
                message = await channel.history().find(lambda m: m.author == self.bot.user) # type: ignore
                await message.delete() # type: ignore
            except:
                pass
        
        self.bot.settings.set("Tickets.Panel", panel.id) # type: ignore
        self.bot.settings.set("Tickets.Category", ticket.id) # type: ignore
        await panel.send(embed=discord.Embed(title="Create a Ticket", description="Click the button below to create a suggestion"), view=CreateTicket(bot=self.bot))
        embed = discord.Embed(title="Setup", description="Ticket Creator successfully setup")
        embed.add_field(name="Panel Channel", value=panel.mention)
        embed.add_field(name="Ticket Category", value=ticket.mention)
        await ctx.respond(embed=embed)


        
    
def setup(bot: commands.Bot):
    bot.add_cog(StaffCommands(bot))

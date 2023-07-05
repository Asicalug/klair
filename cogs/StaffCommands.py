import discord

from discord.ext import commands, has_permissions, MissingPermissions
from discord.commands import SlashCommandGroup, Option, SlashCommand

from views.NewSuggestionView import CreateSuggestion
from views.NewTicketView import CreateTicket

class StaffCommands(commands.Cog):
    def __init__(self, bot: commands.Bot) -> None:
        self.bot = bot
        print(f"{self.__class__.__name__} loaded")

    setup = SlashCommandGroup(name="setup", description="Various Setup Commands")
    embed = SlashCommandGroup(name="embed", description="Various Embed Commands")
    

    @setup.command(name="suggestions", description="Sets up Suggestions")
    @commands.has_permissions(manage_channels=True)
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
    @commands.has_permissions(manage_channels=True)
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

@setup_tickets.error
async def kick_error(ctx, error):
    if isinstance(error, MissingPermissions):
        text = "Sorry {}, you do not have permissions to do that!".format(ctx.message.author)
        await bot.send_message(ctx.message.channel, text)   

    @embed.command(name="rules", description="Sends Rules Embed")
    @commands.has_permissions(manage_messages = True)
    async def embedrules(
        self,
        ctx: discord.ApplicationContext,
    ):
        embed1 = discord.Embed(title="Klair", description="Welcome to the Official Discord Server of Klair Client. We are pleased to have you in our journey :D. Before continuing please read the rules and obey them, any user who breaks the rules is going to face some consequences (that is, ban, mute). NOTE: This Discord Server's Layout is inspired by Hybris.", color=discord.Color.red())
        embed1.set_footer(icon_url="https://asicalug.netlify.app/storage/klair.png",)
        embed2 = discord.Embed(url="https://discord.gg/Hybris", title="Hybris' Discord", color=discord.Color.red())
        embed3 = discord.Embed(title="", color=discord.Color.red())
        embed3.set_image(url="https://media.discordapp.net/attachments/1120373785967738880/1121014281727639684/Klair_Rules.png?width=1040&height=585")
        embed4 = discord.Embed(description="Check out the Rules before Starting Your Journey In our Discord Server - Klair", title="", color=discord.Color.red())
        embed5 = discord.Embed(title="", description="Remember, the rules are applied to all the behaviour on the server including Moderators and Staffs. If you See anyone breaking the Rules, report it to any online Staff/Mod.", color=discord.Color.red())
        embed5.add_field(name="Rules", value="* 1. Be Respectful and dont be mean to others :D\n\n* 2. No Spamming\n\n* 3. No Advertising,\n\n* 4. No Threatening\n\n* 5. Dont share any personal information\n\n* 6. Be a good person :D")
        await ctx.send_response(embeds=(embed1, embed2, embed3, embed4, embed5))

        
    
def setup(bot: commands.Bot):
    bot.add_cog(StaffCommands(bot))

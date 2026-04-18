import discord
from discord.ext import commands
from discord import app_commands
from discord.ui import View, Button

TICKET_CATEGORY_NAME = "🎫 Tickets"
TICKET_LOG_CHANNEL_ID = 0  # <-- Vul hier je logkanaal ID in
STAFF_ROLE_NAME = "Staff"  # <-- Alleen deze rol krijgt toegang

# -----------------------------
# VIEW: Ticket openen
# -----------------------------
class TicketView(View):
    def __init__(self, bot):
        super().__init__(timeout=None)
        self.bot = bot

    @discord.ui.button(label="Open Ticket", style=discord.ButtonStyle.green, emoji="🎫")
    async def open_ticket(self, interaction: discord.Interaction, button: Button):

        guild = interaction.guild

        # Zoek of maak categorie
        category = discord.utils.get(guild.categories, name=TICKET_CATEGORY_NAME)
        if category is None:
            category = await guild.create_category(TICKET_CATEGORY_NAME)

        # Check of gebruiker al een ticket heeft
        existing = discord.utils.get(guild.channels, name=f"ticket-{interaction.user.id}")
        if existing:
            return await interaction.response.send_message(
                f"❌ Je hebt al een ticket open: {existing.mention}",
                ephemeral=True
            )

        # Zoek staff rol
        staff_role = discord.utils.get(guild.roles, name=STAFF_ROLE_NAME)

        # Kanaal perms
        overwrites = {
            guild.default_role: discord.PermissionOverwrite(read_messages=False),
            interaction.user: discord.PermissionOverwrite(read_messages=True, send_messages=True),
            guild.me: discord.PermissionOverwrite(read_messages=True, send_messages=True)
        }

        # Staff rol toegang geven
        if staff_role:
            overwrites[staff_role] = discord.PermissionOverwrite(
                read_messages=True,
                send_messages=True
            )

        # Maak ticket kanaal
        channel = await guild.create_text_channel(
            name=f"ticket-{interaction.user.id}",
            category=category,
            overwrites=overwrites
        )

        await interaction.response.send_message(
            f"🎫 Ticket geopend: {channel.mention}",
            ephemeral=True
        )

        embed = discord.Embed(
            title="🎫 Ticket geopend",
            description="Leg hieronder je vraag of probleem uit.\nEen stafflid zal zo snel mogelijk reageren.",
            color=discord.Color.green()
        )

        await channel.send(embed=embed, view=CloseTicketView(self.bot))

        # Log
        if TICKET_LOG_CHANNEL_ID != 0:
            log = guild.get_channel(TICKET_LOG_CHANNEL_ID)
            if log:
                await log.send(f"📥 Ticket geopend door **{interaction.user}** → {channel.mention}")


# -----------------------------
# VIEW: Ticket sluiten
# -----------------------------
class CloseTicketView(View):
    def __init__(self, bot):
        super().__init__(timeout=None)
        self.bot = bot

    @discord.ui.button(label="Sluit Ticket", style=discord.ButtonStyle.red, emoji="🔒")
    async def close_ticket(self, interaction: discord.Interaction, button: Button):

        channel = interaction.channel

        await interaction.response.send_message("🔒 Ticket wordt gesloten...", ephemeral=True)

        # Log
        if TICKET_LOG_CHANNEL_ID != 0:
            log = interaction.guild.get_channel(TICKET_LOG_CHANNEL_ID)
            if log:
                await log.send(f"🔒 Ticket gesloten: {channel.name}")

        await channel.delete()


# -----------------------------
# COG
# -----------------------------
class Tickets(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(name="ticketpanel", description="Plaats het ticket panel")
    async def ticketpanel(self, interaction: discord.Interaction):

        embed = discord.Embed(
            title="🎫 Support Tickets",
            description="Klik op de knop hieronder om een ticket te openen.",
            color=discord.Color.blue()
        )

        await interaction.channel.send(embed=embed, view=TicketView(self.bot))
        await interaction.response.send_message("Ticket panel geplaatst!", ephemeral=True)


async def setup(bot):
    await bot.add_cog(Tickets(bot))

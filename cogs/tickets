import discord
from discord.ext import commands
from discord import app_commands
from discord.ui import View, Button

# -----------------------------
# Ticket View (knoppen)
# -----------------------------
class TicketView(View):
    def __init__(self, bot, ticket_type):
        super().__init__(timeout=None)
        self.bot = bot
        self.ticket_type = ticket_type

    @discord.ui.button(label="Open Ticket", style=discord.ButtonStyle.green)
    async def open_ticket(self, interaction: discord.Interaction, button: Button):
        guild = interaction.guild
        user = interaction.user

        # Rollen ophalen
        staff_role = discord.utils.get(guild.roles, name="Staff")
        mod_role = discord.utils.get(guild.roles, name="Moderatie team")

        # Als rollen niet bestaan → foutmelding
        if staff_role is None or mod_role is None:
            return await interaction.response.send_message(
                "❌ Rollen **Staff** en **Moderatie team** moeten bestaan.",
                ephemeral=True
            )

        # Kanaalrechten
        overwrites = {
            guild.default_role: discord.PermissionOverwrite(view_channel=False),
            user: discord.PermissionOverwrite(view_channel=True, send_messages=True),
            staff_role: discord.PermissionOverwrite(view_channel=True, send_messages=True),
            mod_role: discord.PermissionOverwrite(view_channel=True, send_messages=True),
        }

        # Ticketkanaal maken
        ticket_channel = await guild.create_text_channel(
            name=f"{self.ticket_type}-{user.name}",
            overwrites=overwrites
        )

        # Embed in ticket
        embed = discord.Embed(
            title=f"{self.ticket_type.capitalize()} Ticket",
            description=f"{user.mention}, welkom in je ticket.\nEen teamlid komt zo snel mogelijk bij je.",
            color=discord.Color.blue()
        )

        await ticket_channel.send(embed=embed)

        await interaction.response.send_message(
            f"🎫 Ticket geopend: {ticket_channel.mention}",
            ephemeral=True
        )


# -----------------------------
# Tickets Cog
# -----------------------------
class Tickets(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(name="ticket-panels", description="Plaats alle ticket panels")
    async def ticket_panels(self, interaction: discord.Interaction):
        await interaction.response.send_message("Panels worden geplaatst...", ephemeral=True)

        # -----------------------------
        # Sollicitatie Panel
        # -----------------------------
        embed_s = discord.Embed(
            title="📄 Sollicitatie Panel",
            description="Klik op de knop hieronder om een sollicitatie-ticket te openen.",
            color=discord.Color.green()
        )
        await interaction.channel.send(
            embed=embed_s,
            view=TicketView(self.bot, "sollicitatie")
        )

        # -----------------------------
        # Support Panel
        # -----------------------------
        embed_sup = discord.Embed(
            title="🎧 Support Panel",
            description="Klik op de knop hieronder om een support-ticket te openen.",
            color=discord.Color.blue()
        )
        await interaction.channel.send(
            embed=embed_sup,
            view=TicketView(self.bot, "support")
        )

        # -----------------------------
        # Staff Panel
        # -----------------------------
        embed_st = discord.Embed(
            title="🛠 Staff Panel",
            description="Klik op de knop hieronder om een staff-ticket te openen.",
            color=discord.Color.orange()
        )
        await interaction.channel.send(
            embed=embed_st,
            view=TicketView(self.bot, "staff")
        )


async def setup(bot):
    await bot.add_cog(Tickets(bot))

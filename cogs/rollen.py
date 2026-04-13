import discord
from discord.ext import commands
from discord import app_commands
from discord.ui import View, Button

# -----------------------------
# Helper: rol ophalen of maken
# -----------------------------
async def get_or_create_role(guild, name, colour=discord.Colour.blue()):
    role = discord.utils.get(guild.roles, name=name)
    if role is None:
        role = await guild.create_role(name=name, colour=colour)
    return role


# -----------------------------
# VIEW: Minecraft rollen panel
# -----------------------------
class MCRollenView(View):
    def __init__(self, bot):
        super().__init__(timeout=None)
        self.bot = bot

    @discord.ui.button(label="Bedrock", style=discord.ButtonStyle.green)
    async def bedrock(self, interaction: discord.Interaction, button: Button):
        role = await get_or_create_role(interaction.guild, "Bedrock", discord.Colour.green())
        await interaction.user.add_roles(role)
        await interaction.response.send_message("✔ Je hebt de **Bedrock** rol gekregen!", ephemeral=True)

    @discord.ui.button(label="Java", style=discord.ButtonStyle.blurple)
    async def java(self, interaction: discord.Interaction, button: Button):
        role = await get_or_create_role(interaction.guild, "Java", discord.Colour.blue())
        await interaction.user.add_roles(role)
        await interaction.response.send_message("✔ Je hebt de **Java** rol gekregen!", ephemeral=True)

    @discord.ui.button(label="Aankondiging melding", style=discord.ButtonStyle.gray)
    async def aankondiging(self, interaction: discord.Interaction, button: Button):
        role = await get_or_create_role(interaction.guild, "Aankondiging melding", discord.Colour.orange())
        await interaction.user.add_roles(role)
        await interaction.response.send_message("🔔 Je ontvangt nu **Aankondiging meldingen**!", ephemeral=True)

    @discord.ui.button(label="Update melding", style=discord.ButtonStyle.green)
    async def update(self, interaction: discord.Interaction, button: Button):
        role = await get_or_create_role(interaction.guild, "Update melding", discord.Colour.green())
        await interaction.user.add_roles(role)
        await interaction.response.send_message("🔧 Je ontvangt nu **Update meldingen**!", ephemeral=True)

    @discord.ui.button(label="Giveaway melding", style=discord.ButtonStyle.red)
    async def giveaway(self, interaction: discord.Interaction, button: Button):
        role = await get_or_create_role(interaction.guild, "Giveaway melding", discord.Colour.red())
        await interaction.user.add_roles(role)
        await interaction.response.send_message("🎉 Je ontvangt nu **Giveaway meldingen**!", ephemeral=True)


# -----------------------------
# VIEW: Algemene rollen panel
# -----------------------------
class RollenPanelView(View):
    def __init__(self, bot):
        super().__init__(timeout=None)
        self.bot = bot

    @discord.ui.button(label="Aankondiging melding", style=discord.ButtonStyle.green)
    async def aankondiging(self, interaction: discord.Interaction, button: Button):
        role = await get_or_create_role(interaction.guild, "Aankondiging melding", discord.Colour.orange())
        await interaction.user.add_roles(role)
        await interaction.response.send_message("🔔 Je ontvangt nu **Aankondiging meldingen**!", ephemeral=True)

    @discord.ui.button(label="Content melding", style=discord.ButtonStyle.gray)
    async def content(self, interaction: discord.Interaction, button: Button):
        role = await get_or_create_role(interaction.guild, "Content melding", discord.Colour.dark_gray())
        await interaction.user.add_roles(role)
        await interaction.response.send_message("📢 Je ontvangt nu **Content meldingen**!", ephemeral=True)

    @discord.ui.button(label="Andere dingen melding", style=discord.ButtonStyle.blurple)
    async def andere(self, interaction: discord.Interaction, button: Button):
        role = await get_or_create_role(interaction.guild, "Andere dingen melding", discord.Colour.blue())
        await interaction.user.add_roles(role)
        await interaction.response.send_message("✨ Je ontvangt nu **Andere dingen meldingen**!", ephemeral=True)


# -----------------------------
# COG
# -----------------------------
class Rollen(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(name="mcrollenpanel", description="Plaats het Minecraft rollen panel")
    async def mcrollenpanel(self, interaction: discord.Interaction):
        embed = discord.Embed(
            title="🟩 Minecraft Rollen",
            description="Kies hieronder jouw Minecraft & meldingsrollen:",
            color=discord.Color.green()
        )
        await interaction.channel.send(embed=embed, view=MCRollenView(self.bot))
        await interaction.response.send_message("Minecraft rollen panel geplaatst!", ephemeral=True)

    @app_commands.command(name="rollenpanel", description="Plaats het algemene rollen panel")
    async def rollenpanel(self, interaction: discord.Interaction):
        embed = discord.Embed(
            title="🔔 Meldingsrollen",
            description="Kies welke meldingen je wilt ontvangen:",
            color=discord.Color.blue()
        )
        await interaction.channel.send(embed=embed, view=RollenPanelView(self.bot))
        await interaction.response.send_message("Rollenpanel geplaatst!", ephemeral=True)


async def setup(bot):
    await bot.add_cog(Rollen(bot))

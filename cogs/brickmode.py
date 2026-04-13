import discord
from discord.ext import commands
from discord import app_commands

OWNER_ID = 901119138662055956  # <-- Jouw Discord ID

class BrickMode(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.bot.bricked = False  # Bot start normaal

    # -----------------------------
    # /brickmode
    # -----------------------------
    @app_commands.command(name="brickmode", description="Zet de bot in brick mode (alleen Dani)")
    async def brickmode(self, interaction: discord.Interaction):

        # Alleen Dani mag dit
        if interaction.user.id != OWNER_ID:
            return await interaction.response.send_message(
                "❌ Alleen **Dani** mag dit gebruiken.",
                ephemeral=True
            )

        self.bot.bricked = True

        await interaction.response.send_message(
            "🧱 **Brick mode geactiveerd.**\n"
            "De bot reageert nergens meer op behalve **/unbrick**."
        )

    # -----------------------------
    # /unbrick
    # -----------------------------
    @app_commands.command(name="unbrick", description="Haalt brick mode weg (alleen Dani)")
    async def unbrick(self, interaction: discord.Interaction):

        if interaction.user.id != OWNER_ID:
            return await interaction.response.send_message(
                "❌ Alleen **Dani** mag dit gebruiken.",
                ephemeral=True
            )

        self.bot.bricked = False

        await interaction.response.send_message(
            "✅ **Brick mode gedeactiveerd.**\n"
            "De bot werkt weer normaal."
        )

    # -----------------------------
    # Intercept ALLE commands
    # -----------------------------
    @commands.Cog.listener()
    async def on_interaction(self, interaction: discord.Interaction):

        # Als bot niet in brick mode staat → alles werkt
        if not self.bot.bricked:
            return

        # /unbrick moet ALTIJD werken
        if interaction.type == discord.InteractionType.application_command:
            if interaction.data.get("name") == "unbrick":
                return

            # Alle andere commands blokkeren
            await interaction.response.send_message(
                "🧱 De bot staat in **brick mode**.\n"
                "Alleen **/unbrick** werkt.",
                ephemeral=True
            )
            raise Exception("Command blocked by brick mode")


async def setup(bot):
    await bot.add_cog(BrickMode(bot))

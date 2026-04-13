import discord
from discord.ext import commands, tasks
from discord import app_commands
import datetime

OWNER_ID = 901119138662055956  # Dani
LOG_CHANNEL_ID = 0  # <-- Vul hier jouw staff-log kanaal ID in

class BrickMode(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.bot.bricked = False
        self.brick_until = None  # Tijd wanneer brickmode eindigt
        self.brick_timer_check.start()

    # -----------------------------
    # Helper: log naar staff kanaal
    # -----------------------------
    async def log(self, guild, message):
        if LOG_CHANNEL_ID == 0:
            return  # Geen logkanaal ingesteld
        channel = guild.get_channel(LOG_CHANNEL_ID)
        if channel:
            await channel.send(message)

    # -----------------------------
    # /brickmode [tijd]
    # -----------------------------
    @app_commands.command(name="brickmode", description="Zet de bot in brick mode (alleen Dani)")
    @app_commands.describe(tijd="Bijv: 10m, 1h, 30s (optioneel)")
    async def brickmode(self, interaction: discord.Interaction, tijd: str = None):

        if interaction.user.id != OWNER_ID:
            return await interaction.response.send_message(
                "❌ Alleen **Dani** mag dit gebruiken.",
                ephemeral=True
            )

        self.bot.bricked = True

        # Tijd verwerken
        if tijd:
            try:
                eenheid = tijd[-1]
                waarde = int(tijd[:-1])

                if eenheid == "s":
                    delta = datetime.timedelta(seconds=waarde)
                elif eenheid == "m":
                    delta = datetime.timedelta(minutes=waarde)
                elif eenheid == "h":
                    delta = datetime.timedelta(hours=waarde)
                else:
                    return await interaction.response.send_message(
                        "❌ Ongeldige tijd. Gebruik s, m of h.",
                        ephemeral=True
                    )

                self.brick_until = datetime.datetime.utcnow() + delta
                msg = f"🧱 **Brick mode geactiveerd voor {tijd}.**"
            except:
                return await interaction.response.send_message(
                    "❌ Ongeldige tijd. Voorbeeld: 10m, 30s, 1h",
                    ephemeral=True
                )
        else:
            self.brick_until = None
            msg = "🧱 **Brick mode geactiveerd.**"

        await interaction.response.send_message(msg)
        await self.log(interaction.guild, f"🧱 Brick mode geactiveerd door Dani. Tijd: {tijd or 'oneindig'}")

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
        self.brick_until = None

        await interaction.response.send_message("✅ **Brick mode gedeactiveerd.**")
        await self.log(interaction.guild, "✅ Brick mode gedeactiveerd door Dani.")

    # -----------------------------
    # /brickstatus
    # -----------------------------
    @app_commands.command(name="brickstatus", description="Laat zien of de bot bricked is")
    async def brickstatus(self, interaction: discord.Interaction):

        if not self.bot.bricked:
            return await interaction.response.send_message("🟢 De bot is **NIET** in brick mode.")

        if self.brick_until:
            resterend = self.brick_until - datetime.datetime.utcnow()
            seconden = int(resterend.total_seconds())
            minuten = seconden // 60
            uren = minuten // 60

            if uren > 0:
                tijd = f"{uren} uur"
            elif minuten > 0:
                tijd = f"{minuten} minuten"
            else:
                tijd = f"{seconden} seconden"

            return await interaction.response.send_message(
                f"🧱 De bot is in **brick mode**.\n⏳ Eindigt over: **{tijd}**"
            )

        await interaction.response.send_message("🧱 De bot staat in **brick mode** (oneindig).")

    # -----------------------------
    # Timer check
    # -----------------------------
    @tasks.loop(seconds=5)
    async def brick_timer_check(self):
        if self.bot.bricked and self.brick_until:
            if datetime.datetime.utcnow() >= self.brick_until:
                self.bot.bricked = False
                self.brick_until = None

    # -----------------------------
    # Intercept ALLE commands
    # -----------------------------
    @commands.Cog.listener()
    async def on_interaction(self, interaction: discord.Interaction):

        if not self.bot.bricked:
            return

        # /unbrick moet ALTIJD werken
        if interaction.type == discord.InteractionType.application_command:
            if interaction.data.get("name") == "unbrick":
                return

            await interaction.response.send_message(
                "🧱 De bot staat in **brick mode**.\nAlleen **/unbrick** werkt.",
                ephemeral=True
            )
            raise Exception("Command blocked by brick mode")


async def setup(bot):
    await bot.add_cog(BrickMode(bot))

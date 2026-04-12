import discord
import random
from discord.ext import commands

class Ping(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @discord.app_commands.command(name="ping", description="Ping test met 5 random uitkomsten")
    async def ping(self, interaction: discord.Interaction):

        opties = [
            "Petitie dat ItsDaniNL Youtuber rol krijg!",
            "Abboneer op ItsDaniNL!",
            "Gemaakt met python!",
            "Join mijn discord link in bio!",
            "ItsDaniNL versie 2.3"
        ]

        keuze = random.choice(opties)
        latency_ms = round(self.bot.latency * 1000)

        await interaction.response.send_message(f"{keuze} — `{latency_ms}ms`")

async def setup(bot):
    await bot.add_cog(Ping(bot))


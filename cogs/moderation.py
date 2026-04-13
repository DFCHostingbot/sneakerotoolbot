import discord
from discord.ext import commands
import asyncio

class Moderation(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    # Helper: rol ophalen of maken
    async def get_or_create_role(self, guild, name, colour):
        role = discord.utils.get(guild.roles, name=name)
        if role is None:
            role = await guild.create_role(name=name, colour=colour)
        return role

    # -----------------------------
    # /warn
    # -----------------------------
    @discord.app_commands.command(name="warn", description="Waarschuw een gebruiker (Warn 1, 2 of 3)")
    async def warn(self, interaction: discord.Interaction, member: discord.Member, reason: str = "Geen reden opgegeven"):
        guild = interaction.guild

        warn1 = await self.get_or_create_role(guild, "Warn 1", discord.Colour.orange())
        warn2 = await self.get_or_create_role(guild, "Warn 2", discord.Colour.red())
        warn3 = await self.get_or_create_role(guild, "Warn 3", discord.Colour.dark_red())

        roles = member.roles

        if warn1 not in roles and warn2 not in roles and warn3 not in roles:
            await member.add_roles(warn1)
            level = "Warn 1"
        elif warn1 in roles and warn2 not in roles:
            await member.remove_roles(warn1)
            await member.add_roles(warn2)
            level = "Warn 2"
        elif warn2 in roles and warn3 not in roles:
            await member.remove_roles(warn2)
            await member.add_roles(warn3)
            level = "Warn 3"
        else:
            level = "Deze gebruiker heeft al Warn 3"

        await interaction.response.send_message(
            f"⚠️ {member.mention} heeft een waarschuwing gekregen.\n"
            f"**Niveau:** {level}\n"
            f"**Reden:** {reason}"
        )

    # -----------------------------
    # /unwarn
    # -----------------------------
    @discord.app_commands.command(name="unwarn", description="Verwijder één warn van een gebruiker")
    async def unwarn(self, interaction: discord.Interaction, member: discord.Member):
        guild = interaction.guild

        warn1 = discord.utils.get(guild.roles, name="Warn 1")
        warn2 = discord.utils.get(guild.roles, name="Warn 2")
        warn3 = discord.utils.get(guild.roles, name="Warn 3")

        roles = member.roles

        if warn3 in roles:
            await member.remove_roles(warn3)
            await member.add_roles(warn2)
            level = "Warn 2"
        elif warn2 in roles:
            await member.remove_roles(warn2)
            await member.add_roles(warn1)
            level = "Warn 1"
        elif warn1 in roles:
            await member.remove_roles(warn1)
            level = "Geen warns meer"
        else:
            level = "Deze gebruiker heeft geen warns"

        await interaction.response.send_message(
            f"♻️ Warn verlaagd voor {member.mention}.\n**Nieuw niveau:** {level}"
        )

    # -----------------------------
    # /clear-warns
    # -----------------------------
    @discord.app_commands.command(name="clear-warns", description="Verwijder alle warns van een gebruiker")
    async def clear_warns(self, interaction: discord.Interaction, member: discord.Member):
        guild = interaction.guild

        warn1 = discord.utils.get(guild.roles, name="Warn 1")
        warn2 = discord.utils.get(guild.roles, name="Warn 2")
        warn3 = discord.utils.get(guild.roles, name="Warn 3")

        for role in [warn1, warn2, warn3]:
            if role in member.roles:
                await member.remove_roles(role)

        await interaction.response.send_message(
            f"🧹 Alle waarschuwingen verwijderd voor {member.mention}"
        )

    # -----------------------------
    # /mute
    # -----------------------------
    @discord.app_commands.command(name="mute", description="Mute een gebruiker")
    async def mute(self, interaction: discord.Interaction, member: discord.Member, reason: str = "Geen reden opgegeven"):
        guild = interaction.guild

        mute_role = discord.utils.get(guild.roles, name="Muted")
        if mute_role is None:
            mute_role = await guild.create_role(name="Muted", colour=discord.Colour.dark_grey())
            for channel in guild.channels:
                await channel.set_permissions(mute_role, speak=False, send_messages=False)

        await member.add_roles(mute_role)
        await interaction.response.send_message(
            f"🔇 {member.mention} is gemute.\n**Reden:** {reason}"
        )

    # -----------------------------
    # /unmute
    # -----------------------------
    @discord.app_commands.command(name="unmute", description="Unmute een gebruiker")
    async def unmute(self, interaction: discord.Interaction, member: discord.Member):
        mute_role = discord.utils.get(interaction.guild.roles, name="Muted")

        if mute_role in member.roles:
            await member.remove_roles(mute_role)
            msg = f"🔊 {member.mention} is geunmute."
        else:
            msg = f"❌ {member.mention} is niet gemute."

        await interaction.response.send_message(msg)

    # -----------------------------
    # /kick
    # -----------------------------
    @discord.app_commands.command(name="kick", description="Kick een gebruiker")
    async def kick(self, interaction: discord.Interaction, member: discord.Member, reason: str = "Geen reden opgegeven"):
        await member.kick(reason=reason)
        await interaction.response.send_message(
            f"👢 {member.mention} is gekickt.\n**Reden:** {reason}"
        )

    # -----------------------------
    # /ban
    # -----------------------------
    @discord.app_commands.command(name="ban", description="Ban een gebruiker")
    async def ban(self, interaction: discord.Interaction, member: discord.Member, reason: str = "Geen reden opgegeven"):
        await member.ban(reason=reason)
        await interaction.response.send_message(
            f"⛔ {member.mention} is verbannen.\n**Reden:** {reason}"
        )

    # -----------------------------
    # /temp-ban
    # -----------------------------
    @discord.app_commands.command(name="temp-ban", description="Ban een gebruiker tijdelijk")
    async def temp_ban(self, interaction: discord.Interaction, member: discord.Member, tijd: int, eenheid: str, reason: str = "Geen reden opgegeven"):
        eenheid = eenheid.lower()
        multiplier = {
            "seconden": 1,
            "minuten": 60,
            "uren": 3600,
            "dagen": 86400
        }

        if eenheid not in multiplier:
            await interaction.response.send_message("❌ Ongeldige tijdseenheid. Gebruik: seconden, minuten, uren, dagen.")
            return

        ban_seconds = tijd * multiplier[eenheid]

        await member.ban(reason=reason)
        await interaction.response.send_message(
            f"⛔ {member.mention} is tijdelijk verbannen voor **{tijd} {eenheid}**.\n**Reden:** {reason}"
        )

        await asyncio.sleep(ban_seconds)
        await interaction.guild.unban(member)

async def setup(bot):
    await bot.add_cog(Moderation(bot))

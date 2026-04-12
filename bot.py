import os
import discord

client = discord.Client(intents=discord.Intents.default())

client.run(os.getenv("TOKEN"))

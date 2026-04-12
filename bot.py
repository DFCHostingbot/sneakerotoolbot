import os
import discord
from discord.ext import commands
from flask import Flask

# Nep webserver zodat Render niet klaagt
app = Flask(__name__)

@app.route("/")
def home():
    return "OK"

# Discord bot (helemaal leeg)
client = discord.Client(intents=discord.Intents.default())

client.run(os.getenv("TOKEN"))

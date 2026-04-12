import os
import discord
from discord.ext import commands
from flask import Flask
from threading import Thread

# Nep webserver voor Render
app = Flask(__name__)

@app.route("/")
def home():
    return "OK"

def run_web():
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)

def start_web():
    Thread(target=run_web).start()

# Discord bot
intents = discord.Intents.default()
bot = commands.Bot(command_prefix="!", intents=intents)

@bot.event
async def on_ready():
    await bot.tree.sync()

# Cogs laden
bot.load_extension("cogs.ping")

start_web()
bot.run(os.getenv("TOKEN"))

import os
import discord
from discord.ext import commands
from flask import Flask
from threading import Thread

app = Flask(__name__)

@app.route("/")
def home():
    return "OK"

@app.route("/tos")
def tos():
    return """
    <h1>Terms of Service — ItsDaniNL Bot</h1>
    <p>Laatste update: 12 april 2026</p>
    <p>Door deze bot te gebruiken, gaat de gebruiker akkoord met deze voorwaarden.</p>
    <p>Je mag niet de weergave naam veranderen. Gebeurt dat? Dan gaat de bot op brick mode.</p>
    <p>De bot mag alleen worden gebruikt volgens de regels van Discord en de server waarin hij actief is.</p>
    <p>De bot slaat geen persoonlijke gegevens op.</p>
    <p>Gebruik van de bot is op eigen risico.</p>
    <p>Contact: ItsDaniNL op Discord.</p>
    """

@app.route("/privacy")
def privacy():
    return """
    <h1>Privacy Policy — ItsDaniNL Bot</h1>
    <p>Laatste update: 12 april 2026</p>
    <p>De bot verzamelt of bewaart geen persoonlijke gegevens.</p>
    <p>Alleen gegevens die nodig zijn voor commando's worden verwerkt.</p>
    <p>Geen opslag, geen derde partijen, geen tracking.</p>
    <p>Contact: ItsDaniNL op Discord.</p>
    """

def run_web():
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)

def start_web():
    Thread(target=run_web).start()

# Discord bot
intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix="!", intents=intents)

# ✔ JUISTE manier om cogs te laden
async def setup_hook():
    await bot.load_extension("cogs.ping")
    await bot.load_extension("cogs.moderation")
    await bot.tree.sync()

bot.setup_hook = setup_hook

@bot.event
async def on_ready():
    print(f"{bot.user} is online")

start_web()
bot.run(os.getenv("TOKEN"))

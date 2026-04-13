import os
import discord
from discord.ext import commands
from flask import Flask
from threading import Thread

# -----------------------------
# Flask webserver
# -----------------------------
app = Flask(__name__)

@app.route("/")
def home():
    return "OK"

@app.route("/tos")
def tos():
    return """
    <h1>Terms of Service — ItsDaniNL Bot</h1>
    <p>Laatste update: 13 april 2026</p>
    <p>Door deze bot te gebruiken, gaat de gebruiker akkoord met deze voorwaarden.</p>
    <p>Je mag niet de weergave naam veranderen. Gebeurt dat? Dan gaat de bot op brick mode.</p>
    <p>De bot mag alleen worden gebruikt volgens de regels van Discord en de server waarin hij actief is.</p>
    <p>De bot slaat geen persoonlijke gegevens op.</p>
    <p>Gebruik van de bot is op eigen risico.</p>
    <p>Ik mag youtuber rol hebben.</p>
    <p>Contact: ItsDaniNL op Discord.</p>
    <p>Om dingen te veranderen moet je een abbonement aansluiten!!!</p>
    <p>1 uur gratis</p>
    <p>Eerste maand 50% korting voor 5 cent</p>
    <p>Daarna 10 cent per maand!</p>
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

# -----------------------------
# Discord bot
# -----------------------------
intents = discord.Intents.all()
bot = commands.Bot(command_prefix="!", intents=intents)

# -----------------------------
# Cogs laden + slash sync
# -----------------------------
async def setup_hook():
    await bot.load_extension("cogs.ping")
    await bot.load_extension("cogs.moderation")
    await bot.load_extension("cogs.tickets")
    await bot.load_extension("cogs.rollen")
    await bot.load_extension("cogs.brickmode")
    await bot.tree.sync()

bot.setup_hook = setup_hook

# -----------------------------
# Bot online melding
# -----------------------------
@bot.event
async def on_ready():
    print(f"{bot.user} is online")

# -----------------------------
# Start webserver + bot
# -----------------------------
start_web()
bot.run(os.getenv("TOKEN"))

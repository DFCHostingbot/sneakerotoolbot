import os
import discord
from flask import Flask
from threading import Thread

app = Flask(__name__)

@app.route("/")
def home():
    return "OK"

def run_web():
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)

def start_web():
    t = Thread(target=run_web)
    t.start()

client = discord.Client(intents=discord.Intents.default())

start_web()
client.run(os.getenv("TOKEN"))

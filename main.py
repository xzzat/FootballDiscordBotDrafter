import discord
from discord.ext import commands
from flask import Flask
from threading import Thread

intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix="!", intents=intents)

teams = {}  # {user_id: {name, formation, players: []}}

# 🟢 Flask app to keep Replit alive
app = Flask('')

@app.route('/')
def home():
    return "I'm alive!"

def run():
    app.run(host='0.0.0.0', port=8080)

def keep_alive():
    t = Thread(target=run)
    t.start()

# 🔧 Discord Bot Events and Commands
@bot.event
async def on_ready():
    print(f"✅ Logged in as {bot.user}")

@bot.command()
async def create(ctx, *, team_name):
    teams[ctx.author.id] = {"name": team_name, "formation": "Not set", "players": []}
    await ctx.send(f"✅ Team **{team_name}** created!")

@bot.command()
async def addplayer(ctx, position, *, name):
    team = teams.get(ctx.author.id)
    if not team:
        return await ctx.send("❌ Use `!create <team name>` first.")
    team["players"].append((name, position))
    await ctx.send(f"➕ Added **{name}** as **{position}**")

@bot.command()
async def formation(ctx, *, formation):
    team = teams.get(ctx.author.id)
    if not team:
        return await ctx.send("❌ Use `!create` first.")
    team["formation"] = formation
    await ctx.send(f"📐 Formation set to **{formation}**")

@bot.command()
async def show(ctx):
    team = teams.get(ctx.author.id)
    if not team:
        return await ctx.send("❌ No team found. Use `!create` to start.")

    emoji_map = {
        "GK": "🧤",
        "CB": "🛡️", "LB": "⬅️", "RB": "➡️", "RWB": "⚡", "LWB": "⚡",
        "CM": "🧠", "CDM": "🛡️", "CAM": "🎯",
        "RW": "⚡", "LW": "⚡", "ST": "⚽", "CF": "🎯"
    }

    lines = [f"🏟️ **{team['name']}**", f"📐 Formation: `{team['formation']}`", ""]

    for name, pos in team["players"]:
        emoji = emoji_map.get(pos.upper(), "👤")
        lines.append(f"{emoji} **{name}** – `{pos}`")

    await ctx.send("\n".join(lines))


# 🔁 Keep bot alive
keep_alive()

# 🤖 Run bot using TOKEN from Replit secrets
import os
bot.run(os.getenv("TOKEN"))

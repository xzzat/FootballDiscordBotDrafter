import os
import discord
from discord.ext import commands
from flask import Flask
import threading

intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix='!', intents=intents)

# Flask setup
app = Flask(__name__)

@app.route('/')
def home():
    return "Bot is running!"

def run_flask():
    app.run(host="0.0.0.0", port=8080)

@bot.event
async def on_ready():
    print(f"✅ Logged in as {bot.user}")

# Start Flask in a new thread
threading.Thread(target=run_flask).start()

# Start Discord bot
bot.run(os.getenv("TOKEN"))


@bot.command()
async def create(ctx, *, team_name):
    teams[ctx.author.id] = {
        "name": team_name,
        "formation": "Not set",
        "players": []
    }
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
async def show(ctx, member: discord.Member = None):
    user = member or ctx.author
    team = teams.get(user.id)

    if not team:
        if member:
            await ctx.send(f"❌ {member.display_name} has not created a team.")
        else:
            await ctx.send(
                "❌ You have not created a team. Use `!create` first.")
        return

    emoji_map = {
        "GK": "🧤",
        "CB": "🛡️",
        "LB": "⬅️",
        "RB": "➡️",
        "CM": "🧠",
        "CDM": "🛡️",
        "CAM": "🎯",
        "RW": "🏃",
        "LW": "🏃",
        "ST": "⚽",
        "CF": "🎯"
    }

    lines = [
        f"🏟️ **{team['name']}** (*{user.display_name}*)",
        f"📐 Formation: `{team['formation']}`", ""
    ]

    for name, pos in team["players"]:
        emoji = emoji_map.get(pos.upper(), "👤")
        lines.append(f"{emoji} **{name}** – `{pos}`")

    await ctx.send("\n".join(lines))

    async def reset(ctx):
        if ctx.author.id in teams:
            del teams[ctx.author.id]
            await ctx.send("🗑️ Your team has been reset.")
        else:
            await ctx.send("❌ You don’t have a team to reset.")


# 🔁 Keep bot alive
keep_alive()

import os
bot.run(os.getenv("TOKEN"))

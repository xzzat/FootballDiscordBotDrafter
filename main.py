import discord
from discord.ext import commands
import os
from flask import Flask
import threading

intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix='!', intents=intents)

app = Flask('')

# In-memory storage for user teams and formations
user_teams = {}
default_formation = "4-3-3"

formation_positions = {
    "4-3-3": ["GK", "LB", "CB1", "CB2", "RB", "CM1", "CM2", "CM3", "LW", "ST", "RW"],
    "4-4-2": ["GK", "LB", "CB1", "CB2", "RB", "LM", "CM1", "CM2", "RM", "ST1", "ST2"],
    "3-5-2": ["GK", "CB1", "CB2", "CB3", "LM", "CM1", "CM2", "CM3", "RM", "ST1", "ST2"],
    "3-4-3": ["GK", "CB1", "CB2", "CB3", "LM", "CM1", "CM2", "RM", "LW", "ST", "RW"],
    "5-3-2": ["GK", "LWB", "CB1", "CB2", "CB3", "RWB", "CM1", "CM2", "CM3", "ST1", "ST2"],
    "4-2-3-1": ["GK", "LB", "CB1", "CB2", "RB", "CDM1", "CDM2", "CAM", "LW", "RW", "ST"],
    "5-a-side 2-2": ["GK", "DEF1", "DEF2", "ATT1", "ATT2"],
    "5-a-side 1-2-1": ["GK", "DEF", "MID1", "MID2", "ST"],
    "7-a-side 2-3-1": ["GK", "DEF1", "DEF2", "MID1", "MID2", "MID3", "ST"],
    "3-4-2-1": ["GK", "CB1", "CB2", "CB3", "LM", "CM1", "CM2", "RM", "LF", "RF", "ST"]
}

@bot.event
async def on_ready():
    print(f'Logged in as {bot.user}')

@bot.command()
async def create(ctx):
    user_teams[ctx.author.id] = {
        "formation": default_formation,
        "players": {}
    }
    await ctx.send(f"Team created for {ctx.author.mention} with formation {default_formation}.")

@bot.command()
async def setformation(ctx, *, formation):
    formation = formation.strip()
    if ctx.author.id not in user_teams:
        await ctx.send("You need to create a team first using !create")
        return
    if formation not in formation_positions:
        await ctx.send("Formation not supported. Example: 4-3-3, 5-a-side 2-2")
        return
    user_teams[ctx.author.id]['formation'] = formation
    user_teams[ctx.author.id]['players'] = {}  # reset players on formation change
    await ctx.send(f"Formation set to {formation} for {ctx.author.mention}.")

@bot.command()
async def setplayer(ctx, position, *, name):
    if ctx.author.id not in user_teams:
        await ctx.send("You need to create a team first using !create")
        return
    formation = user_teams[ctx.author.id]['formation']
    valid_positions = formation_positions.get(formation, [])
    position = position.upper()
    if position not in valid_positions:
        await ctx.send(f"Invalid position for {formation}. Valid: {', '.join(valid_positions)}")
        return
    user_teams[ctx.author.id]['players'][position] = name
    await ctx.send(f"Set {name} at {position} for {ctx.author.mention}.")

@bot.command()
async def show(ctx):
    if ctx.author.id not in user_teams:
        await ctx.send("You need to create a team first using !create")
        return
    team = user_teams[ctx.author.id]
    formation = team['formation']
    positions = formation_positions.get(formation, [])
    players = team['players']
    lines = [f"**{formation} Formation for {ctx.author.display_name}**"]
    for pos in positions:
        player = players.get(pos, "-")
        lines.append(f"{pos}: {player}")
    await ctx.send("\n".join(lines))

@bot.command()
async def reset(ctx):
    if ctx.author.id in user_teams:
        user_teams[ctx.author.id]['players'] = {}
        await ctx.send("Your team has been reset.")
    else:
        await ctx.send("You need to create a team first using !create")

# Keep-alive server (for Render deployment)
@app.route('/')
def home():
    return "Bot is running"

def run():
    app.run(host='0.0.0.0', port=8080)

def keep_alive():
    thread = threading.Thread(target=run)
    thread.start()

keep_alive()

bot.run(os.getenv("DISCORD_BOT_TOKEN"))

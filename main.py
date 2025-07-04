import discord
from discord.ext import commands

# Intents
intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix="!", intents=intents)

# Formation definitions with valid positions
formations = {
    "4-3-3": ["GK", "LB", "CB1", "CB2", "RB", "CM1", "CM2", "CM3", "LW", "ST", "RW"],
    "3-4-2-1": ["GK", "CB1", "CB2", "CB3", "LM", "CM1", "CM2", "RM", "LF", "RF", "ST"],
    "2-2": ["GK", "DEF1", "DEF2", "MID", "ST"],
    "1-2-1": ["GK", "DEF", "MID1", "MID2", "ST"],
    "3-2-1": ["GK", "DEF1", "DEF2", "DEF3", "MID1", "MID2", "ST"],
    "2-3-1": ["GK", "DEF1", "DEF2", "MID1", "MID2", "MID3", "ST"]
}

position_emojis = {
    "GK": "🧤", "LB": "🛡️", "CB1": "🛡️", "CB2": "🛡️", "RB": "🛡️",
    "CM1": "🎯", "CM2": "🎯", "CM3": "🎯", "LM": "📌", "RM": "📌",
    "LF": "⚡", "RF": "⚡", "LW": "⚡", "RW": "⚡", "ST": "⚽", "CF": "⚽"
    "DEF1": "🛡️", "DEF2": "🛡️", "DEF3": "🛡️", "DEF": "🛡️",
    "MID": "🎽", "MID1": "🎽", "MID2": "🎽", "MID3": "🎽"
}

teams = {}

@bot.event
async def on_ready():
    print(f"Logged in as {bot.user}")

@bot.command()
async def create(ctx):
    user_id = str(ctx.author.id)
    teams[user_id] = {
        "formation": "4-3-3",
        "players": {pos: "-" for pos in formations["4-3-3"]}
    }
    await ctx.send("✅ Team created with default formation 4-3-3")

@bot.command()
async def setformation(ctx, *, formation):
    user_id = str(ctx.author.id)
    if user_id not in teams:
        return await ctx.send("❌ You must create a team first using !create")
    formation = formation.strip()
    if formation not in formations:
        return await ctx.send("❌ Invalid formation")
    teams[user_id]["formation"] = formation
    teams[user_id]["players"] = {pos: "-" for pos in formations[formation]}
    await ctx.send(f"✅ Formation set to {formation}")

@bot.command()
async def setplayer(ctx, position, *, name):
    user_id = str(ctx.author.id)
    if user_id not in teams:
        return await ctx.send("❌ You must create a team first using !create")
    team = teams[user_id]
    if position not in team["players"]:
        return await ctx.send("❌ Invalid position for current formation")
    team["players"][position] = name
    await ctx.send(f"✅ Set {name} as {position}")

@bot.command()
async def reset(ctx):
    user_id = str(ctx.author.id)
    if user_id not in teams:
        return await ctx.send("❌ You must create a team first using !create")
    formation = teams[user_id]["formation"]
    teams[user_id]["players"] = {pos: "-" for pos in formations[formation]}
    await ctx.send("🔄 Team reset")

@bot.command()
async def show(ctx):
    user_id = str(ctx.author.id)
    if user_id not in teams:
        return await ctx.send("❌ You must create a team first using !create")
    team = teams[user_id]
    formation = team["formation"]
    lines = [f"**Formation: {formation}**"]
    for pos in formations[formation]:
        emoji = position_emojis.get(pos, "⬜")
        name = team["players"][pos]
        lines.append(f"{emoji} {pos}: {name}")
    await ctx.send("\n".join(lines))

# Replace with your bot token
bot.run("YOUR_TOKEN")

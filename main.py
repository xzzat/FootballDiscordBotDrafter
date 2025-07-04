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

@bot.command(name="show")
async def show_team(ctx):
    user_id = str(ctx.author.id)
    if user_id not in teams:
        await ctx.send("You don't have a team yet. Use `!create [Team Name]` to start.")
        return

    team = teams[user_id]
    formation = team["formation"]
    players = team["players"]

    if formation not in formation_positions:
        await ctx.send("Your formation is not recognized.")
        return

    positions = formation_positions[formation]
    position_labels = {
        "GK": "🧤 GK",
        "LB": "🛡️ LB",
        "CB": "🛡️ CB",
        "RB": "🛡️ RB",
        "LWB": "🛡️ LWB",
        "RWB": "🛡️ RWB",
        "CDM": "🎯 CDM",
        "CM": "🎯 CM",
        "CAM": "🎯 CAM",
        "LM": "🎯 LM",
        "RM": "🎯 RM",
        "LW": "⚽ LW",
        "RW": "⚽ RW",
        "ST": "⚽ ST",
        "CF": "⚽ CF"
    }

    # Sort by vertical order: GK → Defenders → Midfielders → Attackers
    order = {
        "GK": 0, "LB": 1, "LWB": 1, "CB": 2, "RB": 3, "RWB": 3,
        "CDM": 4, "CM": 5, "CAM": 6, "LM": 4, "RM": 6,
        "LW": 7, "RW": 8, "ST": 9, "CF": 9
    }

    sorted_positions = sorted(positions, key=lambda x: order.get(x, 100))

    lines = []
    for pos in sorted_positions:
        player = players.get(pos, "[empty]")
        label = position_labels.get(pos, pos)
        lines.append(f"{label}: {player}")

    await ctx.send("**Your Team:**\n" + "\n".join(lines))

# Replace with your bot token
bot.run("YOUR_TOKEN")

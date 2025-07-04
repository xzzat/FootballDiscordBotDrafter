import discord
from discord.ext import commands

intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix='!', intents=intents)

teams = {}
formations = {}

# Default formation layout for common formations
formation_layouts = {
    "4-3-3": ["GK", "LB", "CB", "CB", "RB", "CM", "CM", "CM", "LW", "ST", "RW"],
    "3-4-2-1": ["GK", "CB", "CB", "CB", "LM", "CM", "CM", "RM", "CAM", "CAM", "ST"],
    "2-2": ["GK", "DEF", "DEF", "MID", "MID"],
    "1-2-1": ["GK", "DEF", "MID", "MID", "ST"],
    "3-2-1": ["GK", "DEF", "DEF", "DEF", "MID", "MID", "ST"],
    "2-3-1": ["GK", "DEF", "DEF", "MID", "MID", "MID", "ST"],
}

position_emojis = {
    "GK": 💪,
    "LB": 🌟, "CB": 🔒, "RB": 🌟, "DEF": 🔒,
    "LM": 🔹, "CM": ⚖️, "RM": 🔹, "MID": ⚖️, "CAM": 🌟,
    "LW": 🔥, "RW": 🔥, "ST": ⚽, "CF": ⚽
}

def format_team(user_id):
    team = teams.get(user_id, {})
    formation = formations.get(user_id, "4-3-3")
    layout = formation_layouts.get(formation, [])

    lines = []
    for position in layout:
        player = team.get(position, "-")
        emoji = position_emojis.get(position, "")
        lines.append(f"{emoji} {position}: {player}")

    return "\n".join(lines)

@bot.event
async def on_ready():
    print(f'Logged in as {bot.user}')

@bot.command()
async def create(ctx):
    user_id = ctx.author.id
    teams[user_id] = {}
    formations[user_id] = "4-3-3"
    await ctx.send("Your team has been created!")

@bot.command()
async def setformation(ctx, *, formation):
    user_id = ctx.author.id
    if formation not in formation_layouts:
        await ctx.send(f"Invalid formation. Available: {', '.join(formation_layouts.keys())}")
    else:
        formations[user_id] = formation
        await ctx.send(f"Formation set to {formation}.")

@bot.command()
async def setplayer(ctx, position, *, name):
    user_id = ctx.author.id
    formation = formations.get(user_id, "4-3-3")
    if position not in formation_layouts.get(formation, []):
        await ctx.send("Invalid position for current formation.")
        return
    if user_id not in teams:
        await ctx.send("Create a team first using !create")
        return
    teams[user_id][position] = name
    await ctx.send(f"Set {name} at {position}.")

@bot.command()
async def reset(ctx):
    user_id = ctx.author.id
    teams[user_id] = {}
    await ctx.send("Your team has been reset.")

@bot.command()
async def show(ctx):
    user_id = ctx.author.id
    if user_id not in teams:
        await ctx.send("Create a team first using !create")
        return
    team_display = format_team(user_id)
    await ctx.send(f"```\n{team_display}\n```")

bot.run("YOUR_TOKEN")

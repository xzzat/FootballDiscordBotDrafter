import os
import discord
from discord.ext import commands
from keep_alive import keep_alive

intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix='!', intents=intents)

teams = {}

@bot.event
async def on_ready():
    print(f'Logged in as {bot.user.name}')

@bot.command()
async def create(ctx, team_name, *players):
    if ctx.author.id not in teams:
        teams[ctx.author.id] = {}
    teams[ctx.author.id][team_name] = {
        "players": list(players),
        "formation": None
    }
    await ctx.send(f"Team `{team_name}` created with players: {', '.join(players)}")

@bot.command()
async def setformation(ctx, team_name, *, formation):
    user_teams = teams.get(ctx.author.id, {})
    team = user_teams.get(team_name)

    if not team:
        await ctx.send(f"No team found with name `{team_name}`.")
        return

    team["formation"] = formation
    await ctx.send(f"Formation `{formation}` set for team `{team_name}`.")

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

    
keep_alive()
bot.run(os.getenv("TOKEN"))


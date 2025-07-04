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

@bot.command()
async def show(ctx, team_name):
    user_teams = teams.get(ctx.author.id, {})
    team = user_teams.get(team_name)

    if not team:
        await ctx.send(f"No team found with name `{team_name}`.")
        return

    formation = team["formation"] or "Not set"
    players = ", ".join(team["players"]) or "No players"
    await ctx.send(f"**Team:** {team_name}\n**Formation:** {formation}\n**Players:** {players}")
    
keep_alive()
bot.run(os.getenv("TOKEN"))


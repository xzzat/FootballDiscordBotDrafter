import os
import discord
from discord.ext import commands
from flask import Flask
import threading
from PIL import Image, ImageDraw, ImageFont
import io

intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix="!", intents=intents)

# Minimal Flask app to keep Render alive
app = Flask(__name__)

@app.route('/')
def index():
    return "Bot is running!"

def run_flask():
    app.run(host="0.0.0.0", port=8080)

threading.Thread(target=run_flask).start()

# Store teams per user
user_teams = {}

# Formation templates (FIFA, 5-a-side, 7-a-side)
formations = {
    "4-3-3": {
        "GK": (375, 530),
        "LB": (100, 400), "CB1": (275, 400), "CB2": (475, 400), "RB": (650, 400),
        "CM1": (200, 280), "CM2": (400, 250), "CM3": (600, 280),
        "LW": (150, 100), "ST": (400, 80), "RW": (650, 100)
    },
    "4-4-2": {
        "GK": (375, 530),
        "LB": (100, 400), "CB1": (275, 400), "CB2": (475, 400), "RB": (650, 400),
        "LM": (150, 250), "CM1": (300, 250), "CM2": (450, 250), "RM": (600, 250),
        "ST1": (275, 100), "ST2": (475, 100)
    },
    "4-2-3-1": {
        "GK": (375, 530),
        "LB": (100, 400), "CB1": (275, 400), "CB2": (475, 400), "RB": (650, 400),
        "CDM1": (275, 300), "CDM2": (475, 300),
        "LAM": (200, 200), "CAM": (375, 200), "RAM": (550, 200),
        "ST": (375, 100)
    },
    "3-5-2": {
        "GK": (375, 530),
        "CB1": (200, 400), "CB2": (375, 400), "CB3": (550, 400),
        "LM": (100, 250), "CM1": (250, 250), "CM2": (375, 220), "CM3": (500, 250), "RM": (650, 250),
        "ST1": (300, 100), "ST2": (450, 100)
    },
    "3-4-2-1": {
        "GK": (375, 530),
        "CB1": (225, 400), "CB2": (375, 400), "CB3": (525, 400),
        "LM": (150, 280), "CM1": (300, 280), "CM2": (450, 280), "RM": (600, 280),
        "LAM": (275, 150), "RAM": (475, 150),
        "ST": (375, 80)
    },
    "2-2": {
        "GK": (375, 530),
        "DEF1": (275, 400), "DEF2": (475, 400),
        "MID1": (275, 250), "MID2": (475, 250)
    },
    "1-2-1": {
        "GK": (375, 530),
        "DEF": (375, 400),
        "MID1": (275, 250), "MID2": (475, 250),
        "FWD": (375, 100)
    },
    "2-3-1": {
        "GK": (375, 530),
        "DEF1": (250, 400), "DEF2": (500, 400),
        "MID1": (200, 250), "MID2": (375, 250), "MID3": (550, 250),
        "FWD": (375, 100)
    }
}

@bot.command()
async def setplayer(ctx, position: str, *, name: str):
    uid = str(ctx.author.id)
    user_teams.setdefault(uid, {})
    user_teams[uid][position.upper()] = name
    await ctx.send(f"✅ Set **{position.upper()}** to **{name}** for your team.")

@bot.command()
async def show(ctx, *, formation_name="4-3-3"):
    formation_key = formation_name.strip().lower()
    if formation_key not in [f.lower() for f in formations]:
        await ctx.send("❌ Formation not found. Try `!show 4-3-3`, `!show 2-3-1`, `!show 3-4-2-1`")
        return

    # Match actual case-sensitive key
    for key in formations:
        if key.lower() == formation_key:
            formation = formations[key]
            break

    uid = str(ctx.author.id)
    team = user_teams.get(uid, {})

    img = Image.new('RGB', (800, 600), color=(34, 139, 34))
    draw = ImageDraw.Draw(img)
    font = ImageFont.load_default()

    for pos, (x, y) in formation.items():
        name = team.get(pos, pos)
        draw.rectangle((x - 40, y - 20, x + 40, y + 20), fill="white")
        draw.text((x - 30, y - 10), name[:12], fill="black", font=font)

    with io.BytesIO() as image_binary:
        img.save(image_binary, 'PNG')
        image_binary.seek(0)
        await ctx.send(file=discord.File(fp=image_binary, filename='formation.png'))

@bot.event
async def on_ready():
    print(f"✅ Logged in as {bot.user}")

bot.run(os.getenv("TOKEN"))

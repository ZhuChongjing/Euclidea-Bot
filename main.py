from discord.ext import commands
from config import LEVEL_DESCRIPTION
from dotenv import load_dotenv
import os
import discord
import asyncio

load_dotenv()
TOKEN = os.getenv("DISCORD_BOT_TOKEN")

intents = discord.Intents.default()
intents.message_content = True
intents.members = False
intents.presences = False

bot = commands.Bot(command_prefix="!", intents=intents)

async def keep_alive():
    sec = 0
    while True:
        sec += 1
        print(f"\rBot is Running... {sec}s", end="")

@bot.event
async def on_ready():
    print(
        f"✅ Robot {bot.user.name} (ID: {bot.user.id}) has successfully logged in!"
    )
    asyncio.create_task(keep_alive())


@bot.slash_command(name="level",
                   description="See the Euclidea level description.")
@discord.option(name="level",
                input_type=str,
                description="Euclidea level number (e.g. 4.11)",
                required=True)
async def level(interaction: discord.Interaction, level: str):
    if level not in LEVEL_DESCRIPTION.keys():
        await interaction.response.send_message(
            "Invalid level number. Please check the format (e.g. 4.11).")
        return
    embed = discord.Embed(title=f"{level} {LEVEL_DESCRIPTION[level]['title']}",
                          description=LEVEL_DESCRIPTION[level]["description"],
                          color=discord.Color.blue())
    await interaction.response.send_message(embed=embed)

if __name__ == "__main__":
    bot.run(TOKEN, reconnect=True)

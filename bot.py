import os
import discord
from discord import app_commands
from discord.ext import commands
from datetime import datetime

# ========= TOKEN FROM ENV =========
TOKEN = os.getenv("TOKEN")
if not TOKEN:
    raise RuntimeError("TOKEN not found in environment variables")

# ========= INTENTS =========
intents = discord.Intents.default()
intents.members = True

bot = commands.Bot(command_prefix="!", intents=intents)

# ========= READY =========
@bot.event
async def on_ready():
    await bot.tree.sync()
    print(f"✅ Logged in as {bot.user}")

# ========= /vouch COMMAND =========
@bot.tree.command(name="vouch", description="Send a vouch with star rating")
@app_commands.describe(
    user="Who are you vouching for",
    stars="Star rating",
    review="Your review message"
)
@app_commands.choices(stars=[
    app_commands.Choice(name="⭐ 1 Star", value=1),
    app_commands.Choice(name="⭐⭐ 2 Stars", value=2),
    app_commands.Choice(name="⭐⭐⭐ 3 Stars", value=3),
    app_commands.Choice(name="⭐⭐⭐⭐ 4 Stars", value=4),
    app_commands.Choice(name="⭐⭐⭐⭐⭐ 5 Stars", value=5),
])
async def vouch(
    interaction: discord.Interaction,
    user: discord.Member,
    stars: app_commands.Choice[int],
    review: str
):
    await interaction.response.defer(thinking=True)

    stars_display = "⭐" * stars.value
    date = datetime.now().strftime("%d %b %Y")

    embed = discord.Embed(
        title="🎉 New Vouch Received!",
        description=f"{interaction.user.mention} vouched for {user.mention}",
        color=discord.Color.gold()
    )
    embed.add_field(name="⭐ Rating", value=f"{stars_display} ({stars.value}/5)", inline=False)
    embed.add_field(name="📝 Review", value=review, inline=False)
    embed.add_field(name="📅 Date", value=date, inline=False)

    msg = await interaction.followup.send(embed=embed)
    await msg.add_reaction("👍")
    await msg.add_reaction("❤️")
    await msg.add_reaction("⭐")

    try:
        await interaction.user.send(embed=embed)
    except:
        pass

    try:
        await user.send(embed=embed)
    except:
        pass

# ========= RUN =========
bot.run(TOKEN)

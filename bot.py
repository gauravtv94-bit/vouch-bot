import discord
from discord.ext import commands
from discord import app_commands
import os
# ================= SAFE TOKEN =================
# Token will come from hosting (Render), NOT from code
TOKEN = os.getenv("TOKEN")

# Stop bot if token is missing (prevents silent crash)
if not TOKEN:
    raise RuntimeError("TOKEN not found. Add it in hosting Environment Variables.")

# ================= INTENTS =================
intents = discord.Intents.default()
intents.members = True

bot = commands.Bot(command_prefix="!", intents=intents)

# ---------- BOT READY ----------
@bot.event
async def on_ready():
    await bot.tree.sync()  # Sync slash commands
    print(f"✅ Logged in as {bot.user}")

# ---------- /vouch COMMAND ----------
@bot.tree.command(name="vouch", description="Send a vouch with star rating")
@app_commands.describe(
    user="Who are you vouching for",
    review="Write your review"
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
    # Prevent "application did not respond"
    await interaction.response.defer()

    star_display = "⭐" * stars.value
    date = datetime.now().strftime("%d %b %Y")

    embed = discord.Embed(
        title="🎉 New Vouch Received!",
        description=f"{interaction.user.mention} has vouched for {user.mention}!",
        color=discord.Color.gold()
    )

    embed.add_field(
        name="Rating",
        value=f"{star_display} ({stars.value}/5)",
        inline=False
    )

    embed.add_field(
        name="📝 Vouch Message",
        value=review,
        inline=False
    )

    embed.add_field(
        name="📅 Date",
        value=date,
        inline=False
    )

    # Send in server
    msg = await interaction.followup.send(embed=embed)

    # Auto reactions
    for emoji in ("👍", "❤️", "⭐"):
        await msg.add_reaction(emoji)

    # DM to vouch creator
    try:
        await interaction.user.send(embed=embed)
    except:
        pass

    # DM to vouched user
    try:
        await user.send(embed=embed)
    except:
        pass

# ================= RUN BOT =================
bot.run(os.getenv("TOKEN"))

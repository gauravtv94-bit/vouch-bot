import discord
from discord.ext import commands
from discord import app_commands
from datetime import datetime

# ================== BOT TOKEN ==================
# 🔴 PASTE YOUR BOT TOKEN BELOW (ONLY ON REPLIT / LOCAL)
TOKEN = "MTQ1NDg4MzIyODc2MTcxODc5Ng.GUw_Ga.5QKPHPw_YNSRmxvcbgvWcGlwhNoV9asORcLrZM"
# =================================================

# --------- INTENTS ---------
intents = discord.Intents.default()
intents.members = True

# --------- BOT SETUP ---------
class MyBot(commands.Bot):
    def __init__(self):
        super().__init__(command_prefix="!", intents=intents)

    async def setup_hook(self):
        await self.tree.sync()  # Sync slash commands globally
        print("✅ Slash commands synced")

bot = MyBot()

# --------- READY EVENT ---------
@bot.event
async def on_ready():
    print(f"🤖 Logged in as {bot.user} (ID: {bot.user.id})")

# --------- /vouch COMMAND ---------
@bot.tree.command(name="vouch", description="Send a vouch with star rating")
@app_commands.describe(
    user="Who are you vouching for",
    stars="Star rating",
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
    await interaction.response.defer(thinking=True)

    star_display = "⭐" * stars.value
    date = datetime.now().strftime("%d %b %Y")

    embed = discord.Embed(
        title="🌟 New Vouch!",
        description=f"{interaction.user.mention} vouched for {user.mention}",
        color=discord.Color.gold()
    )

    embed.add_field(
        name="Rating",
        value=f"{star_display} ({stars.value}/5)",
        inline=False
    )

    embed.add_field(
        name="Review",
        value=review,
        inline=False
    )

    embed.set_footer(text=f"Date: {date}")

    msg = await interaction.followup.send(embed=embed)

    # Reactions
    await msg.add_reaction("❤️")
    await msg.add_reaction("⭐")
    await msg.add_reaction("👍")

    # DM sender
    try:
        await interaction.user.send(embed=embed)
    except:
        pass

    # DM receiver
    try:
        await user.send(embed=embed)
    except:
        pass

# --------- RUN BOT ---------
bot.run(TOKEN)

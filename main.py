import discord
import random
from discord.ext import commands
from discord import app_commands

token = "womp"
with open('token.txt', 'r') as file:
    token = file.read().replace('\n', '')

intents = discord.Intents.all()
intents.message_content = True
intents.presences = True
intents.members = True

client = commands.Bot(command_prefix='/', intents=intents)
testingserver = 1308722552407068733

async def defer_and_send(ctx, content, ephemeral=False, embed=None):
    await ctx.response.defer(ephemeral=ephemeral)
    await ctx.followup.send(content=content, embed=embed)

async def handle_exception(ctx, e):
    await defer_and_send(ctx, f"An error occurred: {e}", ephemeral=True)

@client.event
async def on_ready():
    print("Sync V2 !")
    print('Connecté en tant que : {0.user}'.format(client))
    try:
        synced = await client.tree.sync(guild=discord.Object(id=testingserver))
        print(f"Synced {len(synced)} commands !")
    except Exception as e:
        print(e)
    print(f"Ready")

@client.tree.command(name="ping", description="Ping pong")
@app_commands.guilds(discord.Object(id=testingserver))
async def ping(ctx):
    await defer_and_send(ctx, 'Pong !', ephemeral=True)

@client.tree.command(name="bonk", description="Bonk command")
@app_commands.guilds(discord.Object(id=testingserver))
async def bonk(ctx):
    bonk_url = "https://tenor.com/view/nikke-diesel-gif-13113323641692735605"
    await defer_and_send(ctx, bonk_url)

@client.tree.command(name="yonk", description="yonk command")
@app_commands.guilds(discord.Object(id=testingserver))
async def yonk(ctx):
    yonk_url = "https://imgur.com/a/wsyTIbA"
    await defer_and_send(ctx, yonk_url)

@client.tree.command(name="rename", description="Change your nickname")
@app_commands.guilds(discord.Object(id=testingserver))
async def change_nick(ctx, new_nickname: str):
    try:
        await ctx.user.edit(nick=new_nickname)
        await defer_and_send(ctx, f"Nickname changed to {new_nickname}", ephemeral=True)
    except discord.Forbidden:
        await defer_and_send(ctx, "I don't have permission to change your nickname.", ephemeral=True)
    except Exception as e:
        await handle_exception(ctx, e)

@client.tree.command(name="rename_other_user", description="Change a user's nickname")
@app_commands.guilds(discord.Object(id=testingserver))
async def change_other_nick(ctx, member: discord.Member, new_nickname: str):
    try:
        await member.edit(nick=new_nickname)
        await defer_and_send(ctx, f"Nickname for {member.display_name} changed to {new_nickname}", ephemeral=True)
    except discord.Forbidden:
        await defer_and_send(ctx, "I don't have permission to change this user's nickname.", ephemeral=True)
    except Exception as e:
        await handle_exception(ctx, e)

@client.tree.command(name="avatar", description="Get a user's profile picture")
@app_commands.guilds(discord.Object(id=testingserver))
async def avatar(ctx, member: discord.Member):
    try:
        avatar_url = member.avatar.url if member.avatar else member.default_avatar.url
        await defer_and_send(ctx, f"{member.display_name}'s avatar: {avatar_url}", ephemeral=True)
    except Exception as e:
        await handle_exception(ctx, e)

@client.tree.command(name="userinfo", description="Get a user's account information")
@app_commands.guilds(discord.Object(id=testingserver))
async def userinfo(ctx, member: discord.Member):
    try:
        embed = discord.Embed(title=f"User Information for {member.display_name}", color=discord.Color.purple())
        embed.set_thumbnail(url=member.avatar.url if member.avatar else member.default_avatar.url)
        embed.add_field(name="ID", value=member.id, inline=False)
        embed.add_field(name="Name", value=member.name, inline=True)
        embed.add_field(name="Discriminator", value=member.discriminator, inline=True)
        embed.add_field(name="Account Created", value=member.created_at.strftime('%Y-%m-%d %H:%M:%S'), inline=False)
        embed.add_field(name="Joined Server", value=member.joined_at.strftime('%Y-%m-%d %H:%M:%S') if member.joined_at else 'N/A', inline=False)

        await defer_and_send(ctx, f"User information of {member.mention}", embed=embed)
    except Exception as e:
        await handle_exception(ctx, e)

@client.tree.command(name="dice", description="Roll a dice")
@app_commands.guilds(discord.Object(id=testingserver))
async def roll_dice(ctx):
    dice_roll = random.randint(1, 6)
    await defer_and_send(ctx, f'you rolled a {dice_roll}!')

client.run(token)
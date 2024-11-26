import discord
import random
import re
from PIL import Image
from io import BytesIO
from discord.ext import commands
from discord import app_commands

token = "womp"
with open("token.txt", "r") as file:
    token = file.read().replace("\n", "")

intents = discord.Intents.all()
intents.message_content = True
intents.presences = True
intents.members = True

client = commands.Bot(command_prefix="/", intents=intents)
testingserver = 1308722552407068733


async def defer_and_send(ctx, content, ephemeral=False, embed=None):
    await ctx.response.defer(ephemeral=ephemeral)
    await ctx.followup.send(content=content, embed=embed)


async def handle_exception(ctx, e):
    await defer_and_send(ctx, f"An error occurred: {e}", ephemeral=True)


@client.event
async def on_ready():
    print("Sync V2 !")
    print("Connecté en tant que : {0.user}".format(client))
    try:
        synced = await client.tree.sync(guild=discord.Object(id=testingserver))
        print(f"Synced {len(synced)} commands !")
    except Exception as e:
        print(e)
    print(f"Ready")


@client.tree.command(name="ping", description="Ping pong")
@app_commands.guilds(discord.Object(id=testingserver))
async def ping(ctx):
    await defer_and_send(ctx, "Pong !", ephemeral=True)


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
        await defer_and_send(ctx,f"Nickname for {member.display_name} changed to {new_nickname}",ephemeral=True,)
    except discord.Forbidden:
        await defer_and_send(ctx,"I don't have permission to change this user's nickname.",ephemeral=True,)
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
    await defer_and_send(ctx, f"you rolled a {dice_roll}!")


@client.tree.command(
    name="looking_color", description="Generate a picture with a specified hex color"
)
@app_commands.guilds(discord.Object(id=testingserver))
async def color_pic(ctx, hex_color: str):
    try:
        # Validate hex color code
        if not re.match(r"^#(?:[0-9a-fA-F]{3}){1,2}$", hex_color):
            await defer_and_send(ctx,"Invalid hex color code. Please use a format like #RRGGBB.",ephemeral=True,)
            return

        # Create a 100x100 image with the specified hex color
        img = Image.new("RGB", (100, 100), color=hex_color)

        # Save the image to a temporary file
        temp_file = BytesIO()
        img.save(temp_file, format="PNG")
        temp_file.seek(0)

        # Upload the image to Discord
        await ctx.response.defer(ephemeral=False)
        await ctx.followup.send(file=discord.File(temp_file, filename="color_pic.png"))
        
    except Exception as e:
        await handle_exception(ctx, e)


@client.tree.command(name="create_role", description="Create a new role with a specified name and color")
@app_commands.guilds(discord.Object(id=testingserver))
async def create_role(ctx, role_name: str, color: str):
    try:
        # Check if a role with the specified name already exists
        existing_role = discord.utils.get(ctx.guild.roles, name=role_name)
        if existing_role:
            await defer_and_send(ctx,f"A role with the name '{role_name}' already exists.",ephemeral=True,)
            return

        # Validate hex color code
        if not re.match(r"^#(?:[0-9a-fA-F]{3}){1,2}$", color):
            await defer_and_send(ctx,"Invalid hex color code. Please use a format like #RRGGBB.",ephemeral=True)
            return

        # Convert hex color code to discord.Color
        role_color = discord.Color(int(color.lstrip("#"), 16))

        # Create a new role with the specified color
        new_role = await ctx.guild.create_role(name=role_name, color=role_color)
        await defer_and_send(ctx,f"Role '{role_name}' created successfully with color {color}.",ephemeral=True,)
        
    except discord.Forbidden:
        await defer_and_send(ctx, "I don't have permission to create roles.", ephemeral=True)
        
    except Exception as e:
        await handle_exception(ctx, e)

@client.tree.command(name="change_role_color", description="Change the color of a specified role")
@app_commands.guilds(discord.Object(id=testingserver))
async def change_role_color(ctx, role_name: str, color: str):
    try:
        # Check if a role with the specified name exists
        role = discord.utils.get(ctx.guild.roles, name=role_name)
        if not role:
            await defer_and_send(ctx, f"No role found with the name '{role_name}'.", ephemeral=True)
            return

        # Validate hex color code
        if not re.match(r"^#(?:[0-9a-fA-F]{3}){1,2}$", color):
            await defer_and_send(ctx, "Invalid hex color code. Please use a format like #RRGGBB.", ephemeral=True)
            return

        # Convert hex color code to discord.Color
        role_color = discord.Color(int(color.lstrip("#"), 16))

        # Update the role color
        await role.edit(color=role_color)
        await defer_and_send(ctx, f"Role '{role_name}' color changed to {color}.", ephemeral=True)

    except discord.Forbidden:
        await defer_and_send(ctx, "I don't have permission to change role colors.", ephemeral=True)

    except Exception as e:
        await handle_exception(ctx, e)

client.run(token)
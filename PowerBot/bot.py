import discord
from discord.ext import commands
import asyncio
import json
import logging

# Setup logging
logging.basicConfig(level=logging.INFO)

# Load configuration
with open('config.json') as config_file:
    config = json.load(config_file)

intents = discord.Intents.default()
intents.members = True  # Enable GUILD_MEMBERS intent
intents.messages = True  # Enable MESSAGE CONTENT intent

bot = commands.Bot(command_prefix='/', intents=intents)

@bot.event
async def on_ready():
    logging.info(f'Logged in as {bot.user.name} (ID: {bot.user.id})')
    await bot.change_presence(activity=discord.Game(name="Under Construction"))
    # Register slash commands with the guild
    await bot.tree.sync(guild=discord.Object(id=1166927281646735442))  # Replace YOUR_GUILD_ID with your guild's ID

# Error handling for commands
@bot.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.CommandNotFound):
        await ctx.send('Command not found.')
    else:
        logging.error(f'An error occurred: {str(error)}')
        await ctx.send('An error occurred while processing the command.')

# Load your commands here
# Ensure that your commands are properly defined in 'commands.clean' and 'commands.stats' modules

async def setup():
    try:
        # Load your custom extensions (cogs)
        await bot.load_extension('commands.clean')
        await bot.load_extension('commands.stats')
        # Load other extensions here
    except Exception as e:
        logging.error(f'Failed to load extension: {e}')

async def main():
    try:
        await setup()
        await bot.start(config['token'])
    except Exception as e:
        logging.error(f'Bot encountered an error: {e}')

asyncio.run(main())

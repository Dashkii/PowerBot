import discord
from discord.ext import commands
import json

class BackupCommand(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name='backup', help='Back up server data')
    async def backup(self, ctx):
        # Ensure the user has the right permissions
        if not ctx.author.guild_permissions.administrator:
            await ctx.send('You do not have permission to use this command.')
            return

        backup_data = {
            'channels': [],
            'roles': [role.name for role in ctx.guild.roles]
        }

        for channel in ctx.guild.channels:
            channel_data = {
                'name': channel.name,
                'type': str(channel.type),
                'permissions': {},
                'messages': []
            }

            # Get channel permissions
            for role, perms in channel.overwrites.items():
                channel_data['permissions'][role.name] = dict(perms)

            # Get channel messages if it's a text channel
            if isinstance(channel, discord.TextChannel):
                async for message in channel.history(limit=100):  # Adjust limit as needed
                    channel_data['messages'].append({
                        'author': message.author.name,
                        'content': message.content
                    })

            backup_data['channels'].append(channel_data)

        # Save the backup to a file
        with open(f'{ctx.guild.name}_backup.json', 'w') as file:
            json.dump(backup_data, file, indent=4)

        await ctx.send('Backup completed.')

def setup(bot):
    bot.add_cog(BackupCommand(bot))

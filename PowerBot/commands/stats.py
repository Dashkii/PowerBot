import discord
from discord.ext import commands
from discord import app_commands

class StatsCommand(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(name='stats', description='Display server and user stats')
    @app_commands.guilds(discord.Object(id=1166927281646735442))  # Replace with your guild ID
    async def stats(self, interaction: discord.Interaction):
        guild = interaction.guild
        member = interaction.user

        embed = discord.Embed(title=f"Stats for {guild.name}", color=discord.Color.blue())
        embed.add_field(name="Server Creation Date", value=guild.created_at.strftime("%Y-%m-%d"), inline=True)
        embed.add_field(name="Total Members", value=str(guild.member_count), inline=True)
        embed.add_field(name="Total Roles", value=str(len(guild.roles)), inline=True)

        embed.add_field(name="Your Join Date", value=member.joined_at.strftime("%Y-%m-%d"), inline=True)
        embed.add_field(name="Your Roles", value=", ".join([role.name for role in member.roles if role.name != "@everyone"]), inline=True)

        await interaction.response.send_message(embed=embed)

async def setup(bot):
    await bot.add_cog(StatsCommand(bot))

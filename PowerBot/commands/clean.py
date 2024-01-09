import discord
from discord.ext import commands


class CleanCommand(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @discord.app_commands.command(description="Remove 'Initiate' role from members who also have 'Member' role")
    @discord.app_commands.guilds(discord.Object(id=1166927281646735442))  # Replace with your guild ID
    async def clean(self, interaction: discord.Interaction):
        # Defer the response as the operation might take more than 3 seconds
        await interaction.response.defer()

        member_role = discord.utils.get(interaction.guild.roles, name="Member")
        initiate_role = discord.utils.get(interaction.guild.roles, name="Initiate")

        if not member_role or not initiate_role:
            await interaction.followup.send("Roles not found.")
            return

        try:
            count = 0
            async for member in interaction.guild.fetch_members(limit=None):
                # Log member's name and their roles
                print(f"Processing Member: {member.name}, Roles: {[role.name for role in member.roles]}")

                if member_role in member.roles and initiate_role in member.roles:
                    await member.remove_roles(initiate_role)
                    print(f"Removed 'Initiate' role from: {member.name}")  # Log the removal action
                    count += 1

            # Send a follow-up message after processing is complete
            await interaction.followup.send(f"Clean operation completed. Roles removed from {count} members.")
        except Exception as e:
            # Send a follow-up message if an error occurs
            await interaction.followup.send(f"An error occurred: {e}")


async def setup(bot):
    await bot.add_cog(CleanCommand(bot))

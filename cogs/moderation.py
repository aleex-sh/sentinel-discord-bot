import discord
from discord.ext import commands
from discord import app_commands
import logging


class Moderation(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    # Kick a member command
    @app_commands.command(name='kick', description="Kick a member from the server.")
    @app_commands.describe(member='The member to kick', reason="Reason for the kick")
    async def kick_command(self, interaction: discord.Interaction, member: discord.Member, reason: str):
        if not interaction.user.guild_permissions.kick_members:
            return await interaction.response.send_message(
                "You do not have permission to kick members.",
                ephemeral=True
            )

        try:
            await member.kick(reason=reason)
            await interaction.response.send_message(f"{member} has been kicked from the server.")
            logging.info(f"{member} was kicked by {interaction.user} for: {reason}")
        except discord.Forbidden:
            await interaction.response.send_message(
                "I do not have permission to kick this user.",
                ephemeral=True
            )
            logging.error("Permission denied while attempting to kick a user.")
        except Exception as e:
            await interaction.response.send_message(
                f"An error occurred: {e}",
                ephemeral=True
            )
            logging.error(f"Kick error: {e}")

    # Ban a member command
    @app_commands.command(name='ban', description="Ban a member from the server.")
    @app_commands.describe(member='The member to ban', reason="Reason for the ban")
    async def ban_command(self, interaction: discord.Interaction, member: discord.Member, reason: str):
        if not interaction.user.guild_permissions.ban_members:
            return await interaction.response.send_message(
                "You do not have permission to ban members.",
                ephemeral=True
            )

        try:
            await member.ban(reason=reason)
            await interaction.response.send_message(f"{member} has been banned from the server.")
            logging.info(f"{interaction.user} banned {member} for: {reason}")
        except discord.Forbidden:
            await interaction.response.send_message(
                "I do not have permission to ban this user.",
                ephemeral=True
            )
            logging.error("Permission denied while attempting to ban a user.")
        except Exception as e:
            await interaction.response.send_message(
                f"An error occurred: {e}",
                ephemeral=True
            )
            logging.error(f"Ban error: {e}")

async def setup(bot: commands.Bot):
    await bot.add_cog(Moderation(bot))

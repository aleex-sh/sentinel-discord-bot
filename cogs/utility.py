import discord
from discord.ext import commands
from discord import app_commands
import logging


class Utility(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    # Ping command
    @app_commands.command(name='ping', description='Ping the bot to check if it is responsive.')
    async def ping_command(self, interaction: discord.Interaction):
        await interaction.response.send_message("Pong!")
        logging.info(f"/ping executed by {interaction.user}")

    # Clear chat messages command
    @app_commands.command(name='clear', description='Clear a number of messages from the chat.')
    @app_commands.describe(amount="Number of messages to delete (1-100)")
    async def clear_command(self, interaction: discord.Interaction, amount: int):
        if not interaction.user.guild_permissions.manage_messages:
            return await interaction.response.send_message(
                "You do not have permission to manage messages.",
                ephemeral=True
            )

        if amount < 1 or amount > 100:
            return await interaction.response.send_message(
                "Please enter a number between 1 and 100.",
                ephemeral=True
            )

        await interaction.response.defer(ephemeral=True)

        try:
            deleted = await interaction.channel.purge(limit=amount)
            await interaction.followup.send(
                f"{len(deleted)} message(s) have been deleted.",
                ephemeral=True
            )
            logging.info(f"{interaction.user} deleted {len(deleted)} messages in #{interaction.channel}.")
        except Exception as e:
            logging.error(f"Error during message purge: {e}")
            await interaction.followup.send(f"An error occurred: {e}", ephemeral=True)

async def setup(bot: commands.Bot):
    await bot.add_cog(Utility(bot))

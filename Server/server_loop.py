# Handle imports
import asyncio
from config import config, client, server_settings, save_server_settings

# Define variables

# Define methods
async def setup_server_loop():
    asyncio.ensure_future(update_servers())

async def update_servers():
    """
    Update the server states
    :return:
    """
    for guild in client.guilds:
        if not guild.id in server_settings:
            server_settings[guild.id] = server_settings["default"]

        if not guild.owner is None:
            server_settings[guild.id]["owner_id"] = guild.owner.id

    save_server_settings()

    await asyncio.sleep(config["server_poll_frequency"])
    await update_servers()
# Handle imports
import asyncio
from config import config, client, server_settings, default_server_settings, save_server_settings
import copy

# Define variables

# Define methods
async def setup_server_loop():
    """
    Start the server loop
    :return:
    """
    asyncio.ensure_future(update_servers())

async def update_servers():
    """
    Update the server states
    :return:
    """
    for guild in client.guilds:
        if not str(guild.id) in server_settings:
            server_settings[str(guild.id)] = copy.deepcopy(default_server_settings)

        if not guild.owner is None:
            server_settings[str(guild.id)]["owner_id"] = guild.owner.id

    save_server_settings()

    await asyncio.sleep(config["server_poll_frequency"])
    asyncio.ensure_future(update_servers())
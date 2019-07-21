# Handle imports
from config import config, client

# Define variables

# Define methods
async def set_bot_icon(guild):
    """
    Set the bot's user icon for a guild.
    :param guild: The guild to  update
    :return:
    """
    with open(config["bot_icon_file"], 'rb') as f:
        await client.user.edit(avatar=f.read())
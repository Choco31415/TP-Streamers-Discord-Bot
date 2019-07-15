# Handle imports
from discord.utils import get
from config import config, client
from loggers import logger

# Define variables

# Define methods
async def reset_lounge_category():
    """
    Checks if the lounge category is made, if not then makes it
    :return:
    """
    for guild in client.guilds:
        # Check each guild, make such it has the category
        lounge_category = get(guild.categories, name=config["lounges"]["category_name"])
        if lounge_category is None:
            logger.info("Lounge category has been made for guild {}.".format(guild.name))
            lounge_category = await guild.create_category_channel(config["lounges"]["category_name"])

        # Cleanup the category
        lounge_channel_found = False
        for tc in lounge_category.text_channels:
            if tc.name != config["lounges"]["channel_name"]:
                await tc.delete()
                logger.info("Deleted tc {} for guild {}.".format(tc.name, guild.name))
            else:
                lounge_channel_found = True
        if not lounge_channel_found:
            await guild.create_text_channel(config["lounges"]["channel_name"], category=lounge_category)
            logger.info("Lounge text channel made for guild {}.".format(guild.name))
        for vc in lounge_category.voice_channels:
            await vc.delete()
            logger.info("Deleted vc {} for guild {}.".format(vc.name, guild.name))
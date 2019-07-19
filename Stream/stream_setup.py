# Handle imports
from discord.utils import get
from config import client
from permissions import *
from Stream.stream_loop import *
from loggers import logger

# Define variables

# Define methods
async def setup_stream_channel(guild):
    """
    Ensure every guild has a stream channel
    :return:
    """

    # Check that each guild has channel
    stream_channel = get(guild.text_channels, name=config["stream"]["discord_channel"])

    # Create if needed
    if stream_channel is None:
        overwrites = {guild.default_role: lounge_tc_disallow,
                      guild.me: lounge_tc_allow}
        stream_channel = await guild.create_text_channel(
            config["stream"]["discord_channel"], overwrites=overwrites)

        logger.info("Stream channel created for guild {}.".format(guild.name))

    # Set  permissions
    await stream_channel.set_permissions(guild.default_role, overwrite=lounge_tc_read_only)
    await stream_channel.set_permissions(guild.me, overwrite=lounge_tc_allow)

    # Cleanup channel messages
    if not stream_channel.last_message_id is None:
        last_message = await stream_channel.fetch_message(stream_channel.last_message_id)
    else:
        last_message = None

    if last_message is None or last_message.author != client.user:
        await stream_channel.purge()

        embed = discord.Embed()
        embed.add_field(
            name="**Here is the current list of TagPro streams on Twitch:**\n",
            value="If you don't see your stream here, make sure your game is set to TagPro!\n",
            inline=False)

        embed.add_field(name="Streams", value="Waaaaaa Luiiiggii",
                        inline=False)
        m = await stream_channel.send("", embed=embed)

        logger.info("Purged stream channel on server {}.".format(guild.name))
    else:
        m = last_message

    m.embeds[0].color = int(config["stream"]["panel_color"], 16)

    add_stream_panel(m)

async def setup_stream_loop():
    asyncio.ensure_future(update_streams())
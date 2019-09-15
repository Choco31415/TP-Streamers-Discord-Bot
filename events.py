# Handle imports
from Lounges.lounge_setup import *
from Misc.misc_commands import *
from Server.server_loop import *
from Stream.stream_setup import *
from command_processing import *
from loggers import logger
from config import server_settings, default_server_settings
from bot_setup import *
import discord
import copy
from misc_helper import get_dm_channel

# Define variables

# Define methods
@client.event
async def on_ready():
    '''
    Notify that bot is ready.
    :return:
    '''
    for guild in client.guilds:
        try:
            await reset_lounge_category(guild)

            await setup_stream_channel(guild)

        except Exception:
            logger.info("Couldn't setup server {}.".format(guild.name))

    await setup_stream_loop()

    await setup_server_loop()
    # Separate loop. If one fails, all will
    try:
        for guild in client.guilds:
            await set_bot_icon(guild)
    except Exception:
        logger.info("Couldn't set bot profile picture.")

    # Set bot to look ready
    logger.info("The bot is ready!")
    print("The bot is ready!")
    await client.change_presence(activity=discord.Game(name="Github: {}".format(config["github_repo_name"])))

    for guild in client.guilds:
        logger.info("I am currently in guild {} with name {}.".format(guild.id, guild.name))

@client.event
async def on_message(message):
    '''
    Handles incoming messages.
    :param message: Posted message.
    :return:
    '''
    message.content = message.content.strip() # Remove excess whitespace
    message.content = " ".join(message.content.split()) # Remove duplicate whitespace

    if message.author == client.user:
        return
    if message.content.startswith(command_start): #TODO: Look at bot command prefix parameter for discord py library
        logger.info("User {} ran {} on guild {}.".format(message.author, message.content, message.guild.name))

        command = message.content.split(" ")[0].replace(command_start, "", 1).lower()

        command = resolve_command(command)

        if command in command_lookup:
            command_info = command_lookup[command]
            safe, args = await process_command_params(message, command_info)
            if safe:
                await command_info.run(message, args)
        else:
            logger.info("Command not recognized.")

@client.event
async def on_member_join(member):
    """
    Handles people joining the server.
    :param member: The member joining.
    :return:
    """
    # Handle lounge events
    for lounge in lounges:
        lounge.remove(member)

@client.event
async def on_voice_state_update(member, before, after):
    """
    Handles VoiceState change for a user.
    This includes voice channel change, muted/unmute
    :param member:
    :param before:
    :param after:
    :return:
    """
    # Handle lounge events
    if (before.channel != after.channel):
        # New voice channel, who dis

        # Add to new channel, do first as otherwise rapid switching = bugs
        new_lounge = get(lounges, vc=after.channel)
        if not new_lounge is None:
            await new_lounge.add_member(member)

        # Remove from old channel
        previous_lounge = get(lounges, vc=before.channel)
        if not previous_lounge is None:
            await previous_lounge.remove_member(member)

@client.event
async def on_guild_join(guild):
    """
    Handles joining a server.
    :param guild:
    :return:
    """
    logger.info("Joined guild {} with name {}.".format(guild.id, guild.name))

    if not str(guild.id) in server_settings:
        server_settings[str(guild.id)] = copy.deepcopy(default_server_settings)
        server_settings[str(guild.id)]["owner_id"] = guild.owner.id

        save_server_settings()

    await reset_lounge_category(guild)

    await setup_stream_channel(guild)
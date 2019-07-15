# Handle imports
import discord
from discord.utils import get
from command_processing import resolve_command
from command_registration import *
from config import server_settings

# Define variables
help_highlighter = "asciidoc"

# Define methods
async def role(message, args):
    '''
    Add or remove a role from a user
    :param message:
    :param args:
    :return:
    '''
    # Get a role object
    role = get(message.guild.roles, name=args[0])

    # Check that the role exists to be safe
    if role is None:
        await message.channel.send("This server doesn't support role {}!".format(args[0]))
    else:
        try:
            if role in message.author.roles:
                await message.author.remove_roles(role)
            else:
                await message.author.add_roles(role)
        except discord.errors.Forbidden:
            await message.channel.send("The bot is not powerful enough to handle {}!".format(args[0]))
async def help_role(message):
    roles = server_settings[message.guild.id]["roles"]
    print(roles)
    if len(roles) == 0:
        roles_message = "None"
    else:
        roles_message = ", ".join(roles)

    return "adds/removes role from a player, supported roles are: {}".format(roles_message)

register_command(func=role,
                 name="role",
                 category="misc",
                 help_func=help_role,
                 params=[
                     {"name": "role"}
                 ])

# Define commands
async def help(message, args):
    '''
    Gets help on a command.
    :param message: Message that is command.
    :param args: Command args
    :return:
    '''
    channel = message.channel

    if len(args) == 0:
        # Send every help message
        reply = "This bot supports the following commands:\n```{}".format(help_highlighter)

        command_category = "" # Initial value
        for command in command_lookup.keys():
            command_info = command_lookup[command]
            previous_category = command_category
            command_category = command_info.get_category()

            if previous_category != command_category:
                reply += "\n== {} ==\n".format(command_category.capitalize())

            help_message = await command_info.get_help(message, include_params=False)
            reply += help_message + "\n"

        reply += "\n```"

        await channel.send(reply)
    else:
        # Send help message
        help_for = resolve_command(args[0])

        if help_for not in command_lookup:
            await channel.send("'{}' is not recognized. Run !help for a general list of commands.".format(help_for))
        else:
            command_info = command_lookup[help_for]
            help_message = await command_info.get_help(message, include_params=True)
            reply = "```{}\n{}\n```\n".format(help_highlighter, help_message)
            await channel.send(reply)
register_command(func=help,
                 name="help",
                 category="misc",
                 help_message="get help on a command",
                 params=[
                     {"name": "command", "check": "exists",  "attributes": ["optional"]}
                 ])

async def vc_find(message, args):
    """
    Finds the voice channel a user is in.
    :param message: Message that is command
    :param args: Command args
    :return:
    """
    guild = message.guild

    to_find = args[0]

    for vc in guild.voice_channels:
        if to_find in vc.members:
            await message.channel.send("Found user {} in vc {}!".format(to_find.name, vc.name))
            break
    else:
        await message.channel.send("Could not find user {}.".format(to_find.name))
register_command(func=vc_find,
                 name="find",
                 category="misc",
                 help_message="finds what voice channel a member is in",
                 params=[
                     {"name": "username", "check": "exists"}
                 ])
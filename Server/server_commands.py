# Handle imports
from discord.utils import get
from command_registration import *
from config import server_settings, save_server_settings

# Define variables

# Define methods
async def set_roles(message, args):
    '''
    Set the roles for a server
    :param message:
    :param args:
    :return:
    '''
    if message.author.id == server_settings[message.guild.id]["owner_id"]:
        valid = True
        for role in args:
            if get(message.guild.roles, name=role) is None:
                await message.channel.send("{} is not a valid role. :(".format(role))
                valid = False

        if valid:
            server_settings[message.guild.id]["roles"] = args

            save_server_settings()

            await message.channel.send("Users may now toggle these roles:  {}".format(", ".join(args)))
    else:
        await message.channel.send("This command can only be run by the server owner!")
register_command(func=set_roles,
                 name="set_roles",
                 category="admin",
                 help_message="set the roles for the server",
                 params=[
                     # Nothing specific
                 ],
                 owner_only=True)
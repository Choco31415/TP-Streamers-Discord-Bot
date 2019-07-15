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
    if message.author.id == server_settings[str(message.guild.id)]["owner_id"]:
        valid = True
        role_ids = []
        for arg in args:
            role = get(message.guild.roles, name=arg)
            if role is None:
                await message.channel.send("{} is not a valid role. :(".format(arg))
                valid = False
            else:
                role_ids.append(role.id)

        if valid:
            server_settings[str(message.guild.id)]["role_ids"] = role_ids

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
# Handle imports
from discord.utils import get
from command_registration import *
from config import server_settings, save_server_settings

# Define variables

# Define methods
async def toggle_role(message, args):
    '''
    Set the roles for a server
    :param message:
    :param args:
    :return:
    '''
    role = args[0]

    if role.id in server_settings[str(message.guild.id)]["role_ids"]:
        server_settings[str(message.guild.id)]["role_ids"].remove(role.id)
        await message.channel.send(
            "Users now cannot toggle role {}.".format(role.name))
    else:
        server_settings[str(message.guild.id)]["role_ids"].append(role.id)
        await message.channel.send(
            "Users now can toggle role {}.".format(role.name))

    save_server_settings()

register_command(func=toggle_role,
                 name="toggle_role",
                 category="admin",
                 help_message="enable/disable a role for users to assign",
                 params=[
                     {"name": "role", "check": "exists", "attributes": ["extended"]}
                 ],
                 owner_only=True)
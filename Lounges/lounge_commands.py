# Handle imports
from discord.utils import get
from Lounges.lounges import create_lounge, lounges
from command_registration import *

# Define variables

# Define methods
def lounge_command(arg_position):
    """
    Auto obtain a lounge for a command
    :param arg_position: The arg position of the lounge name
    :return:
    """
    def real_decorator(func):
        async def wrapper(message, args):
            if len(args) == arg_position:
                lounge = get(lounges, tc=message.channel)
                if lounge is None:
                    await message.channel.send("This isn't a lounge! :o")
            else:
                lounge = get(lounges, name=args[arg_position])

            if not lounge is None:
                await func(message, args, lounge)
        return wrapper
    return real_decorator

@lounge_command(1)
async def lounge_admin(message, args, lounge):
    """
    Make a member a lounge admin
    :param message:
    :param args:
    :return:
    """
    await lounge.toggle_admin(member=args[0], requestor=message.author)
register_command(func=lounge_admin,
                 name="admin",
                 category="lounge",
                 help_message="adds/removes a player as a lounge admin",
                 params=[
                     {"name": "username", "check": "exists"},
                     {"name": "lounge", "check": "exists", "attributes": ["optional"]}
                 ])

@lounge_command(0)
async def lounge_admin_list(message, args, lounge):
    """
    Check what admins there are for a lounge
    :param message:
    :param args:
    :return:
    """
    admin_names = [admin.name for admin in lounge.get_admins()]
    await message.channel.send("The lounge has these admins: {}".format(", ".join(admin_names)))
register_command(func=lounge_admin_list,
                 name="admin_list",
                 category="lounge",
                 help_message="list the admins of a lounge",
                 params=[
                     {"name": "lounge", "check": "exists", "attributes": ["optional"]}
                 ])

@lounge_command(1)
async def lounge_bypass(message, args, lounge):
    """
    Bypasses a lounge's lock.
    :param message:
    :param args:
    :return:
    """
    await lounge.bypass_member(member=args[0], requestor=message.author)
register_command(func=lounge_bypass,
                 name="bypass",
                 category="lounge",
                 help_message="allow/reset a player to bypass a locked lounge",
                 params=[
                     {"name": "username", "check": "exists"},
                     {"name": "lounge", "check": "exists", "attributes": ["optional"]}
                 ])

@lounge_command(0)
async def lounge_lock(message, args, lounge):
    """
    Locks a lounge
    :param message: Message that is command
    :param args: Command args
    :return:
    """
    await lounge.toggle_lock(requestor=message.author)
register_command(func=lounge_lock,
                 name="lock",
                 category="lounge",
                 help_message="locks a lounge, making it private",
                 params=[
                     {"name": "lounge", "check": "exists", "attributes": ["optional"]}
                 ])

@lounge_command(0)
async def lounge_delete(message, args, lounge):
    """
    Deletes a lounge
    :param message: Message that is command
    :param args: Command args
    :return:
    """
    await lounge.request_delete(requestor=message.author)
register_command(func=lounge_delete,
                 name="delete",
                 category="lounge",
                 help_message="deletes a lounge",
                 params=[
                     {"name": "lounge", "check": "exists", "attributes": ["optional"]}
                 ])

@lounge_command(1)
async def lounge_kick(message, args, lounge):
    """
    Deletes a lounge
    :param message: Message that is command
    :param args: Command args
    :return:
    """
    await lounge.kick_member(args[0], requestor=message.author)
register_command(func=lounge_kick,
                 name="kick",
                 category="lounge",
                 help_message="kicks a player from a lounge",
                 params=[
                     {"name": "username", "check": "exists"},
                     {"name": "lounge", "check": "exists", "attributes": ["optional"]}
                 ])

async def lounge_new(message, args):
    """
    Makes a new lounge.
    :param message: Message that is command
    :param args: Command args
    :return:
    """
    users_lounges = get(lounges, creator=message.author)
    if users_lounges is None:
        guild = message.guild
        lounge_name = args[0]
        creator = message.author

        await create_lounge(guild, lounge_name, creator)

        await message.channel.send("Created lounge {}.".format(lounge_name))
    else:
        await message.channel.send("You already have lounge {}.".format(users_lounges.name))
register_command(func=lounge_new,
                 name="lounge",
                 alias_list=["l"],
                 category="lounge",
                 help_message="creates a lounge",
                 params=[
                     {"name": "lounge", "check": "not exists", "attributes": ["extended"]}
                 ])
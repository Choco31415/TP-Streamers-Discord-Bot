# Handle imports
import discord

# Define variables
lounge_tc_allow = discord.PermissionOverwrite(read_messages=True, send_messages=True, read_message_history=True)
lounge_tc_disallow = discord.PermissionOverwrite(read_messages=False, send_messages=False, read_message_history=False)
lounge_tc_read_only = discord.PermissionOverwrite(send_messages=False)
lounge_vc_allow_bot = discord.PermissionOverwrite(connect=True, stream=True, move_members=True)
lounge_vc_allow = discord.PermissionOverwrite(connect=True, stream=True)
lounge_vc_disallow = discord.PermissionOverwrite(connect=False, stream=False)
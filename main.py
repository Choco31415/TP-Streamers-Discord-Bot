# Handle imports
from config import tokens
from events import *
from Server.server_commands import *
from Lounges.lounge_commands import *
from Misc.misc_commands import *

# Define constants

# Run stuff
client.run(tokens["discord_token"])
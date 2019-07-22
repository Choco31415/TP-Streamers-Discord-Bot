# Handle imports

# Define variables

# Define methods
async def get_dm_channel(user):
    dm_channel = user.dm_channel
    if dm_channel is None:
        dm_channel = await user.create_dm()
    return dm_channel
# Handle imports
import json
import discord

# Define variables
config_file = "Resources/config.json"
token_file = "Resources/token.json"
server_settings_file = "Resources/server_settings.json"

## config.json
with open(config_file, "r") as f:
    config = json.loads(f.read())

## token.json
with open(token_file, "r") as f:
    tokens = json.loads(f.read())

## server_settings.json
with open(server_settings_file, "r") as f:
    server_settings = json.loads(f.read())

def save_server_settings():
    with open(server_settings_file, "w") as f:
        f.write(json.dumps(server_settings))

client = discord.Client()
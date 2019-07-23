# TP-Streamers-Discord-Bot
This bot helps manage the TagPro streamers Discord server, providing several useful commands.

Currently built on Python 3.6.1. 3.7+ is not supported. To change python versions,
update `monitor.sh`.

## Running

### Setup

Add a `token.json` file to Resources. It must contain values `discord_token` and
`twitch_client_id` for full functionality.

### Starting

Run the following command:

`nohup monitor.sh &`

This creates a crash-resilient, terminal independent start.

## Commands

To list this bot's commands, type "!help", and the bot will respond.
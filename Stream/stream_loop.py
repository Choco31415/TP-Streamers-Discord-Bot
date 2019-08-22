# Handle imports
import asyncio
import json
import requests
from config import config, tokens
import datetime
import pytz
from loggers import logger

# Define variables
stream_panels = []

# Define methods
def add_stream_panel(e):
    """
    Add a comment where stream info will be added
    :param e:
    :return:
    """
    global stream_panels

    stream_panels.append(e)

async def update_streams():
    """
    Update the game streams
    :return:
    """
    while True:
        r = requests.get(config["stream"]["twitch_api_url"], params={'game': config["stream"]["twitch_game"], "client_id": tokens["twitch_client_id"]})
        try:
            r_json = json.loads(r.text)
        except ValueError:
            logger.info("Couldn't load twitch response as json, got HTML status {}.".format(r.status_code))
        else:
            streams = r_json["streams"]

            if len(streams) == 0:
                stream_header = "**No TagPro streams found :c**\n"
                stream_message = "Try making your own stream!\n"
            else:
                stream_header = "**Found {} streams.**".format(len(streams))
                stream_message = ""
                for stream in streams:
                    stream_name = stream['channel']['status']
                    host = stream['channel']['display_name']
                    url = stream['channel']['url']
                    stream_message += "{} is streaming \"{}\" at: {}\n".format(host, stream_name, url)

            d = datetime.datetime.now()
            timezone = pytz.timezone(config["time_zone"])
            d_localized = timezone.localize(d)
            stream_message +=  "*Updated: {}*".format(d_localized.strftime("%I:%M %p %Z").lower())

            for m in stream_panels:
                embed = m.embeds[0]
                embed.set_field_at(1, name=stream_header, value=stream_message)
                await m.edit(embed=embed)

        await asyncio.sleep(config["stream"]["update_frequency"])

async def setup_stream_loop():
    asyncio.ensure_future(update_streams())
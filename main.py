from functools import lru_cache
import logging
import os
from pathlib import Path

import discord
from jinja2 import Environment, FileSystemLoader, select_autoescape

logger = logging.getLogger('discord')
logger.setLevel(logging.DEBUG)
handler = logging.FileHandler(
    filename='discord.log', encoding='utf-8', mode='w')
handler.setFormatter(logging.Formatter(
    '%(asctime)s:%(levelname)s:%(name)s: %(message)s'))
logger.addHandler(handler)

intents = discord.Intents.default()
intents.typing = False
intents.presences = False
intents.members = True
intents.guilds = True
client = discord.Client(intents=intents)


@lru_cache
def get_welcome_message():
    env = Environment(
        loader=FileSystemLoader('templates'),
        autoescape=select_autoescape()
    )
    template = env.get_template('welcome_message.html')
    return template.render(
        rules=channels_reference['rules'].id,
        introductions=channels_reference['introductions'].id,
        what_are_you_reading=channels_reference['what-are-you-reading'].id,
        tools=channels_reference['tools'].id,
        discussion=channels_reference['discussion'].id,
        ml_jobs=channels_reference['ml-jobs'].id,
        memes=channels_reference['memes'].id
    )


def setup_channels_reference(guild):
    # TODO: implement a class to get rid of the global variables
    global channels_reference
    channels_reference = {}
    for channel in guild.channels:
        if channel.type == discord.ChannelType.text:
            channels_reference[channel.name] = channel
    return channels_reference


@client.event
async def on_ready():
    print('We have logged in as {0.user}'.format(client))
    setup_channels_reference(client.guilds[0])
    get_welcome_message()


@client.event
async def on_message(message: discord.Message):
    if message.author == client.user:
        return
    if message.channel.name != 'bot-test':
        return
    logger.info(f'MSG_CONTENT: {message.content}')
    logger.info(f'MSG: {message}')
    if message.content.startswith('$hello'):
        await message.channel.send('Hello! :wave:')


@client.event
async def on_member_join(member: discord.Member):
    logger.info(f'A new member joined, info: {member}')
    guild = member.guild
    channel = guild.get_channel(channel_id=944447918524481546)
    await channel.send(f'A new member joined, info: {member}')
    await channel.send(get_welcome_message())

client.run(os.environ.get('BOT_TOKEN'))

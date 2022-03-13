import logging
import os
from pathlib import Path

import discord

logger = logging.getLogger('discord')
logger.setLevel(logging.DEBUG)
handler = logging.FileHandler(filename='discord.log', encoding='utf-8', mode='w')
handler.setFormatter(logging.Formatter('%(asctime)s:%(levelname)s:%(name)s: %(message)s'))
logger.addHandler(handler)

intents = discord.Intents.default()
intents.typing = False
intents.presences = False
intents.members = True
intents.guilds = True
client = discord.Client(intents=intents)

template_path = Path('./templates')
with (template_path / 'welcome_message.txt').open(mode='r') as f:
    welcome_template = f.read()

@client.event
async def on_ready():
    print('We have logged in as {0.user}'.format(client))


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
    if str(member) == 'testing1#9745':
        await member.send(welcome_template)
    channel = guild.get_channel(channel_id=944447918524481546)
    await channel.send(f'A new member joined, info: {member}')

client.run(os.environ.get('BOT_TOKEN'))

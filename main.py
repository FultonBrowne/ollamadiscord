import discord

from langchain.llms.ollama import Ollama

import json

from langchain.memory import ChatMessageHistory


async def gather(ai):
    ret = []
    async for x in ai:
        ret.append(x)
    return ret


def open_config():
    with open('config.json', 'r') as config_file:
        return json.load(config_file)


async def separate_messages(channel, history):
    messages = channel.history(limit=50)
    ml = await gather(messages)
    reversed(ml)
    for i in ml:
        if i.author == client.user:
            history.add_ai_message(i.content)
        else:
            history.add_user_message(i.content)


config = open_config()
DISCORD_TOKEN = config.get('token')
MODEL_NAME = config.get('model')
ADDRESS = config.get('address')
llm = Ollama(model="llama2")
# Define the bot and its intents
intents = discord.Intents.default()
intents.messages = True
intents.dm_messages = True

client = discord.Client(intents=intents)


@client.event
async def on_ready():
    print(f'We have logged in as {client.user}')


@client.event
async def on_message(message):
    if ((message.author != client.user) and
            (isinstance(message.channel, discord.DMChannel) or client.user in message.mentions)):
        history = ChatMessageHistory()
        await separate_messages(message.channel, history)
        history.add_user_message(message.content)
        async with message.channel.typing():
            t = llm.predict_messages(messages=history.messages)
            await message.channel.send(t.content)


client.run(DISCORD_TOKEN)

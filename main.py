import discord

from langchain.llms.ollama import Ollama

import json

from langchain.memory import ChatMessageHistory


async def separate_messages(channel, history):
    # Check if the bot has permissions to read the channel history

    # Fetch the last 50 messages from the channel
    messages = channel.history(limit=50)
    async for i in messages:
        if i.author == client.user:
            history.add_ai_message(i.content)
        else:
            history.add_user_message(i.content)


if __name__ == "__main__":

    with open('config.json', 'r') as config_file:
        config = json.load(config_file)
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
        print("start message")
        history = ChatMessageHistory()
        await separate_messages(message.channel, history)
        # Ignore messages sent by the bot
        if message.author == client.user:
            return

        # Check if the message is in DMs
        if isinstance(message.channel, discord.DMChannel) or client.user in message.mentions:
            async with message.channel.typing():
                t = llm.predict_messages(messages=history.messages)
                await message.channel.send(t.content)
        # elif message.channel.id in allowed_channels:
        else:
            return

    # Replace 'YOUR_BOT_TOKEN' with your actual bot token
    client.run(DISCORD_TOKEN)

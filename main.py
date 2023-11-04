import discord

import json


if __name__ == "__main__":

    with open('config.json', 'r') as config_file:
        config = json.load(config_file)
    DISCORD_TOKEN = config.get('token')

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
        # Ignore messages sent by the bot
        if message.author == client.user:
            return

        # Check if the message is in DMs
        if isinstance(message.channel, discord.DMChannel):
            await message.channel.send('Hello! This is a DM conversation.')

        # Or check if the message is in a specific channel
        #elif message.channel.id in allowed_channels:
        #    await message.channel.send('This is one of the allowed channels.')


    # Replace 'YOUR_BOT_TOKEN' with your actual bot token
    client.run(DISCORD_TOKEN)
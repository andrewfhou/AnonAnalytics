import discord

client = discord.Client()
token = ""

with open('secret', 'r') as f:
    token = f.read()


@client.event
async def on_ready():
    print('Logged in as {0.user}'.format(client))


@client.event
async def on_message(message):
    if message.author == client.user:
        return
    elif message.content == 'ping':
        await message.channel.send('pong')


client.run(token)

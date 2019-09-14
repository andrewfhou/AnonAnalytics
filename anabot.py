import discord
import csv

client = discord.Client()
token = ""

filename = 'message_log.csv'
with open(filename, mode='w+') as f:
        f = csv.writer(f, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
        f.writerow(['Time', 'Channel', 'Attachment?'])

with open('secret', 'r') as f:
    token = f.read()

@client.event
async def on_ready():
    print('Logged in as {0.user}'.format(client))


@client.event
async def on_message(message):
    if message.author == client.user or message.author.bot:
        return
    elif message.content == 'ping':
        print('Message channel: {} at {}'.format(message.channel, message.created_at))
        await message.channel.send('Message received!')
        # await message.channel.send('pong')
    elif message.content == '!quit':
        await message.channel.send('Goodbye!')
        print('Exiting...')
        await client.close()

    with open(filename, mode='w') as f:
        f.writerow([message.created_at, message.channel, (message.attachments is not None)])

client.run(token)

import discord
import csv
import json

client = discord.Client()
token = ""

filename = 'message_log.csv'

with open('secret', 'r') as f:
    token = f.read()


def log_message(message):
    channel = message.channel.name
    date = message.created_at
    with open('test.csv', 'a') as csvf:
        writer = csv.writer(csvf, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
        writer.writerow([channel, date.month, date.day, date.year, date.hour, date.minute, date.second])


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
    elif message.content == '!q':
        await message.channel.send('Goodbye!')
        print('Exiting...')
        await client.close()

    elif message.content == '!lh':
        # garbage channel ID = 622465697896857619
        channel = client.get_channel(622465697896857619)
        message_list = await channel.history().flatten()
        last_message = message_list[1]
        print(last_message.content)
        log_message(last_message)


'''
    with open(filename, mode='a') as f:
        f = csv.writer(f, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
        f.writerow([message.created_at, message.channel, message.author, message.content])

with open(filename, mode='w+') as f:
    f = csv.writer(f, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
    f.writerow(['Time', 'Channel', 'Attachment?'])
'''

client.run(token)

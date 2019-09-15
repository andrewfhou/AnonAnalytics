import discord
import csv
import json
import os
from lightning import lightning

lgn = Lightning()
client = discord.Client()
token = ""

filename = 'log.csv'

with open('secret', 'r') as f:
    token = f.read()

if not os.path.exists(filename): # add csv headers if file does not exist
    with open(filename, 'a') as f:
        writer = csv.writer(f, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
        writer.writerow(
            ['channel', 'online', 'offline', 'bot?', 'month', 'day', 'year', 'hour', 'minute', 'second'])


def num_online(cli):
    online = 0
    offline = 0
    bot = 0
    for m in cli.get_all_members():
        if bool(m.bot):
            bot += 1
        elif str(m.status) == 'offline':
            offline += 1
        else:
            online += 1

    print('online: {}, offline: {}, bot: {}'.format(online, offline, bot))
    return online, offline, bot


def log_message(message):
    channel = message.channel.name
    date = message.created_at
    online, offline, bot = num_online(client)
    with open(filename, 'a') as f:
        writer = csv.writer(f, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
        writer.writerow(
            [channel, online, offline, bot, date.month, date.day, date.year, date.hour, date.minute, date.second])


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

    elif message.content == '!n':
        online, offline, bots = num_online(client)
        await message.channel.send('Online: {}; Offline: {}; Bots: {}'.format(online, offline, bots))

    elif message.content == '!q':
        await message.channel.send('Goodbye!')
        print('Exiting...')
        await client.close()

    else:
        log_message(message)


client.run(token)

# -*- coding: utf-8 -*-

from __future__ import print_function
from apiclient.discovery import build
from httplib2 import Http
from oauth2client import file, client, tools
import discord, asyncio, time
from discord.ext import commands

# Setup the Sheets API
SCOPES = 'https://www.googleapis.com/auth/spreadsheets'
store = file.Storage('credentials.json')
creds = store.get()
if not creds or creds.invalid:
    flow = client.flow_from_clientsecrets('client_secret.json', SCOPES)
    creds = tools.run_flow(flow, store)
service = build('sheets', 'v4', http=creds.authorize(Http()))
print('Connected to Google Sheets')

# Get sheet ID
file = open('SHID.txt', 'r')
SH_ID = file.read()

print('Opened SH_ID')

command_prefix = '!'
bot = commands.Bot(command_prefix)


@bot.command()
async def addTime(ctx, a: str):
    date = ctx.message.created_at
    date = str(date.month) + '/' + str(date.day) + '/' + str(date.year)
    await ctx.send(ctx.message.created_at)
    result = service.spreadsheets().values().get(spreadsheetId=SH_ID, range='A2').execute()
    values = result.get('values', [])
    x = values[0][0][0]
    service.spreadsheets().values().update(spreadsheetId=SH_ID, range='B' + str(x), valueInputOption='USER_ENTERED',
                                           body={"values": [[date]]}).execute()
    service.spreadsheets().values().update(spreadsheetId=SH_ID, range='C' + str(x), valueInputOption='USER_ENTERED',
                                           body={"values": [[a]]}).execute()
    x += 1
    service.spreadsheets().values().update(spreadsheetId=SH_ID, range='A2', valueInputOption='USER_ENTERED',
                                           body={"values": [[str(x)]]}).execute()
    await ctx.send('Time Added!')


@bot.command()
async def getAverage(ctx):
    result = service.spreadsheets().values().get(spreadsheetId=SH_ID, range='A4').execute()
    values = result.get('values', [])
    time = values[0][0]
    await ctx.send(time)


@bot.command()
async def getOnDate(ctx, a: str):
    result = service.spreadsheets().values().get(spreadsheetId=SH_ID, range='A2').execute()
    print(result)
    values = result.get('values', [])
    print(values)
    x = int(values[0][0])
    print(x)
    result = service.spreadsheets().values().get(spreadsheetId=SH_ID, range='B1:C' + str(x)).execute()
    print(result)
    values = result.get('values', [])
    print(values)
    for row in values:
        if row[0].find(a) != -1:
            await ctx.send(row[1])
            return
    await ctx.send('No Date Found')


@bot.command()
async def testSend(ctx):
    await ctx.send('hi')


@bot.event
async def on_message(message):
    if message.author.id == bot.user.id:
        return
    elif message.author.id == 185214105072697345:
        jackId = '<@185214105072697345>'
        await message.channel.send('<@185214105072697345> is a bitch')


@bot.event
async def on_ready():
    print('Logged in as')
    print(bot.user.name)
    print(bot.user.id)
    print('----------')


bot.run('insert token here')

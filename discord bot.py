import discord
from discord.ext.commands import Bot
from discord.ext import commands
import asyncio
import time

bot = commands.Bot(command_prefix='!')

@bot.event
async def on_ready():
    print ("Locked and loaded")
    print (bot.user.name)
    print (bot.user.id)

@bot.command(pass_context=True)
async def ping(ctx)
    await bot.channel.send("pong")
    print ("ponged")

bot.run("token")

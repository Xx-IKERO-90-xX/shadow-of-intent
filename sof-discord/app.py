import discord
from discord.ext import commands
import os
import sys


intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix='!', intents=intents)

@bot.event
async def on_ready():
    print(f'Logged in as {bot.user}')


if __name__ == "__main__":
    bot.run('token')
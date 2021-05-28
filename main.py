import discord
from discord.ext import commands
from os import environ, listdir

# Get emote name & id: \:PainChamp:
# Animated emoji: <a:rikkaBongo:697839129257312286>
# Emote example: <:PainChamp:695437777763958874>
# Embed color: color = discord.Color(0x + hex)
# <@user_id> (or <@!user_id> if the member has a nickname.)

token = environ.get('TOKEN')

# https://discordpy.readthedocs.io/en/latest/intents.html?highlight=intents
intents = discord.Intents.all()

client = commands.Bot(command_prefix='!', case_insensitive=True, help_command=None, intents=intents)


# Loading cogs
for filename in listdir("./cogs"):
    if filename.endswith(".py"):
        client.load_extension("cogs.{}".format(filename[:-3]))


client.run(token)
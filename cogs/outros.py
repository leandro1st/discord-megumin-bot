import discord
from discord.ext import commands
from datetime import datetime, timezone
import random as r
from pytz import timezone #timezone()
import re
import requests

class Outros(commands.Cog, name="Diversos"):
    """Comandos diversos"""


    def __init__(self, client):
        self.client = client


    # !dm - sends dm to mentioned person
    @commands.command(usage="<member> <message>", description="Send a DM to a member")
    async def dm(self, ctx, member: discord.Member = None, *, message = None):
        if member and message:
            # Sending dm and deleting the message
            channel = await member.create_dm()
            await channel.send("**<@!{}>** from **{}:** {}".format(ctx.message.author.id, ctx.guild.name, message))
            await ctx.message.delete()
        else:
            embed = discord.Embed(
                color = discord.Color(0xff0000),
                timestamp = datetime.utcnow(),
                description = "**Sintaxe incorreta! Use !dm <member> <message>**"
            )

            embed.set_footer(icon_url='{}'.format(ctx.message.author.avatar_url_as(format=None, static_format='png')).split("?")[0], text="Gerado por {0}".format(ctx.message.author.name))
            await ctx.reply(embed=embed)

    # Checking if arguments are valid
    @dm.error
    async def dm_error(self, ctx, error):
        if isinstance(error, commands.BadArgument):
            embed = discord.Embed(
                color = discord.Color(0xff0000),
                timestamp = datetime.utcnow(),
                description = "**Sintaxe incorreta! Use !dm <member> <message>**"
            )

            embed.set_footer(icon_url='{}'.format(ctx.message.author.avatar_url_as(format=None, static_format='png')).split("?")[0], text="Gerado por {0}".format(ctx.message.author.name))
            await ctx.reply(embed=embed)


    # !hello - hello
    @commands.command(description="Sup")
    async def hello(self, ctx):
        await ctx.reply("Yo")


    # !random - random number between 2 numbers
    @commands.command(usage="<min>, <max>", description="Pick a random number from `min` to `max`")
    async def random(self, ctx, *, numero = None):
        # Verificando se somente um número inteiro foi fornecido, aceitando espaços em branco entre ele
        if numero and re.compile('^\s*(-?\d+)\s*$').search(numero):
            m = re.compile('^\s*(-?\d+)\s*$').search(numero)
            n1 = int(m.group(1))

            if n1 <= 0:
                random_number = r.randint(n1, 0)
            else:
                random_number = r.randint(0, n1)

            await ctx.reply(random_number)
        # Verificando se há dois números inteiros separados por uma vírgula, aceitando espaços em branco entre as palavras
        elif numero and re.compile('^\s*(-?\d+)\s*,\s*(-?\d+)\s*$').search(numero):
            m = re.compile('^\s*(-?\d+)\s*,\s*(-?\d+)\s*$').search(numero)
            n1 = int(m.group(1))
            n2 = int(m.group(2))
            
            if n1 <= n2:
                random_number = r.randint(n1, n2)
            else:
                random_number = r.randint(n2, n1)

            await ctx.reply(random_number)
        else:
            embed = discord.Embed(
                color = discord.Color(0xff0000),
                timestamp = datetime.utcnow(),
                description = "**Sintaxe incorreta! Use !random <min>, <max>**"
            )
            
            embed.set_footer(icon_url='{}'.format(ctx.message.author.avatar_url_as(format=None, static_format='png')).split("?")[0], text="Gerado por {0}".format(ctx.message.author.name))
            await ctx.reply(embed=embed)


    # !junior - display junior's pic
    @commands.command(description="Junior zuado")
    async def junior(self, ctx):
        embed = discord.Embed(
            color = discord.Color.gold(),
            timestamp = datetime.utcnow()
        )

        embed.set_image(url='https://image.prntscr.com/image/BemzF5RlTxa8Tdog35W5Aw.jpg')
        embed.set_footer(icon_url='{}'.format(ctx.message.author.avatar_url_as(format=None, static_format='png')).split("?")[0], text="Gerado por {0}".format(ctx.message.author.name))
        message = await ctx.reply(embed=embed)
        await message.add_reaction('<:PepeWTF:720074659294478377>')


    # !now - now
    @commands.command(description="Display current datetime")
    async def now(self, ctx):
        """ Auto detect timezone (working example 1) datetime.timezone """
        # local_now = datetime.now(timezone.utc).astimezone()
        # await ctx.reply(local_now.strftime("%a, %b %d %Y %X %Z"))
        """ Working example 2 (EST gmt -5) timezone.pytz """
        # now_utc = datetime.now(timezone('UTC')).astimezone(timezone('EST'))
        # await ctx.reply(now_utc.strftime("%a, %b %d %Y %X %Z"))

        # utc verification and stuff, you can change America/Sao_Paulo to another timezone See: https://gist.github.com/heyalexej/8bf688fd67d7199be4a1682b3eec7568
        local_now = datetime.now(timezone('UTC')).astimezone(timezone('America/Sao_Paulo'))
        if local_now.strftime("%Z")[1] == '0':
            if len(local_now.strftime("%Z")) != 3:
                utc = local_now.strftime("%Z")[0] + local_now.strftime("%Z")[2] + ":" + local_now.strftime("%Z")[3:]
                await ctx.reply(local_now.strftime("Today is %d/%m/%Y (%A), **%X (UTC{})**").format(utc))
            else:
                utc = local_now.strftime("%Z")[0] + local_now.strftime("%Z")[2:]
                await ctx.reply(local_now.strftime("Today is %d/%m/%Y (%A), **%X (UTC{})**").format(utc))
        elif local_now.strftime("%Z").isalpha():
            await ctx.reply(local_now.strftime("Today is %d/%m/%Y (%A), **%X %Z**"))
        elif local_now.strftime("%Z")[1] != '0':
            if len(local_now.strftime("%Z")) != 3:
                utc = local_now.strftime("%Z")[:3] + ":" + local_now.strftime("%Z")[3:]
                await ctx.reply(local_now.strftime("Today is %d/%m/%Y (%A), **%X (UTC{})**").format(utc))
            else:
                await ctx.reply(local_now.strftime("Today is %d/%m/%Y (%A), **%X (UTC%Z)**"))


def setup(client):
    client.add_cog(Outros(client))
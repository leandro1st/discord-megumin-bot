from datetime import datetime, timezone
import random
from pytz import timezone #timezone()
import re
import urllib.parse, urllib.request
import requests
import math
from decimal import Decimal, ROUND_HALF_UP, ROUND_HALF_DOWN
from dateutil.parser import parse #osu
from youtube_basic import *
from os import environ
import nekos # https://github.com/Nekos-life/nekos.py/blob/master/nekos/nekos.py

token = environ.get('TOKEN')
osu_token = environ.get('OSU_API_KEY')

client = commands.Bot(command_prefix='!', case_insensitive=True)
client.remove_command('help')

# Get emote name & id: \:PainChamp:
# Animated emoji: <a:rikkaBongo:697839129257312286>
# Emote example: <:PainChamp:695437777763958874>
# Embed color: color = discord.Color(0x + hex)
# <@user_id> (or <@!user_id> if the member has a nickname.) 

# !help - help command
@client.command()
async def help(ctx):
    embed = discord.Embed(
        color = discord.Color.green(),
        timestamp = datetime.utcnow(),
        description = "`!help`\nWelp\n\n" \
            "`!hello`\nSup\n\n" \
            "`!all`\nMention @everyone\n\n" \
            "`!pat <member>`\nPat a member\n\n" \
            "`!poke <member>`\nPoke a member\n\n" \
            "`!kiss <member>`\nKiss a member\n\n" \
            "`!neko`\nNeko pic\n\n" \
            "`!baka <member>`\nBaka\n\n" \
            "`!hug <member>`\nHug a member\n\n" \
            "`!cuddle <member>`\nCuddle a member\n\n" \
            "`!random <min>, <max>`\nPick a random number from `min` to `max`\n\n" \
            "`!junior`\nJunior zuado\n\n" \
            "`!userinfo (optional member)`\nDisplay user info\n\n" \
            "`!avatar (optional member)`\nDisplay user's avatar\n\n" \
            "`!pfp (optional member)`\nDisplay user's pfp\n\n" \
            "`!dm <member> <message>`\nSend a DM to someone\n\n" \
            "`!rename <member> <new name>`\nChange user nickname\n\n" \
            "`!now`\nDisplay current datetime\n\n" \
            "`!osu <username/id>`\nDisplay osu player's info\n\n" \
            "`!top10 <username/id>`\nDisplay Top 10 Plays\n\n" \
            "`!mute <member> (optional reason)`\nMute a member\n\n" \
            "`!unmute <member>`\nUnmute a member\n\n" \
            "`!mutelist`\nDisplay mutelist\n\n" \
            "`!kick <member> <reason>`\nKick a member\n\n" \
            "`!ban <member> <reason>`\nBankai\n\n" \
            "`!unban <member/id>`\nUnban a member\n\n" \
            "`!banlist`\nDisplay banlist\n\n" \
            "`!yt <url>`\nPlay a song from YouTube\n\n" \
            "`!volume <int>`\nSet new volume\n\n" \
            "`!stop`\nStop song and disconnect bot from voice channel\n\n" \
            "`!man`\nLibrary functions - Linux man pages\n\n" \
    )

    # .split("?")[0] to avoid image resizing
    embed.set_author(name="Megumin's Commands", icon_url='{}'.format(client.user.avatar_url_as(format=None, static_format='png')).split("?")[0])
    embed.set_footer(icon_url='{}'.format(ctx.message.author.avatar_url_as(format=None, static_format='png')).split("?")[0], text="Gerado por {0}".format(ctx.message.author.name))
    embed.set_thumbnail(url='https://media1.tenor.com/images/52c7b756bf213ebee645f2a02c35de04/tenor.gif?itemid=16241381')
    await ctx.send(embed=embed)


# !avatar - display user's avatar 
@client.command()
async def avatar(ctx, member: discord.Member=None):
    # If member name is given
    if member != None:
        # if member is a bot
        if member.bot:
            show_avatar = discord.Embed(
                color = discord.Color.dark_blue(),
                title = 'Avatar de {0} (BOT)'.format(member.name),
                url = '{}'.format(member.avatar_url_as(format=None, static_format='png')).split("?")[0],
                timestamp = datetime.utcnow()
            )
        else:
            show_avatar = discord.Embed(
                color = discord.Color(0x0087FF),
                title = 'Avatar de {0}'.format(member.name),
                url = '{}'.format(member.avatar_url_as(format=None, static_format='png')).split("?")[0],
                timestamp = datetime.utcnow()
            )

        show_avatar.set_footer(icon_url='{}'.format(ctx.message.author.avatar_url_as(format=None, static_format='png')).split("?")[0], text="Gerado por {0}".format(ctx.message.author.name))
        show_avatar.set_image(url='{}'.format(member.avatar_url_as(format=None, static_format='png', size=4096)))
        await ctx.send(embed=show_avatar)
    # else member is himself
    else:
        show_avatar = discord.Embed(
            color = discord.Color.dark_blue(),
            title = 'Avatar de {0}'.format(ctx.message.author.name),
            url = '{}'.format(ctx.message.author.avatar_url_as(format=None, static_format='png')).split("?")[0],
            timestamp = datetime.utcnow()
        )

        show_avatar.set_footer(icon_url='{}'.format(ctx.message.author.avatar_url_as(format=None, static_format='png')).split("?")[0], text="Gerado por {0}".format(ctx.message.author.name))
        show_avatar.set_image(url='{}'.format(ctx.message.author.avatar_url_as(format=None, static_format='png', size=4096)))
        await ctx.send(embed=show_avatar)

# Checking if arguments are valid
@avatar.error
async def avatar_error(ctx, error):
    if isinstance(error, commands.BadArgument):
        embed = discord.Embed(
            color = discord.Color(0xff0000),
            timestamp = datetime.utcnow(),
            description = "**Mencione um membro do canal! <a:rikkaBongo:697839129257312286>**"
        )
        embed.set_footer(icon_url='{}'.format(ctx.message.author.avatar_url_as(format=None, static_format='png')).split("?")[0], text="Gerado por {0}".format(ctx.message.author.name))
        await ctx.send(embed=embed)


# !pfp - display user's pfp 
@client.command()
async def pfp(ctx, member: discord.Member=None):
    # If member name is given
    if member != None:
        # if member is a bot
        if member.bot:
            show_pfp = discord.Embed(
                color = discord.Color.dark_blue(),
                title = 'Avatar de {0} (BOT)'.format(member.name),
                url = '{}'.format(member.avatar_url_as(format=None, static_format='png')).split("?")[0],
                timestamp = datetime.utcnow()
            )
        else:
            show_pfp = discord.Embed(
                color = discord.Color(0x0087FF),
                title = 'Avatar de {0}'.format(member.name),
                url = '{}'.format(member.avatar_url_as(format=None, static_format='png')).split("?")[0],
                timestamp = datetime.utcnow()
            )

        show_pfp.set_footer(icon_url='{}'.format(ctx.message.author.avatar_url_as(format=None, static_format='png')).split("?")[0], text="Gerado por {0}".format(ctx.message.author.name))
        show_pfp.set_image(url='{}'.format(member.avatar_url_as(format=None, static_format='png', size=4096)))
        await ctx.send(embed=show_pfp)
    # else member is himself
    else:
        show_pfp = discord.Embed(
            color = discord.Color.dark_blue(),
            title = 'Avatar de {0}'.format(ctx.message.author.name),
            url = '{}'.format(ctx.message.author.avatar_url_as(format=None, static_format='png')).split("?")[0],
            timestamp = datetime.utcnow()
        )

        show_pfp.set_footer(icon_url='{}'.format(ctx.message.author.avatar_url_as(format=None, static_format='png')).split("?")[0], text="Gerado por {0}".format(ctx.message.author.name))
        show_pfp.set_image(url='{}'.format(ctx.message.author.avatar_url_as(format=None, static_format='png', size=4096)))
        await ctx.send(embed=show_pfp)

# Checking if arguments are valid
@pfp.error
async def pfp_error(ctx, error):
    if isinstance(error, commands.BadArgument):
        embed = discord.Embed(
            color = discord.Color(0xff0000),
            timestamp = datetime.utcnow(),
            description = "**Mencione um membro do canal! <a:rikkaBongo:697839129257312286>**"
        )
        embed.set_footer(icon_url='{}'.format(ctx.message.author.avatar_url_as(format=None, static_format='png')).split("?")[0], text="Gerado por {0}".format(ctx.message.author.name))
        await ctx.send(embed=embed)


# !dm - sends dm to mentioned person
@client.command()
async def dm(ctx, member: discord.Member = None, *, message = None):
    if member and message:
        channel = await member.create_dm()
        await channel.send(message)
    else:
        embed = discord.Embed(
            color = discord.Color(0xff0000),
            timestamp = datetime.utcnow(),
            description = "**Sintaxe incorreta! Use !dm <member> <message>**"
        )
        embed.set_footer(icon_url='{}'.format(ctx.message.author.avatar_url_as(format=None, static_format='png')).split("?")[0], text="Gerado por {0}".format(ctx.message.author.name))
        await ctx.send(embed=embed)

# Checking if arguments are valid
@dm.error
async def dm_error(ctx, error):
    if isinstance(error, commands.BadArgument):
        embed = discord.Embed(
            color = discord.Color(0xff0000),
            timestamp = datetime.utcnow(),
            description = "**Sintaxe incorreta! Use !dm <member> <message>**"
        )
        embed.set_footer(icon_url='{}'.format(ctx.message.author.avatar_url_as(format=None, static_format='png')).split("?")[0], text="Gerado por {0}".format(ctx.message.author.name))
        await ctx.send(embed=embed)
    elif isinstance(error, commands.MissingRequiredArgument):
        embed = discord.Embed(
            color = discord.Color(0xff0000),
            timestamp = datetime.utcnow(),
            description = "**Sintaxe incorreta! Use !dm <member> <message>**"
        )
        embed.set_footer(icon_url='{}'.format(ctx.message.author.avatar_url_as(format=None, static_format='png')).split("?")[0], text="Gerado por {0}".format(ctx.message.author.name))
        await ctx.send(embed=embed)


# !hello - hello
@client.command()
async def hello(ctx):
    await ctx.send("How ya doin {0.author.mention}".format(ctx))


# !random - random number between 1 and 1000
@client.command()
async def Random(ctx, *, numero = None):
    if numero and "," in numero and not numero.islower() and not re.compile('[@_!#$%^&*()<>?/\|}{~:.;+]').search(numero):
        n1 = numero.split(",")[0].strip()
        n2 = numero.split(",")[1].strip()
        n1 = int(n1)
        n2 = int(n2)
        if n1 <= n2:
            random_number = random.randint(n1, n2)
        else:
            random_number = random.randint(n2, n1)
        await ctx.send(random_number)
    else:
        embed = discord.Embed(
            color = discord.Color(0xff0000),
            description = "**Sintaxe incorreta! Use !random <min>, <max>**"
        )
        await ctx.send(embed=embed)

# Checking if arguments are valid
@Random.error
async def Random_error(ctx, error):
    if isinstance(error, commands.BadArgument):
        embed = discord.Embed(
            color = discord.Color(0xff0000),
            timestamp = datetime.utcnow(),
            description = "**Sintaxe incorreta! Use !random <min>, <max>**"
        )
        embed.set_footer(icon_url='{}'.format(ctx.message.author.avatar_url_as(format=None, static_format='png')).split("?")[0], text="Gerado por {0}".format(ctx.message.author.name))
        await ctx.send(embed=embed)
    elif isinstance(error, commands.MissingRequiredArgument):
        embed = discord.Embed(
            color = discord.Color(0xff0000),
            timestamp = datetime.utcnow(),
            description = "**Sintaxe incorreta! Use !random <min>, <max>**"
        )
        embed.set_footer(icon_url='{}'.format(ctx.message.author.avatar_url_as(format=None, static_format='png')).split("?")[0], text="Gerado por {0}".format(ctx.message.author.name))
        await ctx.send(embed=embed)


# !all - mention everyone
@client.command()
async def all(ctx):
    await ctx.send("@everyone")


# !junior - display junior's pic
@client.command()
async def junior(ctx):
    embed = discord.Embed(
        color = discord.Color.gold(),
        timestamp = datetime.utcnow(),
        title = ':face_vomiting:'
    )

    embed.set_image(url='https://image.prntscr.com/image/BemzF5RlTxa8Tdog35W5Aw.jpg')
    embed.set_footer(icon_url='{}'.format(ctx.message.author.avatar_url_as(format=None, static_format='png')).split("?")[0], text="Gerado por {0}".format(ctx.message.author.name))
    await ctx.send(embed=embed)


# !userinfo - display user's information
@client.command()
async def userinfo(ctx, member: discord.Member = None):
    # If member name is given
    if member:
        # If member is a bot
        if member.bot:
            embed = discord.Embed(
                color = discord.Color.greyple(),
                timestamp = datetime.utcnow(),
                title = "Informações de {0} (BOT)".format(member.name)
            )
        else:
            embed = discord.Embed(
                color = discord.Color(0x81E199),
                timestamp = datetime.utcnow(),
                title = "Informações de {0}".format(member.name)
            )
            
        # appending role name to list, ignoring first element (@everyone) / reversed() to reverse roles list
        role_list = [role.name for role in reversed(member.roles[1:])]
        # concatenating elements from role_list
        role_string = ', '.join(role_list)

        # formatting creation date (changing timezone)
        creation_date = member.created_at.replace(tzinfo=timezone('UTC')).astimezone(timezone('America/Sao_Paulo'))
        if creation_date.strftime("%Z")[1] == '0':
            if len(creation_date.strftime("%Z")) != 3:
                utc = creation_date.strftime("%Z")[0] + creation_date.strftime("%Z")[2] + ":" + creation_date.strftime("%Z")[3:]
                creation_date = creation_date.strftime("%a, %b %d %Y %X (UTC{})").format(utc)
            else:
                utc = creation_date.strftime("%Z")[0] + creation_date.strftime("%Z")[2:]
                creation_date = creation_date.strftime("%a, %b %d %Y %X (UTC{})").format(utc)
        elif creation_date.strftime("%Z").isalpha():
            creation_date = creation_date.strftime("%a, %b %d %Y %X %Z")
        elif creation_date.strftime("%Z")[1] != '0':
            if len(creation_date.strftime("%Z")) != 3:
                utc = creation_date.strftime("%Z")[:3] + ":" + creation_date.strftime("%Z")[3:]
                creation_date = creation_date.strftime("%a, %b %d %Y %X (UTC{})").format(utc)
            else:
                creation_date = creation_date.strftime("%a, %b %d %Y %X (UTC%Z)")
                
        # formatting join date (changing timezone)
        join_date = member.joined_at.replace(tzinfo=timezone('UTC')).astimezone(timezone('America/Sao_Paulo'))
        if join_date.strftime("%Z")[1] == '0':
            if len(join_date.strftime("%Z")) != 3:
                utc = join_date.strftime("%Z")[0] + join_date.strftime("%Z")[2] + ":" + join_date.strftime("%Z")[3:]
                join_date = join_date.strftime("%a, %b %d %Y %X (UTC{})").format(utc)
            else:
                utc = join_date.strftime("%Z")[0] + join_date.strftime("%Z")[2:]
                join_date = join_date.strftime("%a, %b %d %Y %X (UTC{})").format(utc)
        elif join_date.strftime("%Z").isalpha():
            join_date = join_date.strftime("%a, %b %d %Y %X %Z")
        elif join_date.strftime("%Z")[1] != '0':
            if len(join_date.strftime("%Z")) != 3:
                utc = join_date.strftime("%Z")[:3] + ":" + join_date.strftime("%Z")[3:]
                join_date = join_date.strftime("%a, %b %d %Y %X (UTC{})").format(utc)
            else:
                join_date = join_date.strftime("%a, %b %d %Y %X (UTC%Z)")
        
        # Embed fields
        embed.add_field(name="Nome", value="{0} ({1})".format(member, member.id), inline=False)
        embed.add_field(name="Apelido", value="{0}".format(member.name), inline=False)
        embed.add_field(name="Data da criação", value="{0}".format(creation_date), inline=False)
        embed.add_field(name="Entrada", value="{0}".format(join_date), inline=False)
        embed.add_field(name="Cargos", value="{0}".format(role_string), inline=False)
        embed.add_field(name="Avatar", value="{0}".format(member.avatar_url_as(format=None, static_format='png')).split("?")[0], inline=False)
        embed.set_footer(icon_url='{}'.format(ctx.message.author.avatar_url_as(format=None, static_format='png')).split("?")[0], text="Gerado por {0}".format(ctx.message.author.name))
        embed.set_thumbnail(url='{0}'.format(member.avatar_url_as(format=None, static_format='png')).split("?")[0])
        await ctx.send(embed=embed)
    # else member is himself
    else:
        embed = discord.Embed(
            color = discord.Color(0x81E199),
            timestamp = datetime.utcnow(),
            title = "Informações de {0}".format(ctx.message.author.name)
        )

        # appending role name to list, ignoring first element (@everyone)
        role_list = [role.name for role in reversed(ctx.message.author.roles[1:])]
        # concatenating elements from role_list
        role_string = ', '.join(role_list)

        # formatting creation date (changing timezone)
        creation_date = ctx.message.author.created_at.replace(tzinfo=timezone('UTC')).astimezone(timezone('America/Sao_Paulo'))
        if creation_date.strftime("%Z")[1] == '0':
            if len(creation_date.strftime("%Z")) != 3:
                utc = creation_date.strftime("%Z")[0] + creation_date.strftime("%Z")[2] + ":" + creation_date.strftime("%Z")[3:]
                creation_date = creation_date.strftime("%a, %b %d %Y %X (UTC{})").format(utc)
            else:
                utc = creation_date.strftime("%Z")[0] + creation_date.strftime("%Z")[2:]
                creation_date = creation_date.strftime("%a, %b %d %Y %X (UTC{})").format(utc)
        elif creation_date.strftime("%Z").isalpha():
            creation_date = creation_date.strftime("%a, %b %d %Y %X %Z")
        elif creation_date.strftime("%Z")[1] != '0':
            if len(creation_date.strftime("%Z")) != 3:
                utc = creation_date.strftime("%Z")[:3] + ":" + creation_date.strftime("%Z")[3:]
                creation_date = creation_date.strftime("%a, %b %d %Y %X (UTC{})").format(utc)
            else:
                creation_date = creation_date.strftime("%a, %b %d %Y %X (UTC%Z)")
                
        # formatting join date (changing timezone)
        join_date = ctx.message.author.joined_at.replace(tzinfo=timezone('UTC')).astimezone(timezone('America/Sao_Paulo'))
        if join_date.strftime("%Z")[1] == '0':
            if len(join_date.strftime("%Z")) != 3:
                utc = join_date.strftime("%Z")[0] + join_date.strftime("%Z")[2] + ":" + join_date.strftime("%Z")[3:]
                join_date = join_date.strftime("%a, %b %d %Y %X (UTC{})").format(utc)
            else:
                utc = join_date.strftime("%Z")[0] + join_date.strftime("%Z")[2:]
                join_date = join_date.strftime("%a, %b %d %Y %X (UTC{})").format(utc)
        elif join_date.strftime("%Z").isalpha():
            join_date = join_date.strftime("%a, %b %d %Y %X %Z")
        elif join_date.strftime("%Z")[1] != '0':
            if len(join_date.strftime("%Z")) != 3:
                utc = join_date.strftime("%Z")[:3] + ":" + join_date.strftime("%Z")[3:]
                join_date = join_date.strftime("%a, %b %d %Y %X (UTC{})").format(utc)
            else:
                join_date = join_date.strftime("%a, %b %d %Y %X (UTC%Z)")

        # Embed fields
        embed.add_field(name="Nome", value="{0} ({1})".format(ctx.message.author, ctx.message.author.id), inline=False)
        embed.add_field(name="Apelido", value="{0}".format(ctx.message.author.name), inline=False)
        # adjust timezone %Z & add discord creation date
        embed.add_field(name="Criação da conta", value="{0}".format(creation_date), inline=False)
        embed.add_field(name="Entrada", value="{0}".format(join_date), inline=False)
        embed.add_field(name="Cargos", value="{0}".format(role_string), inline=False)
        embed.add_field(name="Avatar", value="{0}".format(ctx.message.author.avatar_url_as(format=None, static_format='png')).split("?")[0], inline=False)
        embed.set_footer(icon_url='{}'.format(ctx.message.author.avatar_url_as(format=None, static_format='png')).split("?")[0], text="Gerado por {0}".format(ctx.message.author.name))
        embed.set_thumbnail(url='{0}'.format(ctx.message.author.avatar_url_as(format=None, static_format='png')).split("?")[0])
        await ctx.send(embed=embed)

# Checking if arguments are valid
@userinfo.error
async def userinfo_error(ctx, error):
    if isinstance(error, commands.BadArgument):
        embed = discord.Embed(
            color = discord.Color(0xff0000),
            timestamp = datetime.utcnow(),
            description = "**Mencione um membro do canal! <a:rikkaBongo:697839129257312286>**"
        )
        embed.set_footer(icon_url='{}'.format(ctx.message.author.avatar_url_as(format=None, static_format='png')).split("?")[0], text="Gerado por {0}".format(ctx.message.author.name))
        await ctx.send(embed=embed)


# !rename - change user's nick
@client.command()
@commands.has_permissions(administrator=True)
async def rename(ctx, member: discord.Member = None, *, new_name = None):
    if member and new_name:
        # hierarchy checking
        if member.top_role >= ctx.author.top_role:
            embed = discord.Embed(
                color = discord.Color(0xff0000),
                timestamp = datetime.utcnow(),
                description = "**Você apenas consegue renomear o nickname de membros com cargo inferior ao seu!**"
            )
            embed.set_footer(icon_url='{}'.format(ctx.message.author.avatar_url_as(format=None, static_format='png')).split("?")[0], text="Gerado por {0}".format(ctx.message.author.name))
            await ctx.send(embed=embed)
        else:
            old_nick = member.nick
            new_nick = "<@!{}>".format(member.id)
            await member.edit(nick=new_name)

            embed = discord.Embed(
                color = discord.Color(0x5cb85c),
                timestamp = datetime.utcnow()
            )

            embed.set_author(name="Nick de {} alterado".format(member), icon_url='{}'.format(member.avatar_url_as(format=None, static_format='png')).split("?")[0])
            if old_nick != None:
                embed.add_field(name="Nickname antigo", value="**`{}`**".format(old_nick), inline=False)
            # If user doesnt have a nick
            else:
                embed.add_field(name="Nickname antigo", value="**`{}`**".format(member.name), inline=False)
            embed.add_field(name="Nickname novo", value="**{}**".format(new_nick), inline=False)
            embed.set_footer(icon_url='{}'.format(ctx.message.author.avatar_url_as(format=None, static_format='png')).split("?")[0], text="Alterado por {0}".format(ctx.message.author.name))
            embed.set_thumbnail(url='{0}'.format(member.avatar_url_as(format=None, static_format='png')).split("?")[0])
            await ctx.send(embed=embed)
    else:
        embed = discord.Embed(
            color = discord.Color(0xff0000),
            timestamp = datetime.utcnow(),
            description = "**Sintaxe incorreta! Use !rename <member> <new nickname>**"
        )
        embed.set_footer(icon_url='{}'.format(ctx.message.author.avatar_url_as(format=None, static_format='png')).split("?")[0], text="Gerado por {0}".format(ctx.message.author.name))
        await ctx.send(embed=embed)

# Checking if an user has permission to use this command/if arguments are valid
@rename.error
async def rename_error(ctx, error):
    if isinstance(error, commands.MissingPermissions):
        embed = discord.Embed(
            color = discord.Color(0xff0000),
            timestamp = datetime.utcnow(),
            description = "**Você não possui permissão para alterar nicknames!**"
        )
        embed.set_footer(icon_url='{}'.format(ctx.message.author.avatar_url_as(format=None, static_format='png')).split("?")[0], text="Gerado por {0}".format(ctx.message.author.name))
        await ctx.send(embed=embed)
    elif isinstance(error, commands.BadArgument):
        embed = discord.Embed(
            color = discord.Color(0xff0000),
            timestamp = datetime.utcnow(),
            description = "**Mencione um membro do canal e seu nickname novo! <a:rikkaBongo:697839129257312286>**"
        )
        embed.set_footer(icon_url='{}'.format(ctx.message.author.avatar_url_as(format=None, static_format='png')).split("?")[0], text="Gerado por {0}".format(ctx.message.author.name))
        await ctx.send(embed=embed)
    elif isinstance(error, commands.MissingRequiredArgument):
        embed = discord.Embed(
            color = discord.Color(0xff0000),
            timestamp = datetime.utcnow(),
            description = "**Sintaxe incorreta! Use !rename <member> <new nickname>**"
        )
        embed.set_footer(icon_url='{}'.format(ctx.message.author.avatar_url_as(format=None, static_format='png')).split("?")[0], text="Gerado por {0}".format(ctx.message.author.name))
        await ctx.send(embed=embed)


# !now - now
@client.command()
async def now(ctx):
    """ Auto detect timezone (working example 1) datetime.timezone """
    # local_now = datetime.now(timezone.utc).astimezone()
    # await ctx.send(local_now.strftime("%a, %b %d %Y %X %Z"))
    """ Working example 2 (EST gmt -5) timezone.pytz """
    # now_utc = datetime.now(timezone('UTC')).astimezone(timezone('EST'))
    # await ctx.send(now_utc.strftime("%a, %b %d %Y %X %Z"))

    # utc verification and stuff, you can change America/Sao_Paulo to another timezone See: https://gist.github.com/heyalexej/8bf688fd67d7199be4a1682b3eec7568
    local_now = datetime.now(timezone('UTC')).astimezone(timezone('America/Sao_Paulo'))
    if local_now.strftime("%Z")[1] == '0':
        if len(local_now.strftime("%Z")) != 3:
            utc = local_now.strftime("%Z")[0] + local_now.strftime("%Z")[2] + ":" + local_now.strftime("%Z")[3:]
            await ctx.send(local_now.strftime("Today is %d/%m/%Y (%A), **%X (UTC{})**").format(utc))
        else:
            utc = local_now.strftime("%Z")[0] + local_now.strftime("%Z")[2:]
            await ctx.send(local_now.strftime("Today is %d/%m/%Y (%A), **%X (UTC{})**").format(utc))
    elif local_now.strftime("%Z").isalpha():
        await ctx.send(local_now.strftime("Today is %d/%m/%Y (%A), **%X %Z**"))
    elif local_now.strftime("%Z")[1] != '0':
        if len(local_now.strftime("%Z")) != 3:
            utc = local_now.strftime("%Z")[:3] + ":" + local_now.strftime("%Z")[3:]
            await ctx.send(local_now.strftime("Today is %d/%m/%Y (%A), **%X (UTC{})**").format(utc))
        else:
            await ctx.send(local_now.strftime("Today is %d/%m/%Y (%A), **%X (UTC%Z)**"))


# !mute - mute members
@client.command()
@commands.has_permissions(administrator=True)
async def mute(ctx, member: discord.Member = None, *, reason=None):
    if member != None:
        # user's role list
        user_roles = []
        for role in member.roles:
            # appending role name to list
            user_roles.append(role.name)

        # checks if user_roles not contains Boruto role
        if "Boruto" not in user_roles:
            # Checking if there is role named Boruto and channel named hueco_mundo
            role_muted = discord.utils.get(ctx.guild.roles, name="Boruto")
            hueco_mundo = discord.utils.get(ctx.guild.text_channels, name="hueco_mundo")
            category = discord.utils.get(ctx.guild.categories, name='main')

            # Checks if there is a role named Boruto
            if not role_muted:
                # creating new role named Boruto
                role_muted = await ctx.guild.create_role(name="Boruto", reason="To use for muting", colour=discord.Colour(0x4A4A4A))
                for channel in ctx.guild.channels:
                    # settings
                    await channel.set_permissions(role_muted, send_messages=False)
                await member.add_roles(role_muted)
            else:
                await member.add_roles(role_muted)

            # Checks if there is a channel named hueco_mundo
            if not hueco_mundo:
                # permissions
                overwrites = {ctx.guild.default_role: discord.PermissionOverwrite(send_messages=False),
                            ctx.guild.me: discord.PermissionOverwrite(send_messages=True),
                            role_muted: discord.PermissionOverwrite(send_messages=True)}
                # creating channel named hueco_mundo
                channel = await ctx.message.guild.create_text_channel('hueco_mundo', overwrites=overwrites, category=category, topic="Bankai")
                await channel.send("Welcome to Hueco Mundo, <@{}>".format(member.id))

            # default reason
            if reason == None:
                reason = "<:SillyChamp:695437918625595542>"
            
            embed = discord.Embed(
                color = discord.Color(0xE53A5E),
                timestamp = datetime.utcnow(),
                description = "<@{}> foi mutado!\n**Motivo:** {}".format(member.id, reason)
            )
            embed.set_author(name="{} mutado!".format(member.name), icon_url='{}'.format(member.avatar_url_as(format=None, static_format='png')).split("?")[0])
            embed.set_thumbnail(url='{}'.format(member.avatar_url_as(format=None, static_format='png')).split("?")[0])
            embed.set_footer(icon_url='{}'.format(ctx.message.author.avatar_url_as(format=None, static_format='png')).split("?")[0], text="Mutado por {0}".format(ctx.message.author.name))
            await ctx.send(embed=embed)
        else:
            embed = discord.Embed(
                color = discord.Color(0xE53A5E),
                timestamp = datetime.utcnow(),
                description = "<@{}> já está mutado!".format(member.id)
            )
            embed.set_author(name="{}".format(member), icon_url='{}'.format(member.avatar_url_as(format=None, static_format='png')).split("?")[0])
            embed.set_thumbnail(url='{}'.format(member.avatar_url_as(format=None, static_format='png')).split("?")[0])
            embed.set_footer(icon_url='{}'.format(ctx.message.author.avatar_url_as(format=None, static_format='png')).split("?")[0], text="Gerado por {0}".format(ctx.message.author.name))
            await ctx.send(embed=embed)
    else:
        embed = discord.Embed(
            color = discord.Color(0xff0000),
            timestamp = datetime.utcnow(),
            description = "**Preciso de um usuário pra mutar! <a:rikkaBongo:697839129257312286>**"
        )
        embed.set_footer(icon_url='{}'.format(ctx.message.author.avatar_url_as(format=None, static_format='png')).split("?")[0], text="Gerado por {0}".format(ctx.message.author.name))
        await ctx.send(embed=embed)

# Checking if arguments are valid
@mute.error
async def mute_error(ctx, error):
    if isinstance(error, commands.MissingPermissions):
        embed = discord.Embed(
            color = discord.Color(0xff0000),
            timestamp = datetime.utcnow(),
            description = "**Você não possui permissão para mutar!**"
        )
        embed.set_footer(icon_url='{}'.format(ctx.message.author.avatar_url_as(format=None, static_format='png')).split("?")[0], text="Gerado por {0}".format(ctx.message.author.name))
        await ctx.send(embed=embed)
    elif isinstance(error, commands.BadArgument):
        embed = discord.Embed(
            color = discord.Color(0xff0000),
            timestamp = datetime.utcnow(),
            description = "**Mencione um membro do canal! <a:rikkaBongo:697839129257312286>**"
        )
        embed.set_footer(icon_url='{}'.format(ctx.message.author.avatar_url_as(format=None, static_format='png')).split("?")[0], text="Gerado por {0}".format(ctx.message.author.name))
        await ctx.send(embed=embed)


# !unmute - unmute members
@client.command()
@commands.has_permissions(administrator=True)
async def unmute(ctx, member: discord.Member = None):
    if member != None:
        # user's role list
        user_roles = []
        for role in member.roles:
            # appending role name to list
            user_roles.append(role.name)

        # checks if user_roles not contains Boruto role
        if "Boruto" in user_roles:
            # removing Boruto role from member
            await member.remove_roles(discord.utils.get(ctx.guild.roles, name="Boruto"))
            embed = discord.Embed(
                color = discord.Color(0x63DBC2),
                timestamp = datetime.utcnow(),
                description = "<@{}> foi desmutado!".format(member.id)
            )
            embed.set_author(name="{} desmutado!".format(member.name), icon_url='{}'.format(member.avatar_url_as(format=None, static_format='png')).split("?")[0])
            embed.set_thumbnail(url='{}'.format(member.avatar_url_as(format=None, static_format='png')).split("?")[0])
            embed.set_footer(icon_url='{}'.format(ctx.message.author.avatar_url_as(format=None, static_format='png')).split("?")[0], text="Desmutado por {0}".format(ctx.message.author.name))
            await ctx.send(embed=embed)
        else:
            embed = discord.Embed(
                color = discord.Color(0x63DBC2),
                timestamp = datetime.utcnow(),
                description = "<@{}> não está mutado!".format(member.id)
            )
            embed.set_author(name="{}".format(member), icon_url='{}'.format(member.avatar_url_as(format=None, static_format='png')).split("?")[0])
            embed.set_thumbnail(url='{}'.format(member.avatar_url_as(format=None, static_format='png')).split("?")[0])
            embed.set_footer(icon_url='{}'.format(ctx.message.author.avatar_url_as(format=None, static_format='png')).split("?")[0], text="Gerado por {0}".format(ctx.message.author.name))
            await ctx.send(embed=embed)
    else:
        embed = discord.Embed(
            color = discord.Color(0xff0000),
            timestamp = datetime.utcnow(),
            description = "**Preciso de um usuário pra desmutar! <a:rikkaBongo:697839129257312286>**"
        )
        embed.set_footer(icon_url='{}'.format(ctx.message.author.avatar_url_as(format=None, static_format='png')).split("?")[0], text="Gerado por {0}".format(ctx.message.author.name))
        await ctx.send(embed=embed)

# Checking if arguments are valid
@unmute.error
async def unmute_error(ctx, error):
    if isinstance(error, commands.MissingPermissions):
        embed = discord.Embed(
            color = discord.Color(0xff0000),
            timestamp = datetime.utcnow(),
            description = "**Você não possui permissão para desmutar!**"
        )
        embed.set_footer(icon_url='{}'.format(ctx.message.author.avatar_url_as(format=None, static_format='png')).split("?")[0], text="Gerado por {0}".format(ctx.message.author.name))
        await ctx.send(embed=embed)
    elif isinstance(error, commands.BadArgument):
        embed = discord.Embed(
            color = discord.Color(0xff0000),
            timestamp = datetime.utcnow(),
            description = "**Mencione um membro do canal! <a:rikkaBongo:697839129257312286>**"
        )
        embed.set_footer(icon_url='{}'.format(ctx.message.author.avatar_url_as(format=None, static_format='png')).split("?")[0], text="Gerado por {0}".format(ctx.message.author.name))
        await ctx.send(embed=embed)


# !mutelist - displays mutelist
@client.command()
@commands.has_permissions(administrator=True)
async def mutelist(ctx):
    embed = discord.Embed(
        color = discord.Color(0xEBCF02),
        timestamp = datetime.utcnow(),
        title = "Usuários Mutados"
    )
    embed.set_thumbnail(url='https://image.prntscr.com/image/W1Lamz1dRbS2Uzhd5CkUtw.gif')
    embed.set_footer(icon_url='{}'.format(ctx.message.author.avatar_url_as(format=None, static_format='png')).split("?")[0], text="Gerado por {0}".format(ctx.message.author.name))
    for member in ctx.guild.members:
        for role in member.roles:
            if role.name == "Boruto":
                embed.add_field(name="{}".format(member), value="<@{}>".format(member.id), inline=False)
    await ctx.send(embed=embed)

# Checking if arguments are valid
@mutelist.error
async def mutelist_error(ctx, error):
    if isinstance(error, commands.MissingPermissions):
        embed = discord.Embed(
            color = discord.Color(0xff0000),
            timestamp = datetime.utcnow(),
            description = "**Você não possui permissão para acessar a Lista de Mutados!**"
        )
        embed.set_footer(icon_url='{}'.format(ctx.message.author.avatar_url_as(format=None, static_format='png')).split("?")[0], text="Gerado por {0}".format(ctx.message.author.name))
        await ctx.send(embed=embed)


# !kick - kick users
@client.command()
@commands.has_permissions(administrator=True)
async def kick(ctx, member: discord.Member = None, *, reason=None):
    if member != None:
        if member == ctx.message.author:
            embed = discord.Embed(
                color = discord.Color(0xff0000),
                timestamp = datetime.utcnow(),
                description = "**Você não pode se expulsar!**"
            )
            embed.set_footer(icon_url='{}'.format(ctx.message.author.avatar_url_as(format=None, static_format='png')).split("?")[0], text="Gerado por {0}".format(ctx.message.author.name))
            await ctx.send(embed=embed)
        else:
            # hierarchy checking
            if member.top_role >= ctx.author.top_role:
                embed = discord.Embed(
                    color = discord.Color(0xff0000),
                    timestamp = datetime.utcnow(),
                    description = "**Você apenas consegue expulsar membros com cargo inferior ao seu!**"
                )
                embed.set_footer(icon_url='{}'.format(ctx.message.author.avatar_url_as(format=None, static_format='png')).split("?")[0], text="Gerado por {0}".format(ctx.message.author.name))
                await ctx.send(embed=embed)
            else:
                # default reason
                if reason == None:
                    reason = "<:PepegaChair:695437797552816210>"
                embed = discord.Embed(
                    color = discord.Color(0xFF5C0B),
                    timestamp = datetime.utcnow(),
                    description = "**Motivo:** {}".format(reason)
                )
                embed.set_author(name="RIP {}!".format(member.name), icon_url='{}'.format(member.avatar_url_as(format=None, static_format='png')).split("?")[0])
                embed.set_footer(icon_url='{}'.format(ctx.message.author.avatar_url_as(format=None, static_format='png')).split("?")[0], text="Expulso por {0}".format(ctx.message.author.name))
                await ctx.send(embed=embed)

                # Sending a dm to kicked user
                channel = await member.create_dm()
                await channel.send(embed=embed)
                await member.kick(reason = reason)
    else:
        embed = discord.Embed(
            color = discord.Color(0xff0000),
            timestamp = datetime.utcnow(),
            description = "**Preciso de um usuário pra expulsar! <a:rikkaBongo:697839129257312286>**"
        )
        embed.set_footer(icon_url='{}'.format(ctx.message.author.avatar_url_as(format=None, static_format='png')).split("?")[0], text="Gerado por {0}".format(ctx.message.author.name))
        await ctx.send(embed=embed)

# Checking if arguments are valid
@kick.error
async def kick_error(ctx, error):
    if isinstance(error, commands.MissingPermissions):
        embed = discord.Embed(
            color = discord.Color(0xff0000),
            timestamp = datetime.utcnow(),
            description = "**Você não possui permissão para expulsar!**"
        )
        embed.set_footer(icon_url='{}'.format(ctx.message.author.avatar_url_as(format=None, static_format='png')).split("?")[0], text="Gerado por {0}".format(ctx.message.author.name))
        await ctx.send(embed=embed)
    elif isinstance(error, commands.BadArgument):
        embed = discord.Embed(
            color = discord.Color(0xff0000),
            timestamp = datetime.utcnow(),
            description = "**Mencione um membro do canal! <a:rikkaBongo:697839129257312286>**"
        )
        embed.set_footer(icon_url='{}'.format(ctx.message.author.avatar_url_as(format=None, static_format='png')).split("?")[0], text="Gerado por {0}".format(ctx.message.author.name))
        await ctx.send(embed=embed)


# !ban - ban a member
@client.command()
@commands.has_permissions(administrator=True)
async def ban(ctx, member: discord.Member = None, *, reason=None):
    if member != None:
        if member == ctx.message.author:
            embed = discord.Embed(
                color = discord.Color(0xff0000),
                timestamp = datetime.utcnow(),
                description = "**Você não pode banir a si mesmo!**"
            )
            embed.set_footer(icon_url='{}'.format(ctx.message.author.avatar_url_as(format=None, static_format='png')).split("?")[0], text="Gerado por {0}".format(ctx.message.author.name))
            await ctx.send(embed=embed)
        else:
            # hierarchy checking
            if member.top_role >= ctx.author.top_role:
                embed = discord.Embed(
                    color = discord.Color(0xff0000),
                    timestamp = datetime.utcnow(),
                    description = "**Você apenas consegue banir membros com cargo inferior ao seu!**"
                )
                embed.set_footer(icon_url='{}'.format(ctx.message.author.avatar_url_as(format=None, static_format='png')).split("?")[0], text="Gerado por {0}".format(ctx.message.author.name))
                await ctx.send(embed=embed)
            else:
                if reason == None:
                    reason = "Você é <:Pepega:695434151230177330>!"
                embed = discord.Embed(
                    color = discord.Color(0xE52913),
                    timestamp = datetime.utcnow(),
                    description = "**Motivo:** {}".format(reason)
                )
                embed.set_author(name="RIP {}!".format(member.name), icon_url='{}'.format(member.avatar_url_as(format=None, static_format='png')).split("?")[0])
                embed.set_footer(icon_url='{}'.format(ctx.message.author.avatar_url_as(format=None, static_format='png')).split("?")[0], text="Banido por {0}".format(ctx.message.author.name))
                await ctx.send(embed=embed)

                # Sending a dm to banned user
                channel = await member.create_dm()
                await channel.send(embed=embed)
                await member.ban(reason = reason, delete_message_days = 1)                
    else:
        embed = discord.Embed(
            color = discord.Color(0xff0000),
            timestamp = datetime.utcnow(),
            description = "**Preciso de um usuário pra banir! <a:rikkaBongo:697839129257312286>**"
        )
        embed.set_footer(icon_url='{}'.format(ctx.message.author.avatar_url_as(format=None, static_format='png')).split("?")[0], text="Gerado por {0}".format(ctx.message.author.name))
        await ctx.send(embed=embed)

# Checking if arguments are valid
@ban.error
async def ban_error(ctx, error):
    if isinstance(error, commands.MissingPermissions):
        embed = discord.Embed(
            color = discord.Color(0xff0000),
            timestamp = datetime.utcnow(),
            description = "**Você não possui permissão para banir!**"
        )
        embed.set_footer(icon_url='{}'.format(ctx.message.author.avatar_url_as(format=None, static_format='png')).split("?")[0], text="Gerado por {0}".format(ctx.message.author.name))
        await ctx.send(embed=embed)
    elif isinstance(error, commands.BadArgument):
        embed = discord.Embed(
            color = discord.Color(0xff0000),
            timestamp = datetime.utcnow(),
            description = "**Mencione um membro do canal! <a:rikkaBongo:697839129257312286>**"
        )
        embed.set_footer(icon_url='{}'.format(ctx.message.author.avatar_url_as(format=None, static_format='png')).split("?")[0], text="Gerado por {0}".format(ctx.message.author.name))
        await ctx.send(embed=embed)


# !unban - unban a member
@client.command()
@commands.has_permissions(administrator=True)
async def unban(ctx, *, member=None):
    if member != None:
        contador = 0
        banned_users = await ctx.guild.bans()
        if "#" in member:
            member_name, member_discriminator = member.split('#')
            member_id = 0
        elif member.isdecimal():
            member_name, member_discriminator = "a", "0"
            member_id = int(member)
        else:
            embed = discord.Embed(
                color = discord.Color(0xff0000),
                timestamp = datetime.utcnow(),
                description = "**Sintaxe incorreta! Use !unban <name@discriminator/id>**"
            )
            embed.set_footer(icon_url='{}'.format(ctx.message.author.avatar_url_as(format=None, static_format='png')).split("?")[0], text="Gerado por {0}".format(ctx.message.author.name))
            await ctx.send(embed=embed)

        for ban_entry in banned_users:
            user = ban_entry.user
            if (user.name, user.discriminator) == (member_name, member_discriminator):
                await ctx.guild.unban(user)
                embed = discord.Embed(
                    color = discord.Color(0x1FD358),
                    timestamp = datetime.utcnow(),
                    description = "<@{}> foi desbanido!".format(user.id)
                )
                embed.set_footer(icon_url='{}'.format(ctx.message.author.avatar_url_as(format=None, static_format='png')).split("?")[0], text="Desbanido por {0}".format(ctx.message.author.name))
                await ctx.send(embed=embed)
                contador += 1
            elif user.id == member_id:
                await ctx.guild.unban(user)
                embed = discord.Embed(
                    color = discord.Color(0x1FD358),
                    timestamp = datetime.utcnow(),
                    description = "<@{}> foi desbanido!".format(user.id)
                )
                embed.set_footer(icon_url='{}'.format(ctx.message.author.avatar_url_as(format=None, static_format='png')).split("?")[0], text="Desbanido por {0}".format(ctx.message.author.name))
                await ctx.send(embed=embed)
                contador += 1
        else:
            if contador == 0:
                embed = discord.Embed(
                    color = discord.Color(0xff0000),
                    timestamp = datetime.utcnow(),
                    description = "**Usuário não existe ou não está na lista de banimentos!**"
                )
                embed.set_footer(icon_url='{}'.format(ctx.message.author.avatar_url_as(format=None, static_format='png')).split("?")[0], text="Gerado por {0}".format(ctx.message.author.name))
                await ctx.send(embed=embed)
    else:
        embed = discord.Embed(
            color = discord.Color(0xff0000),
            timestamp = datetime.utcnow(),
            description = "**Preciso de um usuário pra desbanir! <a:rikkaBongo:697839129257312286>**"
        )
        embed.set_footer(icon_url='{}'.format(ctx.message.author.avatar_url_as(format=None, static_format='png')).split("?")[0], text="Gerado por {0}".format(ctx.message.author.name))
        await ctx.send(embed=embed)

# Checking if arguments are valid
@unban.error
async def unban_error(ctx, error):
    if isinstance(error, commands.MissingPermissions):
        embed = discord.Embed(
            color = discord.Color(0xff0000),
            timestamp = datetime.utcnow(),
            description = "**Você não possui permissão para desbanir!**"
        )
        embed.set_footer(icon_url='{}'.format(ctx.message.author.avatar_url_as(format=None, static_format='png')).split("?")[0], text="Gerado por {0}".format(ctx.message.author.name))
        await ctx.send(embed=embed)
    elif isinstance(error, commands.BadArgument):
        embed = discord.Embed(
            color = discord.Color(0xff0000),
            timestamp = datetime.utcnow(),
            description = "**Sintaxe incorreta! Use !unban <member/id>**"
        )
        embed.set_footer(icon_url='{}'.format(ctx.message.author.avatar_url_as(format=None, static_format='png')).split("?")[0], text="Gerado por {0}".format(ctx.message.author.name))
        await ctx.send(embed=embed)


# !banlist - displays banlist
@client.command()
@commands.has_permissions(administrator=True)
async def banlist(ctx):
    banned_users = await ctx.guild.bans()

    embed = discord.Embed(
        color = discord.Color(0xD65F27),
        timestamp = datetime.utcnow(),
        title = "Usuários Banidos"
    )
    embed.set_thumbnail(url='https://media1.tenor.com/images/f6425d74284e9784e62fd581c29124e9/tenor.gif?itemid=13329275')
    embed.set_footer(icon_url='{}'.format(ctx.message.author.avatar_url_as(format=None, static_format='png')).split("?")[0], text="Gerado por {0}".format(ctx.message.author.name))
    for ban_entry in banned_users:
        user = ban_entry.user
        reason = ban_entry.reason
        if reason == None:
            reason = "Sem motivo informado"
        embed.add_field(name="{} ({})".format(user, user.id), value="**Motivo: **{}".format(reason), inline=False)
    await ctx.send(embed=embed)

# Checking if arguments are valid
@banlist.error
async def banlist_error(ctx, error):
    if isinstance(error, commands.MissingPermissions):
        embed = discord.Embed(
            color = discord.Color(0xff0000),
            timestamp = datetime.utcnow(),
            description = "**Você não possui permissão para acessar a Lista de Banidos!**"
        )
        embed.set_footer(icon_url='{}'.format(ctx.message.author.avatar_url_as(format=None, static_format='png')).split("?")[0], text="Gerado por {0}".format(ctx.message.author.name))
        await ctx.send(embed=embed)


# Osu - displays player's info
@client.command(pass_context=True)
async def osu(ctx, *, username=None):
    r_user = requests.get("https://osu.ppy.sh/api/get_user?u={}&k={}".format(username, osu_token))
    json_user = r_user.json()

    # Checking if username is given and user exists
    if username != None and json_user:
        json_user = r_user.json()[0]
        # avatar verification
        avatar_verification = requests.get('https://a.ppy.sh/{}'.format(json_user['user_id']))
        if avatar_verification.status_code == 404:
            avatar = 'http://s.ppy.sh/a/'
        else:
            avatar = 'http://s.ppy.sh/a/{}'.format(json_user["user_id"])

        # pp verification
        if float(json_user["pp_raw"]) - math.floor(float(json_user["pp_raw"])) < 0.5:
            pp = math.floor(float(json_user["pp_raw"]))
        else:
            pp = math.ceil(float(json_user["pp_raw"]))

        # Accuracy verification
        acc = Decimal(str(json_user["accuracy"])).quantize(Decimal('0.00'), rounding=ROUND_HALF_UP)

        # Country's flag
        flag_emoji = ":flag_" + json_user["country"].lower() + ":"

        # Converting seconds to days, hour, minutes and seconds
        min, sec = divmod(int(json_user["total_seconds_played"]), 60) 
        hour, min = divmod(min, 60)
        days, hour = divmod(hour, 24)
        if days != 0:
            total_played = "{}d {}h {}m {}s".format(days, hour, min, sec)
        else:
            total_played = "{}h {}m {}s".format(hour, min, sec)

        # formatting account creation date (changing timezone)
        datetime_join_date = parse(json_user["join_date"])
        creation_date = datetime_join_date.replace(tzinfo=timezone('UTC')).astimezone(timezone('America/Sao_Paulo'))
        if creation_date.strftime("%Z")[1] == '0':
            if len(creation_date.strftime("%Z")) != 3:
                utc = creation_date.strftime("%Z")[0] + creation_date.strftime("%Z")[2] + ":" + creation_date.strftime("%Z")[3:]
                creation_date = creation_date.strftime("%a, %b %d %Y %X (UTC{})").format(utc)
            else:
                utc = creation_date.strftime("%Z")[0] + creation_date.strftime("%Z")[2:]
                creation_date = creation_date.strftime("%a, %b %d %Y %X (UTC{})").format(utc)
        elif creation_date.strftime("%Z").isalpha():
            creation_date = creation_date.strftime("%a, %b %d %Y %X %Z")
        elif creation_date.strftime("%Z")[1] != '0':
            if len(creation_date.strftime("%Z")) != 3:
                utc = creation_date.strftime("%Z")[:3] + ":" + creation_date.strftime("%Z")[3:]
                creation_date = creation_date.strftime("%a, %b %d %Y %X (UTC{})").format(utc)
            else:
                creation_date = creation_date.strftime("%a, %b %d %Y %X (UTC%Z)")

        embed = discord.Embed(
            color = discord.Color(0xe969a2),
            timestamp = datetime.utcnow(),
            title = "Perfil de {}".format(json_user["username"]),
            url = "https://osu.ppy.sh/users/{}".format(json_user["user_id"])
        )
        # embed.set_author(name="Perfil de {}".format(json_user["username"]), url="https://osu.ppy.sh/users/{}".format(json_user["user_id"]), icon_url='http://s.ppy.sh/a/{}'.format(json_user["user_id"]))
        embed.add_field(name="Nickname", value="{} (#{})".format(json_user["username"], json_user["user_id"]), inline=False)
        # Verifying if user has rank
        if int(json_user["pp_rank"]) == 0:
            embed.add_field(name="Rank", value="{} (#{:,} {})".format("—", int(json_user["pp_country_rank"]), flag_emoji), inline=False)
        else:
            embed.add_field(name="Rank", value="#{:,} (#{:,} {})".format(int(json_user["pp_rank"]), int(json_user["pp_country_rank"]), flag_emoji), inline=False)
        embed.add_field(name="Level", value="{}".format(math.floor(float(json_user["level"]))), inline=False)
        embed.add_field(name="Join Date", value="{}".format(creation_date), inline=False)
        embed.add_field(name="Total Play Time", value="{}".format(total_played), inline=False)
        embed.add_field(name="pp", value="{:,}".format(int(pp)), inline=False)
        embed.add_field(name="Accuracy", value="{}%".format(acc), inline=False)
        embed.add_field(name="Play Count", value="{:,}".format(int(json_user["playcount"])), inline=False)
        embed.set_thumbnail(url=avatar)
        embed.set_footer(icon_url='{}'.format(ctx.message.author.avatar_url_as(format=None, static_format='png')).split("?")[0], text="Gerado por {0}".format(ctx.message.author.name))
        message = await ctx.send(embed=embed)
        await message.add_reaction('<:PogChampion:706621494477717565>')
        # await ctx.send(r.json_user())
    # Username is incorrect or is not given
    else:
        if username == None:
            embed = discord.Embed(
                color = discord.Color(0xff0000),
                timestamp = datetime.utcnow(),
                description = "**Nome do usuário não fornecido! <a:rikkaBongo:697839129257312286> Use !osu <username/id>**"
            )
            embed.set_footer(icon_url='{}'.format(ctx.message.author.avatar_url_as(format=None, static_format='png')).split("?")[0], text="Gerado por {0}".format(ctx.message.author.name))
            await ctx.send(embed=embed)
        elif not json_user:
            embed = discord.Embed(
                color = discord.Color(0xff0000),
                timestamp = datetime.utcnow(),
                description = "**Usuário não existe! <a:rikkaBongo:697839129257312286>**"
            )
            embed.set_footer(icon_url='{}'.format(ctx.message.author.avatar_url_as(format=None, static_format='png')).split("?")[0], text="Gerado por {0}".format(ctx.message.author.name))
            await ctx.send(embed=embed)

# Checking if arguments are valid
@osu.error
async def osu_error(ctx, error):
    if isinstance(error, commands.BadArgument):
        embed = discord.Embed(
            color = discord.Color(0xff0000),
            timestamp = datetime.utcnow(),
            description = "**Sintaxe incorreta! Use !osu <member/id>**"
        )
        embed.set_footer(icon_url='{}'.format(ctx.message.author.avatar_url_as(format=None, static_format='png')).split("?")[0], text="Gerado por {0}".format(ctx.message.author.name))
        await ctx.send(embed=embed)


# !top10 - Osu user's top 10 plays
@client.command()
async def top10(ctx, *, username=None):
    r_user = requests.get("https://osu.ppy.sh/api/get_user?u={}&k={}".format(username, osu_token))
    json_user = r_user.json()
    r_scores = requests.get("https://osu.ppy.sh/api/get_user_best?u={}&k={}".format(username, osu_token))
    json_scores = r_scores.json()

    # Checking if username is given and user exists
    if username != None and json_user:
        json_user = r_user.json()[0]
        # avatar verification
        avatar_verification = requests.get('https://a.ppy.sh/{}'.format(json_user['user_id']))
        if avatar_verification.status_code == 404:
            avatar = 'http://s.ppy.sh/a/'
        else:
            avatar = 'http://s.ppy.sh/a/{}'.format(json_user["user_id"])

        # Embed
        embed = discord.Embed(
            color = discord.Color(0xe969a2),
            timestamp = datetime.utcnow(),
            title = "{}'s Top 10 Plays".format(json_user["username"]),
            url = "https://osu.ppy.sh/users/{}".format(json_user["user_id"])
        )

        # Checking if user has scores
        if json_scores:         
            # Top 10 plays, adding fields to embed
            for play in json_scores:
                r_map = requests.get("https://osu.ppy.sh/api/get_beatmaps?b={}&k={}".format(play['beatmap_id'], osu_token))
                json_map = r_map.json()[0]
                # Mods verification
                conjunto_mods = int(play['enabled_mods'])

                lista_mods = [
                    {"None": 0},
                    {"NF": 1},
                    {"EZ": 2},
                    {"TD": 4},
                    {"HD": 8},
                    {"DT": 64},
                    {"NC": 576},
                    {"HR": 16},
                    {"SD": 32},
                    {"PF": 16416},
                    {"HT": 256},
                    {"FL": 1024},
                    ]
                mods_usados = []

                for mod in lista_mods:
                    for mod_name, mod_value in mod.items():
                        resultado = conjunto_mods & mod_value
                        if resultado > 0:
                            mods_usados.append(mod_name)
                            # NC, PF verification
                            if mod_name == "NC" and resultado == 64:
                                mods_usados.remove("NC")
                            if mod_name == "PF" and (resultado == 16384 or resultado == 32):
                                mods_usados.remove("PF")
                            if mod_name == "NC" and resultado == 576:
                                mods_usados.remove("DT")
                            if mod_name == "PF" and resultado == 16416:
                                mods_usados.remove("SD")

                # print("".join(mods_usados))
                string_mods = "".join(mods_usados)

                # pp verification
                if float(play["pp"]) - math.floor(float(play["pp"])) < 0.5:
                    pp_map = math.floor(float(play["pp"]))
                else:
                    pp_map = math.ceil(float(play["pp"]))

                if not string_mods:
                    embed.add_field(name="**{}pp**".format(pp_map), value="{} - **{}** [{}]".format(json_map['artist'], json_map['title_unicode'], json_map['version']), inline=False)
                else:
                    embed.add_field(name="**{}pp**".format(pp_map), value="{} - **{}** [{}] **+{}**".format(json_map['artist'], json_map['title_unicode'], json_map['version'], string_mods), inline=False)

            embed.set_thumbnail(url=avatar)
            embed.set_footer(icon_url='{}'.format(ctx.message.author.avatar_url_as(format=None, static_format='png')).split("?")[0], text="Gerado por {0}".format(ctx.message.author.name))
            message = await ctx.send(embed=embed)
            await message.add_reaction('<:PogYou:695437835964252222>')
        # If user doesnt have scores
        else:
            embed.add_field(name="No awesome performance records yet!", value=":sob:", inline=False)
            embed.set_thumbnail(url=avatar)
            embed.set_footer(icon_url='{}'.format(ctx.message.author.avatar_url_as(format=None, static_format='png')).split("?")[0], text="Gerado por {0}".format(ctx.message.author.name))
            message = await ctx.send(embed=embed)
            await message.add_reaction('<:SadChamp:695437902032797766>')
    # Username is incorrect or is not given
    else:
        if username == None:
            embed = discord.Embed(
                color = discord.Color(0xff0000),
                timestamp = datetime.utcnow(),
                description = "**Nome do usuário não fornecido! <a:rikkaBongo:697839129257312286> Use !top10 <username/id>**"
            )
            embed.set_footer(icon_url='{}'.format(ctx.message.author.avatar_url_as(format=None, static_format='png')).split("?")[0], text="Gerado por {0}".format(ctx.message.author.name))
            await ctx.send(embed=embed)
        elif not json_user:
            embed = discord.Embed(
                color = discord.Color(0xff0000),
                timestamp = datetime.utcnow(),
                description = "**Usuário não existe! <a:rikkaBongo:697839129257312286>**"
            )
            embed.set_footer(icon_url='{}'.format(ctx.message.author.avatar_url_as(format=None, static_format='png')).split("?")[0], text="Gerado por {0}".format(ctx.message.author.name))
            await ctx.send(embed=embed)

# Checking if arguments are valid
@top10.error
async def top10_error(ctx, error):
    if isinstance(error, commands.BadArgument):
        embed = discord.Embed(
            color = discord.Color(0xff0000),
            timestamp = datetime.utcnow(),
            description = "**Sintaxe incorreta! Use !top10 <member/id>**"
        )
        embed.set_footer(icon_url='{}'.format(ctx.message.author.avatar_url_as(format=None, static_format='png')).split("?")[0], text="Gerado por {0}".format(ctx.message.author.name))
        await ctx.send(embed=embed)


# !yt - plays a song from youtube
@client.command()
async def yt(ctx, *, url):
    # Bot can play only 1 song at a time
    try:
        if ctx.author.voice is not None:
            channel = ctx.author.voice.channel
            # Connecting the bot if its not connected to a voice channel
            if ctx.voice_client is None:
                await channel.connect()
            # Moving the bot
            else:
                await ctx.voice_client.move_to(channel)
                
            player = await YTDLSource.from_url(url, stream=True)
            ctx.voice_client.play(player, after=lambda e: print('Player error: %s' % e) if e else None)

            embed = discord.Embed(
                color = discord.Color(0xf8ff1f),
                timestamp = datetime.utcnow(),
                title = player.title,
                url = url,
                description = 'Now playing: **{}**'.format(player.title)
            )
            embed.set_footer(icon_url='{}'.format(ctx.message.author.avatar_url_as(format=None, static_format='png')).split("?")[0], text="Gerado por {0}".format(ctx.message.author.name))
            await ctx.send(embed=embed)
        else:
            embed = discord.Embed(
                color = discord.Color(0xff0000),
                timestamp = datetime.utcnow(),
                description = '**Not connected to a voice channel!**'
            )
            embed.set_footer(icon_url='{}'.format(ctx.message.author.avatar_url_as(format=None, static_format='png')).split("?")[0], text="Gerado por {0}".format(ctx.message.author.name))
            await ctx.send(embed=embed)
    except:
        embed = discord.Embed(
            color = discord.Color(0xf8ff1f),
            timestamp = datetime.utcnow(),
            title = player.title,
            url = url,
            description = 'Currently playing: **{}**'.format(player.title)
        )
        embed.set_footer(icon_url='{}'.format(ctx.message.author.avatar_url_as(format=None, static_format='png')).split("?")[0], text="Gerado por {0}".format(ctx.message.author.name))
        await ctx.send(embed=embed)

# Checking if arguments are valid
@yt.error
async def yt_error(ctx, error):
    if isinstance(error, commands.BadArgument):
        embed = discord.Embed(
            color = discord.Color(0xff0000),
            timestamp = datetime.utcnow(),
            description = "**Sintaxe incorreta! Use !yt <url>**"
        )
        embed.set_footer(icon_url='{}'.format(ctx.message.author.avatar_url_as(format=None, static_format='png')).split("?")[0], text="Gerado por {0}".format(ctx.message.author.name))
        await ctx.send(embed=embed)
    elif isinstance(error, commands.MissingRequiredArgument):
        embed = discord.Embed(
            color = discord.Color(0xff0000),
            timestamp = datetime.utcnow(),
            description = "**Sintaxe incorreta! Use !yt <url>**"
        )
        embed.set_footer(icon_url='{}'.format(ctx.message.author.avatar_url_as(format=None, static_format='png')).split("?")[0], text="Gerado por {0}".format(ctx.message.author.name))
        await ctx.send(embed=embed)
    else:
        embed = discord.Embed(
            color = discord.Color(0xff0000),
            timestamp = datetime.utcnow(),
            description = "**Link/formato de arquivo não suportado!**"
        )
        embed.set_footer(icon_url='{}'.format(ctx.message.author.avatar_url_as(format=None, static_format='png')).split("?")[0], text="Gerado por {0}".format(ctx.message.author.name))
        await ctx.send(embed=embed)


# !volume - adjusts song's volume
@client.command()
async def volume(ctx, volume: int):
    # Volume cant exceed 200%
    if volume <= 200:
        # Only adjusts the volume if bot is connected to a voice channel
        if ctx.voice_client is None:
            embed = discord.Embed(
                color = discord.Color(0xff0000),
                timestamp = datetime.utcnow(),
                description = '**Not connected to a voice channel!**'
            )
            embed.set_footer(icon_url='{}'.format(ctx.message.author.avatar_url_as(format=None, static_format='png')).split("?")[0], text="Gerado por {0}".format(ctx.message.author.name))
            await ctx.send(embed=embed)
        else:
            ctx.voice_client.source.volume = volume / 100

            # if volume is a negative value, set to 0
            if volume < 0:
                volume = 0
    
            embed = discord.Embed(
                color = discord.Color(0xf8ff1f),
                timestamp = datetime.utcnow(),
                description = "Changed volume to {}%".format(volume)
            )
            embed.set_footer(icon_url='{}'.format(ctx.message.author.avatar_url_as(format=None, static_format='png')).split("?")[0], text="Gerado por {0}".format(ctx.message.author.name))
            await ctx.send(embed=embed)
    else:
        if ctx.voice_client is None:
            embed = discord.Embed(
                color = discord.Color(0xff0000),
                timestamp = datetime.utcnow(),
                description = '**Not connected to a voice channel!**'
            )
            embed.set_footer(icon_url='{}'.format(ctx.message.author.avatar_url_as(format=None, static_format='png')).split("?")[0], text="Gerado por {0}".format(ctx.message.author.name))
            await ctx.send(embed=embed)
        else:
            embed = discord.Embed(
                color = discord.Color(0xff0000),
                timestamp = datetime.utcnow(),
                description = '**The limit is 200%!**'
            )
            embed.set_footer(icon_url='{}'.format(ctx.message.author.avatar_url_as(format=None, static_format='png')).split("?")[0], text="Gerado por {0}".format(ctx.message.author.name))
            await ctx.send(embed=embed)

# Checking if arguments are valid
@volume.error
async def volume_error(ctx, error):
    if isinstance(error, commands.BadArgument):
        embed = discord.Embed(
            color = discord.Color(0xff0000),
            timestamp = datetime.utcnow(),
            description = "**Use um valor inteiro!**"
        )
        embed.set_footer(icon_url='{}'.format(ctx.message.author.avatar_url_as(format=None, static_format='png')).split("?")[0], text="Gerado por {0}".format(ctx.message.author.name))
        await ctx.send(embed=embed)
    elif isinstance(error, commands.MissingRequiredArgument):
        embed = discord.Embed(
            color = discord.Color(0xff0000),
            timestamp = datetime.utcnow(),
            description = "**Sintaxe incorreta! Use !volume <integer>**"
        )
        embed.set_footer(icon_url='{}'.format(ctx.message.author.avatar_url_as(format=None, static_format='png')).split("?")[0], text="Gerado por {0}".format(ctx.message.author.name))
        await ctx.send(embed=embed)


# !stop - stops song and disconnect bot from voice channel
@client.command()
async def stop(ctx):
    # Only disconnects if bot is connected to a voice channel
    if ctx.voice_client is None:
        embed = discord.Embed(
            color = discord.Color(0xff0000),
            timestamp = datetime.utcnow(),
            description = '**Not connected to a voice channel!**'
        )
        embed.set_footer(icon_url='{}'.format(ctx.message.author.avatar_url_as(format=None, static_format='png')).split("?")[0], text="Gerado por {0}".format(ctx.message.author.name))
        await ctx.send(embed=embed)
    else:
        # Disconnecting
        await ctx.voice_client.disconnect()

# Checking if arguments are valid
@stop.error
async def stop_error(ctx, error):
    if isinstance(error, commands.BadArgument):
        embed = discord.Embed(
            color = discord.Color(0xff0000),
            timestamp = datetime.utcnow(),
            description = "**Sintaxe incorreta! Use !stop**"
        )
        embed.set_footer(icon_url='{}'.format(ctx.message.author.avatar_url_as(format=None, static_format='png')).split("?")[0], text="Gerado por {0}".format(ctx.message.author.name))
        await ctx.send(embed=embed)


# !man - library functions - Linux man pages
@client.command()
async def man(ctx, nome_funcao):
    url = requests.get('https://linux.die.net/man/3/{}'.format(nome_funcao))
    # request was successful and the server responded with the data requested
    if url.status_code == 200:
        await ctx.send('https://linux.die.net/man/3/{}'.format(nome_funcao))
    else:
        embed = discord.Embed(
            color = discord.Color(0xff0000),
            timestamp = datetime.utcnow(),
            description = "**Função não foi encontrada!**"
        )
        embed.set_footer(icon_url='{}'.format(ctx.message.author.avatar_url_as(format=None, static_format='png')).split("?")[0], text="Gerado por {0}".format(ctx.message.author.name))
        await ctx.send(embed=embed)

# Checking if arguments are valid
@man.error
async def man_error(ctx, error):
    if isinstance(error, commands.MissingRequiredArgument):
        embed = discord.Embed(
            color = discord.Color(0xff0000),
            timestamp = datetime.utcnow(),
            description = "**Nome da função não fornecido! <a:rikkaBongo:697839129257312286> Use !man <function>**"
        )
        embed.set_footer(icon_url='{}'.format(ctx.message.author.avatar_url_as(format=None, static_format='png')).split("?")[0], text="Gerado por {0}".format(ctx.message.author.name))
        await ctx.send(embed=embed)


# !pat - pat a member
@client.command()
async def pat(ctx, member: discord.Member = None):
    target = "pat"
    
    if member:
        embed = discord.Embed(
            color = discord.Color(0xB8B8B8),
            timestamp = datetime.utcnow(),
            description = "<@!{}> pats <@!{}>".format(ctx.message.author.id, member.id)
        )
        embed.set_image(url=nekos.img(target))
        embed.set_footer(icon_url='{}'.format(ctx.message.author.avatar_url_as(format=None, static_format='png')).split("?")[0], text="Gerado por {0}".format(ctx.message.author.name))
        await ctx.send(embed=embed)
    else:
        embed = discord.Embed(
            color = discord.Color(0xff0000),
            timestamp = datetime.utcnow(),
            description = "**Preciso de um usuário! <a:rikkaBongo:697839129257312286>**"
        )
        embed.set_footer(icon_url='{}'.format(ctx.message.author.avatar_url_as(format=None, static_format='png')).split("?")[0], text="Gerado por {0}".format(ctx.message.author.name))
        await ctx.send(embed=embed)

# Checking if arguments are valid
@pat.error
async def pat_error(ctx, error):
    if isinstance(error, commands.BadArgument):
        embed = discord.Embed(
            color = discord.Color(0xff0000),
            timestamp = datetime.utcnow(),
            description = "**Mencione um membro do canal! <a:rikkaBongo:697839129257312286>**"
        )
        embed.set_footer(icon_url='{}'.format(ctx.message.author.avatar_url_as(format=None, static_format='png')).split("?")[0], text="Gerado por {0}".format(ctx.message.author.name))
        await ctx.send(embed=embed)


# !poke - poke a member
@client.command()
async def poke(ctx, member: discord.Member = None):
    target = "poke"
    
    if member:
        embed = discord.Embed(
            color = discord.Color(0xB8B8B8),
            timestamp = datetime.utcnow(),
            description = "<@!{}> cutuca <@!{}>".format(ctx.message.author.id, member.id)
        )
        embed.set_image(url=nekos.img(target))
        embed.set_footer(icon_url='{}'.format(ctx.message.author.avatar_url_as(format=None, static_format='png')).split("?")[0], text="Gerado por {0}".format(ctx.message.author.name))
        await ctx.send(embed=embed)
    else:
        embed = discord.Embed(
            color = discord.Color(0xff0000),
            timestamp = datetime.utcnow(),
            description = "**Preciso de um usuário! <a:rikkaBongo:697839129257312286>**"
        )
        embed.set_footer(icon_url='{}'.format(ctx.message.author.avatar_url_as(format=None, static_format='png')).split("?")[0], text="Gerado por {0}".format(ctx.message.author.name))
        await ctx.send(embed=embed)

# Checking if arguments are valid
@poke.error
async def poke_error(ctx, error):
    if isinstance(error, commands.BadArgument):
        embed = discord.Embed(
            color = discord.Color(0xff0000),
            timestamp = datetime.utcnow(),
            description = "**Mencione um membro do canal! <a:rikkaBongo:697839129257312286>**"
        )
        embed.set_footer(icon_url='{}'.format(ctx.message.author.avatar_url_as(format=None, static_format='png')).split("?")[0], text="Gerado por {0}".format(ctx.message.author.name))
        await ctx.send(embed=embed)


# !kiss - kiss a member
@client.command()
async def kiss(ctx, member: discord.Member = None):
    target = "kiss"
    
    if member:
        embed = discord.Embed(
            color = discord.Color(0xB8B8B8),
            timestamp = datetime.utcnow(),
            description = "<@!{}> beija <@!{}>".format(ctx.message.author.id, member.id)
        )
        embed.set_image(url=nekos.img(target))
        embed.set_footer(icon_url='{}'.format(ctx.message.author.avatar_url_as(format=None, static_format='png')).split("?")[0], text="Gerado por {0}".format(ctx.message.author.name))
        await ctx.send(embed=embed)
    else:
        embed = discord.Embed(
            color = discord.Color(0xff0000),
            timestamp = datetime.utcnow(),
            description = "**Preciso de um usuário! <a:rikkaBongo:697839129257312286>**"
        )
        embed.set_footer(icon_url='{}'.format(ctx.message.author.avatar_url_as(format=None, static_format='png')).split("?")[0], text="Gerado por {0}".format(ctx.message.author.name))
        await ctx.send(embed=embed)

# Checking if arguments are valid
@kiss.error
async def kiss_error(ctx, error):
    if isinstance(error, commands.BadArgument):
        embed = discord.Embed(
            color = discord.Color(0xff0000),
            timestamp = datetime.utcnow(),
            description = "**Mencione um membro do canal! <a:rikkaBongo:697839129257312286>**"
        )
        embed.set_footer(icon_url='{}'.format(ctx.message.author.avatar_url_as(format=None, static_format='png')).split("?")[0], text="Gerado por {0}".format(ctx.message.author.name))
        await ctx.send(embed=embed)


# !neko - some random neko pic
@client.command()
async def neko(ctx):
    target = "neko"
    
    embed = discord.Embed(
        color = discord.Color(0xB8B8B8),
        timestamp = datetime.utcnow(),
    )
    embed.set_image(url=nekos.img(target))
    embed.set_footer(icon_url='{}'.format(ctx.message.author.avatar_url_as(format=None, static_format='png')).split("?")[0], text="Gerado por {0}".format(ctx.message.author.name))
    await ctx.send(embed=embed)


# !baka - member is baka
@client.command()
async def baka(ctx, member: discord.Member = None):
    target = "baka"
    
    if member:
        embed = discord.Embed(
            color = discord.Color(0xB8B8B8),
            timestamp = datetime.utcnow(),
            description = "<@!{}>, b-baka!".format(member.id)
        )
        embed.set_image(url=nekos.img(target))
        embed.set_footer(icon_url='{}'.format(ctx.message.author.avatar_url_as(format=None, static_format='png')).split("?")[0], text="Gerado por {0}".format(ctx.message.author.name))
        await ctx.send(embed=embed)
    else:
        embed = discord.Embed(
            color = discord.Color(0xff0000),
            timestamp = datetime.utcnow(),
            description = "**Preciso de um usuário! <a:rikkaBongo:697839129257312286>**"
        )
        embed.set_footer(icon_url='{}'.format(ctx.message.author.avatar_url_as(format=None, static_format='png')).split("?")[0], text="Gerado por {0}".format(ctx.message.author.name))
        await ctx.send(embed=embed)

# Checking if arguments are valid
@baka.error
async def baka_error(ctx, error):
    if isinstance(error, commands.BadArgument):
        embed = discord.Embed(
            color = discord.Color(0xff0000),
            timestamp = datetime.utcnow(),
            description = "**Mencione um membro do canal! <a:rikkaBongo:697839129257312286>**"
        )
        embed.set_footer(icon_url='{}'.format(ctx.message.author.avatar_url_as(format=None, static_format='png')).split("?")[0], text="Gerado por {0}".format(ctx.message.author.name))
        await ctx.send(embed=embed)


# !hug - hug a member
@client.command()
async def hug(ctx, member: discord.Member = None):
    target = "hug"
    
    if member:
        embed = discord.Embed(
            color = discord.Color(0xB8B8B8),
            timestamp = datetime.utcnow(),
            description = "<@!{}> hugs <@!{}>".format(ctx.message.author.id, member.id)
        )
        embed.set_image(url=nekos.img(target))
        embed.set_footer(icon_url='{}'.format(ctx.message.author.avatar_url_as(format=None, static_format='png')).split("?")[0], text="Gerado por {0}".format(ctx.message.author.name))
        await ctx.send(embed=embed)
    else:
        embed = discord.Embed(
            color = discord.Color(0xff0000),
            timestamp = datetime.utcnow(),
            description = "**Preciso de um usuário! <a:rikkaBongo:697839129257312286>**"
        )
        embed.set_footer(icon_url='{}'.format(ctx.message.author.avatar_url_as(format=None, static_format='png')).split("?")[0], text="Gerado por {0}".format(ctx.message.author.name))
        await ctx.send(embed=embed)

# Checking if arguments are valid
@hug.error
async def hug_error(ctx, error):
    if isinstance(error, commands.BadArgument):
        embed = discord.Embed(
            color = discord.Color(0xff0000),
            timestamp = datetime.utcnow(),
            description = "**Mencione um membro do canal! <a:rikkaBongo:697839129257312286>**"
        )
        embed.set_footer(icon_url='{}'.format(ctx.message.author.avatar_url_as(format=None, static_format='png')).split("?")[0], text="Gerado por {0}".format(ctx.message.author.name))
        await ctx.send(embed=embed)


# !cuddle - cuddle a member
@client.command()
async def cuddle(ctx, member: discord.Member = None):
    target = "cuddle"
    
    if member:
        embed = discord.Embed(
            color = discord.Color(0xB8B8B8),
            timestamp = datetime.utcnow(),
            description = "<@!{}> cuddles <@!{}>".format(ctx.message.author.id, member.id)
        )
        embed.set_image(url=nekos.img(target))
        embed.set_footer(icon_url='{}'.format(ctx.message.author.avatar_url_as(format=None, static_format='png')).split("?")[0], text="Gerado por {0}".format(ctx.message.author.name))
        await ctx.send(embed=embed)
    else:
        embed = discord.Embed(
            color = discord.Color(0xff0000),
            timestamp = datetime.utcnow(),
            description = "**Preciso de um usuário! <a:rikkaBongo:697839129257312286>**"
        )
        embed.set_footer(icon_url='{}'.format(ctx.message.author.avatar_url_as(format=None, static_format='png')).split("?")[0], text="Gerado por {0}".format(ctx.message.author.name))
        await ctx.send(embed=embed)

# Checking if arguments are valid
@cuddle.error
async def cuddle_error(ctx, error):
    if isinstance(error, commands.BadArgument):
        embed = discord.Embed(
            color = discord.Color(0xff0000),
            timestamp = datetime.utcnow(),
            description = "**Mencione um membro do canal! <a:rikkaBongo:697839129257312286>**"
        )
        embed.set_footer(icon_url='{}'.format(ctx.message.author.avatar_url_as(format=None, static_format='png')).split("?")[0], text="Gerado por {0}".format(ctx.message.author.name))
        await ctx.send(embed=embed)


# !youtube - not working properly
# @client.command()
# async def youtube(ctx, *, search):
#     query_string = urllib.parse.urlencode({
#         'search_query': search
#     })
#     htm_content = urllib.request.urlopen(
#         'http://www.youtube.com/results?' + query_string
#     )
#     search_results = re.findall('href=\"\\/watch\\?v=(.{11})', htm_content.read().decode())
#     await ctx.send('http://www.youtube.com/watch?v=' + search_results[0])


# When command is not found/errors
@client.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.CommandNotFound):
        embed = discord.Embed(
            color = discord.Color(0xff0000),
            timestamp = datetime.utcnow(),
            description = "**Comando inexistente!**"
        )
        embed.set_footer(icon_url='{}'.format(ctx.message.author.avatar_url_as(format=None, static_format='png')).split("?")[0], text="Gerado por {0}".format(ctx.message.author.name))
        await ctx.send(embed=embed)
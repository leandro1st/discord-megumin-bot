import discord
from discord.ext import commands
from datetime import datetime, timezone
from pytz import timezone #timezone()

class User(commands.Cog, name="Usuário"):
    """Comandos relacionados ao usuário"""


    def __init__(self, client):
        self.client = client


    # !avatar - display user's avatar
    @commands.command(usage="(optional member)", description="Display user's avatar", aliases=["pfp"])
    async def avatar(self, ctx, member: discord.Member = None):
        # If member name is given
        if member != None:
            # if member is a bot
            if member.bot:
                embed = discord.Embed(
                    color = discord.Color.dark_blue(),
                    title = 'Avatar de {0} (BOT)'.format(member.name),
                    url = '{}'.format(member.avatar_url_as(format=None, static_format='png')).split("?")[0],
                    timestamp = datetime.utcnow()
                )
            else:
                embed = discord.Embed(
                    color = discord.Color(0x0087FF),
                    title = 'Avatar de {0}'.format(member.name),
                    url = '{}'.format(member.avatar_url_as(format=None, static_format='png')).split("?")[0],
                    timestamp = datetime.utcnow()
                )

            embed.set_footer(icon_url='{}'.format(ctx.message.author.avatar_url_as(format=None, static_format='png')).split("?")[0], text="Gerado por {0}".format(ctx.message.author.name))
            embed.set_image(url='{}'.format(member.avatar_url_as(format=None, static_format='png', size=4096)))
            await ctx.reply(embed=embed)
        # else member is himself
        else:
            embed = discord.Embed(
                color = discord.Color.dark_blue(),
                title = 'Avatar de {0}'.format(ctx.message.author.name),
                url = '{}'.format(ctx.message.author.avatar_url_as(format=None, static_format='png')).split("?")[0],
                timestamp = datetime.utcnow()
            )

            embed.set_footer(icon_url='{}'.format(ctx.message.author.avatar_url_as(format=None, static_format='png')).split("?")[0], text="Gerado por {0}".format(ctx.message.author.name))
            embed.set_image(url='{}'.format(ctx.message.author.avatar_url_as(format=None, static_format='png', size=4096)))
            await ctx.reply(embed=embed)

    # Checking if arguments are valid
    @avatar.error
    async def avatar_error(self, ctx, error):
        if isinstance(error, commands.BadArgument):
            embed = discord.Embed(
                color = discord.Color(0xff0000),
                timestamp = datetime.utcnow(),
                description = "**Mencione um membro do canal! <a:rikkaBongo:878038328333697045>**"
            )

            embed.set_footer(icon_url='{}'.format(ctx.message.author.avatar_url_as(format=None, static_format='png')).split("?")[0], text="Gerado por {0}".format(ctx.message.author.name))
            await ctx.reply(embed=embed)

    
    # !user_info - display user's information
    @commands.command(usage="(optional member)", description="Display user's info")
    async def user_info(self, ctx, member: discord.Member = None):
        # If member name is given
        if member:
            # If member is a bot
            if member.bot:
                embed = discord.Embed(
                    color = discord.Color(0x5bcf78),
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
            await ctx.reply(embed=embed)
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
            await ctx.reply(embed=embed)

    # Checking if arguments are valid
    @user_info.error
    async def user_info_error(self, ctx, error):
        if isinstance(error, commands.BadArgument):
            embed = discord.Embed(
                color = discord.Color(0xff0000),
                timestamp = datetime.utcnow(),
                description = "**Mencione um membro do canal! <a:rikkaBongo:878038328333697045>**"
            )

            embed.set_footer(icon_url='{}'.format(ctx.message.author.avatar_url_as(format=None, static_format='png')).split("?")[0], text="Gerado por {0}".format(ctx.message.author.name))
            await ctx.reply(embed=embed)


    # !user_status - users activities
    @commands.command(usage="(optional member)", description="Display user's activities")
    async def user_status(self, ctx, member: discord.Member = None):
        # Atividades do usuário
        atividade = ""
        
        # If member name is given
        if member:
            for i, activity in enumerate(member.activities):
                # First iteration
                if i == 0:
                    atividade += "<@!{}> is ".format(member.id)
                # Last iteration
                elif i == len(member.activities) - 1:
                    atividade += " and "
                else:
                    atividade += ", "

                if activity.type.name == "listening":
                    atividade += "{} to {}".format(activity.type.name, activity.name)
                else:
                    atividade += "{} {}".format(activity.type.name, activity.name)
            
            # Se atividade não estiver vazia
            if atividade:
                await ctx.reply(atividade)
            else:
                await ctx.reply("<@!{}> não está fazendo nada".format(member.id))
        # else member is himself
        else:
            for i, activity in enumerate(ctx.message.author.activities):    
                # First iteration
                if i == 0:
                    atividade += "<@!{}> is ".format(ctx.message.author.id)
                # Last iteration
                elif i == len(ctx.message.author.activities) - 1:
                    atividade += " and "
                else:
                    atividade += ", "

                if activity.type.name == "listening":
                    atividade += "{} to {}".format(activity.type.name, activity.name)
                else:
                    atividade += "{} {}".format(activity.type.name, activity.name)
                
            # Se atividade não estiver vazia
            if atividade:
                await ctx.reply(atividade)
            else:
                await ctx.reply("<@!{}> não está fazendo nada".format(ctx.message.author.id))

    # Checking if arguments are valid
    @user_status.error
    async def status(self, ctx, error):
        if isinstance(error, commands.BadArgument):
            embed = discord.Embed(
                color = discord.Color(0xff0000),
                timestamp = datetime.utcnow(),
                description = "**Mencione um membro do canal! <a:rikkaBongo:878038328333697045>**"
            )

            embed.set_footer(icon_url='{}'.format(ctx.message.author.avatar_url_as(format=None, static_format='png')).split("?")[0], text="Gerado por {0}".format(ctx.message.author.name))
            await ctx.reply(embed=embed)


def setup(client):
    client.add_cog(User(client))
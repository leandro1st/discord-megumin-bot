import discord
from discord.ext import commands
from datetime import datetime
import re

class Admin(commands.Cog, name="Administrador"):
    """Comandos para administradores"""


    def __init__(self, client):
        self.client = client


    # !rename - change user's nick
    @commands.command(usage="<member> <new nick>", description="Change user's nickname")
    @commands.has_permissions(manage_nicknames=True)
    async def rename(self, ctx, member: discord.Member = None, *, new_name = None):
        if member and new_name:
            # checking users hierarchy and if member isnt himself
            if member.top_role >= ctx.author.top_role and member != ctx.message.author:
                embed = discord.Embed(
                    color = discord.Color(0xff0000),
                    timestamp = datetime.utcnow(),
                    description = "**Você apenas consegue renomear o nickname de membros com cargo inferior ao seu!**"
                )
                
                embed.set_footer(icon_url='{}'.format(ctx.message.author.avatar_url_as(format=None, static_format='png')).split("?")[0], text="Gerado por {0}".format(ctx.message.author.name))
                await ctx.reply(embed=embed)
            # checking bots hierarchy and if member isnt itself
            elif member.top_role >= ctx.guild.get_member(self.client.user.id).top_role and member != self.client.user:
                embed = discord.Embed(
                    color = discord.Color(0xff0000),
                    timestamp = datetime.utcnow(),
                    description = "**Eu apenas consigo renomear o nickname de membros com cargo inferior ao meu!**"
                )

                embed.set_footer(icon_url='{}'.format(ctx.message.author.avatar_url_as(format=None, static_format='png')).split("?")[0], text="Gerado por {0}".format(ctx.message.author.name))
                await ctx.reply(embed=embed)
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
                await ctx.reply(embed=embed)
        else:
            embed = discord.Embed(
                color = discord.Color(0xff0000),
                timestamp = datetime.utcnow(),
                description = "**Sintaxe incorreta! Use !rename <member> <new nick>**"
            )
            embed.set_footer(icon_url='{}'.format(ctx.message.author.avatar_url_as(format=None, static_format='png')).split("?")[0], text="Gerado por {0}".format(ctx.message.author.name))
            await ctx.reply(embed=embed)

    # Checking if an user has permission to use this command/if arguments are valid
    @rename.error
    async def rename_error(self, ctx, error):
        if isinstance(error, commands.MissingPermissions):
            embed = discord.Embed(
                color = discord.Color(0xff0000),
                timestamp = datetime.utcnow(),
                description = "**Você não possui permissão para alterar nicknames!**"
            )
            embed.set_footer(icon_url='{}'.format(ctx.message.author.avatar_url_as(format=None, static_format='png')).split("?")[0], text="Gerado por {0}".format(ctx.message.author.name))
            await ctx.reply(embed=embed)
        elif isinstance(error, commands.BadArgument):
            embed = discord.Embed(
                color = discord.Color(0xff0000),
                timestamp = datetime.utcnow(),
                description = "**Sintaxe incorreta! Use !rename <member> <new nick>**"
            )
            embed.set_footer(icon_url='{}'.format(ctx.message.author.avatar_url_as(format=None, static_format='png')).split("?")[0], text="Gerado por {0}".format(ctx.message.author.name))
            await ctx.reply(embed=embed)
            

    # !mute - mute members
    @commands.command(usage="<member> (optional reason)", description="Mute a member")
    @commands.has_permissions(administrator=True)
    async def mute(self, ctx, member: discord.Member = None, *, reason=None):
        if member != None:
            if member == ctx.message.author:
                embed = discord.Embed(
                    color = discord.Color(0xff0000),
                    timestamp = datetime.utcnow(),
                    description = "**Você não pode se mutar!**"
                )

                embed.set_footer(icon_url='{}'.format(ctx.message.author.avatar_url_as(format=None, static_format='png')).split("?")[0], text="Gerado por {0}".format(ctx.message.author.name))
                await ctx.reply(embed=embed)
            # if member is a bot
            elif member.bot:
                embed = discord.Embed(
                    color = discord.Color(0xff0000),
                    timestamp = datetime.utcnow(),
                    description = "**Você não pode mutar um bot!**"
                )

                embed.set_footer(icon_url='{}'.format(ctx.message.author.avatar_url_as(format=None, static_format='png')).split("?")[0], text="Gerado por {0}".format(ctx.message.author.name))
                await ctx.reply(embed=embed)
            else:
                # users hierarchy checking
                if member.top_role >= ctx.author.top_role:
                    embed = discord.Embed(
                        color = discord.Color(0xff0000),
                        timestamp = datetime.utcnow(),
                        description = "**Você apenas consegue mutar membros com cargo inferior ao seu!**"
                    )

                    embed.set_footer(icon_url='{}'.format(ctx.message.author.avatar_url_as(format=None, static_format='png')).split("?")[0], text="Gerado por {0}".format(ctx.message.author.name))
                    await ctx.reply(embed=embed)
                # bots hierarchy checking
                elif member.top_role >= ctx.guild.get_member(self.client.user.id).top_role:
                    embed = discord.Embed(
                        color = discord.Color(0xff0000),
                        timestamp = datetime.utcnow(),
                        description = "**Eu apenas consigo mutar membros com cargo inferior ao meu!**"
                    )

                    embed.set_footer(icon_url='{}'.format(ctx.message.author.avatar_url_as(format=None, static_format='png')).split("?")[0], text="Gerado por {0}".format(ctx.message.author.name))
                    await ctx.reply(embed=embed)
                else:
                    # user's role list
                    user_roles = []
                    for role in member.roles:
                        # appending role name to list
                        user_roles.append(role.name)

                    # checks if user_roles not contains Boruto role
                    if "Boruto" not in user_roles:
                        # Checking if there is a role named Boruto, a channel named hueco_mundo and a category named main
                        role_muted = discord.utils.get(ctx.guild.roles, name="Boruto")
                        hueco_mundo = discord.utils.get(ctx.guild.text_channels, name="hueco_mundo")
                        category = discord.utils.get(ctx.guild.categories, name="main")

                        # Checks if there is a role named Boruto
                        if not role_muted:
                            # creating new role named Boruto
                            role_muted = await ctx.guild.create_role(name="Boruto", reason="To use for muting", colour=discord.Colour(0x4A4A4A))
                            
                            for channel in ctx.guild.channels:
                                # settings
                                await channel.set_permissions(role_muted, send_messages=False)

                            await member.edit(roles=[role_muted])
                        else:
                            await member.edit(roles=[role_muted])
                            # await member.add_roles(role_muted)

                        # Checks if there is a category named main
                        if not category:
                            category = await ctx.guild.create_category('main')

                        # Checks if there is a channel named hueco_mundo
                        if not hueco_mundo:
                            # permissions
                            overwrites = {ctx.guild.default_role: discord.PermissionOverwrite(send_messages=False),
                                        ctx.guild.me: discord.PermissionOverwrite(send_messages=True),
                                        role_muted: discord.PermissionOverwrite(send_messages=True)}

                            # creating a channel named hueco_mundo
                            channel = await ctx.message.guild.create_text_channel('hueco_mundo', overwrites=overwrites, category=category, topic="KEKW")
                            await channel.send("Welcome to Hueco Mundo, <@!{}> <:LULW:695753501309009991>".format(member.id))
                        else:
                            # await self.client.get_channel(846965091165143061).send("Welcome to Hueco Mundo, <@!{}> <:LULW:695753501309009991>".format(member.id))
                            await hueco_mundo.send("Welcome to Hueco Mundo, <@!{}> <:LULW:695753501309009991>".format(member.id))

                        # default reason
                        if reason == None:
                            reason = "<:SillyChamp:695437918625595542>"
                        
                        embed = discord.Embed(
                            color = discord.Color(0xE53A5E),
                            timestamp = datetime.utcnow(),
                            description = "<@!{}> foi mutado!\n**Motivo:** {}".format(member.id, reason)
                        )

                        embed.set_author(name="{} mutado!".format(member.name), icon_url='{}'.format(member.avatar_url_as(format=None, static_format='png')).split("?")[0])
                        embed.set_thumbnail(url='{}'.format(member.avatar_url_as(format=None, static_format='png')).split("?")[0])
                        embed.set_footer(icon_url='{}'.format(ctx.message.author.avatar_url_as(format=None, static_format='png')).split("?")[0], text="Mutado por {0}".format(ctx.message.author.name))
                        await ctx.reply(embed=embed)
                    else:
                        embed = discord.Embed(
                            color = discord.Color(0xff0000),
                            timestamp = datetime.utcnow(),
                            description = "<@!{}> já está mutado!".format(member.id)
                        )

                        embed.set_author(name="{}".format(member), icon_url='{}'.format(member.avatar_url_as(format=None, static_format='png')).split("?")[0])
                        embed.set_thumbnail(url='{}'.format(member.avatar_url_as(format=None, static_format='png')).split("?")[0])
                        embed.set_footer(icon_url='{}'.format(ctx.message.author.avatar_url_as(format=None, static_format='png')).split("?")[0], text="Gerado por {0}".format(ctx.message.author.name))
                        await ctx.reply(embed=embed)
        else:
            embed = discord.Embed(
                color = discord.Color(0xff0000),
                timestamp = datetime.utcnow(),
                description = "**Preciso de um usuário pra mutar! <a:rikkaBongo:697839129257312286>**"
            )

            embed.set_footer(icon_url='{}'.format(ctx.message.author.avatar_url_as(format=None, static_format='png')).split("?")[0], text="Gerado por {0}".format(ctx.message.author.name))
            await ctx.reply(embed=embed)

    # Checking if arguments are valid
    @mute.error
    async def mute_error(self, ctx, error):
        if isinstance(error, commands.MissingPermissions):
            embed = discord.Embed(
                color = discord.Color(0xff0000),
                timestamp = datetime.utcnow(),
                description = "**Você não possui permissão para mutar!**"
            )

            embed.set_footer(icon_url='{}'.format(ctx.message.author.avatar_url_as(format=None, static_format='png')).split("?")[0], text="Gerado por {0}".format(ctx.message.author.name))
            await ctx.reply(embed=embed)
        elif isinstance(error, commands.BadArgument):
            embed = discord.Embed(
                color = discord.Color(0xff0000),
                timestamp = datetime.utcnow(),
                description = "**Mencione um membro do canal! <a:rikkaBongo:697839129257312286>**"
            )

            embed.set_footer(icon_url='{}'.format(ctx.message.author.avatar_url_as(format=None, static_format='png')).split("?")[0], text="Gerado por {0}".format(ctx.message.author.name))
            await ctx.reply(embed=embed)


    # !unmute - unmute members
    @commands.command(usage="<member>", description="Unmute a member")
    @commands.has_permissions(administrator=True)
    async def unmute(self, ctx, member: discord.Member = None):
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
                    description = "<@!{}> foi desmutado!".format(member.id)
                )

                embed.set_author(name="{} desmutado!".format(member.name), icon_url='{}'.format(member.avatar_url_as(format=None, static_format='png')).split("?")[0])
                embed.set_thumbnail(url='{}'.format(member.avatar_url_as(format=None, static_format='png')).split("?")[0])
                embed.set_footer(icon_url='{}'.format(ctx.message.author.avatar_url_as(format=None, static_format='png')).split("?")[0], text="Desmutado por {0}".format(ctx.message.author.name))
                await ctx.reply(embed=embed)
            else:
                embed = discord.Embed(
                    color = discord.Color(0xff0000),
                    timestamp = datetime.utcnow(),
                    description = "<@!{}> não está mutado!".format(member.id)
                )

                embed.set_author(name="{}".format(member), icon_url='{}'.format(member.avatar_url_as(format=None, static_format='png')).split("?")[0])
                embed.set_thumbnail(url='{}'.format(member.avatar_url_as(format=None, static_format='png')).split("?")[0])
                embed.set_footer(icon_url='{}'.format(ctx.message.author.avatar_url_as(format=None, static_format='png')).split("?")[0], text="Gerado por {0}".format(ctx.message.author.name))
                await ctx.reply(embed=embed)
        else:
            embed = discord.Embed(
                color = discord.Color(0xff0000),
                timestamp = datetime.utcnow(),
                description = "**Preciso de um usuário pra desmutar! <a:rikkaBongo:697839129257312286>**"
            )

            embed.set_footer(icon_url='{}'.format(ctx.message.author.avatar_url_as(format=None, static_format='png')).split("?")[0], text="Gerado por {0}".format(ctx.message.author.name))
            await ctx.reply(embed=embed)

    # Checking if arguments are valid
    @unmute.error
    async def unmute_error(self, ctx, error):
        if isinstance(error, commands.MissingPermissions):
            embed = discord.Embed(
                color = discord.Color(0xff0000),
                timestamp = datetime.utcnow(),
                description = "**Você não possui permissão para desmutar!**"
            )

            embed.set_footer(icon_url='{}'.format(ctx.message.author.avatar_url_as(format=None, static_format='png')).split("?")[0], text="Gerado por {0}".format(ctx.message.author.name))
            await ctx.reply(embed=embed)
        elif isinstance(error, commands.BadArgument):
            embed = discord.Embed(
                color = discord.Color(0xff0000),
                timestamp = datetime.utcnow(),
                description = "**Mencione um membro do canal! <a:rikkaBongo:697839129257312286>**"
            )

            embed.set_footer(icon_url='{}'.format(ctx.message.author.avatar_url_as(format=None, static_format='png')).split("?")[0], text="Gerado por {0}".format(ctx.message.author.name))
            await ctx.reply(embed=embed)


    # !mutelist - displays mutelist
    @commands.command(description="Display mutelist")
    @commands.has_permissions(administrator=True)
    async def mutelist(self, ctx):
        contador = 0
        
        for member in ctx.guild.members:
            for role in member.roles:
                if role.name == "Boruto":
                    if contador == 0:
                        embed = discord.Embed(
                            color = discord.Color(0xEBCF02),
                            timestamp = datetime.utcnow(),
                            title = "Usuários Mutados"
                        )
                        contador += 1
                    embed.add_field(name="{}".format(member), value="<@!{}>".format(member.id), inline=False)
        
        if contador == 0:
            embed = discord.Embed(
                color = discord.Color(0xEBCF02),
                timestamp = datetime.utcnow(),
                title = "Usuários Mutados",
                description = "**Nenhum usuário foi mutado ainda!**"
            )

        embed.set_thumbnail(url='https://media1.tenor.com/images/31da06f3766e9bf24271ac0cf412d5fe/tenor.gif?itemid=18610807')
        embed.set_footer(icon_url='{}'.format(ctx.message.author.avatar_url_as(format=None, static_format='png')).split("?")[0], text="Gerado por {0}".format(ctx.message.author.name))

        await ctx.reply(embed=embed)

    # Checking if arguments are valid
    @mutelist.error
    async def mutelist_error(self, ctx, error):
        if isinstance(error, commands.MissingPermissions):
            embed = discord.Embed(
                color = discord.Color(0xff0000),
                timestamp = datetime.utcnow(),
                description = "**Você não possui permissão para acessar a Lista de Mutados!**"
            )
            embed.set_footer(icon_url='{}'.format(ctx.message.author.avatar_url_as(format=None, static_format='png')).split("?")[0], text="Gerado por {0}".format(ctx.message.author.name))
            await ctx.reply(embed=embed)


    # !kick - kick users
    @commands.command(usage="<member> (optional reason)", description="Kick a member")
    @commands.has_permissions(kick_members=True)
    async def kick(self, ctx, member: discord.Member = None, *, reason=None):
        if member != None:
            if member == ctx.message.author:
                embed = discord.Embed(
                    color = discord.Color(0xff0000),
                    timestamp = datetime.utcnow(),
                    description = "**Você não pode se expulsar!**"
                )

                embed.set_footer(icon_url='{}'.format(ctx.message.author.avatar_url_as(format=None, static_format='png')).split("?")[0], text="Gerado por {0}".format(ctx.message.author.name))
                await ctx.reply(embed=embed)
            else:
                # users hierarchy checking
                if member.top_role >= ctx.author.top_role:
                    embed = discord.Embed(
                        color = discord.Color(0xff0000),
                        timestamp = datetime.utcnow(),
                        description = "**Você apenas consegue expulsar membros com cargo inferior ao seu!**"
                    )

                    embed.set_footer(icon_url='{}'.format(ctx.message.author.avatar_url_as(format=None, static_format='png')).split("?")[0], text="Gerado por {0}".format(ctx.message.author.name))
                    await ctx.reply(embed=embed)
                # checking bots hierarchy and if member isnt itself
                elif member.top_role >= ctx.guild.get_member(self.client.user.id).top_role and member != self.client.user:
                    embed = discord.Embed(
                        color = discord.Color(0xff0000),
                        timestamp = datetime.utcnow(),
                        description = "**Eu apenas consigo expulsar membros com cargo inferior ao meu!**"
                    )

                    embed.set_footer(icon_url='{}'.format(ctx.message.author.avatar_url_as(format=None, static_format='png')).split("?")[0], text="Gerado por {0}".format(ctx.message.author.name))
                    await ctx.reply(embed=embed)
                else:
                    # checking if member is the bot itself
                    if member == self.client.user:
                        embed = discord.Embed(
                            color = discord.Color(0xff0000),
                            timestamp = datetime.utcnow(),
                            description = "**Eu não posso me expulsar!**"
                        )

                        embed.set_footer(icon_url='{}'.format(ctx.message.author.avatar_url_as(format=None, static_format='png')).split("?")[0], text="Gerado por {0}".format(ctx.message.author.name))
                        await ctx.reply(embed=embed)
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
                        await ctx.reply(embed=embed)

                        # if member is not a bot
                        if not member.bot:
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
            await ctx.reply(embed=embed)

    # Checking if arguments are valid
    @kick.error
    async def kick_error(self, ctx, error):
        if isinstance(error, commands.MissingPermissions):
            embed = discord.Embed(
                color = discord.Color(0xff0000),
                timestamp = datetime.utcnow(),
                description = "**Você não possui permissão para expulsar!**"
            )

            embed.set_footer(icon_url='{}'.format(ctx.message.author.avatar_url_as(format=None, static_format='png')).split("?")[0], text="Gerado por {0}".format(ctx.message.author.name))
            await ctx.reply(embed=embed)
        elif isinstance(error, commands.BadArgument):
            embed = discord.Embed(
                color = discord.Color(0xff0000),
                timestamp = datetime.utcnow(),
                description = "**Mencione um membro do canal! <a:rikkaBongo:697839129257312286>**"
            )

            embed.set_footer(icon_url='{}'.format(ctx.message.author.avatar_url_as(format=None, static_format='png')).split("?")[0], text="Gerado por {0}".format(ctx.message.author.name))
            await ctx.reply(embed=embed)


    # !ban - ban a member
    @commands.command(usage="<member> (optional reason)", description="Bankai")
    @commands.has_permissions(ban_members=True)
    async def ban(self, ctx, member: discord.Member = None, *, reason=None):
        if member != None:
            if member == ctx.message.author:
                embed = discord.Embed(
                    color = discord.Color(0xff0000),
                    timestamp = datetime.utcnow(),
                    description = "**Você não pode banir a si mesmo!**"
                )
                embed.set_footer(icon_url='{}'.format(ctx.message.author.avatar_url_as(format=None, static_format='png')).split("?")[0], text="Gerado por {0}".format(ctx.message.author.name))
                await ctx.reply(embed=embed)
            else:
                # users hierarchy checking
                if member.top_role >= ctx.author.top_role:
                    embed = discord.Embed(
                        color = discord.Color(0xff0000),
                        timestamp = datetime.utcnow(),
                        description = "**Você apenas consegue banir membros com cargo inferior ao seu!**"
                    )

                    embed.set_footer(icon_url='{}'.format(ctx.message.author.avatar_url_as(format=None, static_format='png')).split("?")[0], text="Gerado por {0}".format(ctx.message.author.name))
                    await ctx.reply(embed=embed)
                # checking bots hierarchy and if member isnt itself
                elif member.top_role >= ctx.guild.get_member(self.client.user.id).top_role and member != self.client.user:
                    embed = discord.Embed(
                        color = discord.Color(0xff0000),
                        timestamp = datetime.utcnow(),
                        description = "**Eu apenas consigo banir membros com cargo inferior ao meu!**"
                    )

                    embed.set_footer(icon_url='{}'.format(ctx.message.author.avatar_url_as(format=None, static_format='png')).split("?")[0], text="Gerado por {0}".format(ctx.message.author.name))
                    await ctx.reply(embed=embed)
                else:
                    # checking if member is the bot itself
                    if member == self.client.user:
                        embed = discord.Embed(
                            color = discord.Color(0xff0000),
                            timestamp = datetime.utcnow(),
                            description = "**Eu não posso me banir!**"
                        )

                        embed.set_footer(icon_url='{}'.format(ctx.message.author.avatar_url_as(format=None, static_format='png')).split("?")[0], text="Gerado por {0}".format(ctx.message.author.name))
                        await ctx.reply(embed=embed)
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
                        await ctx.reply(embed=embed)

                        # if member is not a bot
                        if not member.bot:
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
            await ctx.reply(embed=embed)

    # Checking if arguments are valid
    @ban.error
    async def ban_error(self, ctx, error):
        if isinstance(error, commands.MissingPermissions):
            embed = discord.Embed(
                color = discord.Color(0xff0000),
                timestamp = datetime.utcnow(),
                description = "**Você não possui permissão para banir!**"
            )

            embed.set_footer(icon_url='{}'.format(ctx.message.author.avatar_url_as(format=None, static_format='png')).split("?")[0], text="Gerado por {0}".format(ctx.message.author.name))
            await ctx.reply(embed=embed)
        elif isinstance(error, commands.BadArgument):
            embed = discord.Embed(
                color = discord.Color(0xff0000),
                timestamp = datetime.utcnow(),
                description = "**Mencione um membro do canal! <a:rikkaBongo:697839129257312286>**"
            )

            embed.set_footer(icon_url='{}'.format(ctx.message.author.avatar_url_as(format=None, static_format='png')).split("?")[0], text="Gerado por {0}".format(ctx.message.author.name))
            await ctx.reply(embed=embed)


    # !unban - unban a member
    @commands.command(usage="<name#discriminator/id>", description="Unban a banned member")
    @commands.has_permissions(administrator=True)
    async def unban(self, ctx, *, member=None):
        if member != None:
            banned_users = await ctx.guild.bans()

            # Verificando se o member fornecido segue o seguinte formato: nome#discriminator (discriminator deve ter somente 4 números)
            if re.compile('^(.+?)#(\d{4})$').search(member):
                m = re.compile('^(.+?)#(\d{4})$').search(member)
                member_name, member_discriminator = m.group(1), m.group(2)
                member_id = None
            # Verificando se o member fornecido é um ID (somente números de 0-9)
            elif member.isdecimal():
                member_name, member_discriminator = None, None
                member_id = int(member)
            # Nenhum dos 2 casos anteriores
            else:
                embed = discord.Embed(
                    color = discord.Color(0xff0000),
                    timestamp = datetime.utcnow(),
                    description = "**Sintaxe incorreta! Use !unban <name#discriminator/id>**"
                )

                embed.set_footer(icon_url='{}'.format(ctx.message.author.avatar_url_as(format=None, static_format='png')).split("?")[0], text="Gerado por {0}".format(ctx.message.author.name))
                await ctx.reply(embed=embed)
                # return para não executar o resto da função
                return

            # Percorrendo a lista de banidos
            for ban_entry in banned_users:
                user = ban_entry.user

                # Verificando com o nome e discriminator
                if (user.name, user.discriminator) == (member_name, member_discriminator):
                    # Desbanindo o usuário se um nome e discriminator igual for encontrado
                    await ctx.guild.unban(user)

                    embed = discord.Embed(
                        color = discord.Color(0x1FD358),
                        timestamp = datetime.utcnow(),
                        description = "<@!{}> foi desbanido!".format(user.id)
                    )

                    embed.set_footer(icon_url='{}'.format(ctx.message.author.avatar_url_as(format=None, static_format='png')).split("?")[0], text="Desbanido por {0}".format(ctx.message.author.name))
                    await ctx.reply(embed=embed)
                    # Encerra o loop
                    break
                # Verificando com o ID
                elif user.id == member_id:
                    # Desbanindo o usuário se um ID igual for encontrado
                    await ctx.guild.unban(user)

                    embed = discord.Embed(
                        color = discord.Color(0x1FD358),
                        timestamp = datetime.utcnow(),
                        description = "<@!{}> foi desbanido!".format(user.id)
                    )

                    embed.set_footer(icon_url='{}'.format(ctx.message.author.avatar_url_as(format=None, static_format='png')).split("?")[0], text="Desbanido por {0}".format(ctx.message.author.name))
                    await ctx.reply(embed=embed)
                    # Encerra o loop
                    break
            # Se cair no else, significa que nenhum membro foi desbanido
            else:
                embed = discord.Embed(
                    color = discord.Color(0xff0000),
                    timestamp = datetime.utcnow(),
                    description = "**Usuário não existe ou não está na lista de banimentos!**"
                )

                embed.set_footer(icon_url='{}'.format(ctx.message.author.avatar_url_as(format=None, static_format='png')).split("?")[0], text="Gerado por {0}".format(ctx.message.author.name))
                await ctx.reply(embed=embed)
        else:
            embed = discord.Embed(
                color = discord.Color(0xff0000),
                timestamp = datetime.utcnow(),
                description = "**Preciso de um usuário pra desbanir! <a:rikkaBongo:697839129257312286>**"
            )

            embed.set_footer(icon_url='{}'.format(ctx.message.author.avatar_url_as(format=None, static_format='png')).split("?")[0], text="Gerado por {0}".format(ctx.message.author.name))
            await ctx.reply(embed=embed)

    # Checking if arguments are valid
    @unban.error
    async def unban_error(self, ctx, error):
        if isinstance(error, commands.MissingPermissions):
            embed = discord.Embed(
                color = discord.Color(0xff0000),
                timestamp = datetime.utcnow(),
                description = "**Você não possui permissão para desbanir!**"
            )

            embed.set_footer(icon_url='{}'.format(ctx.message.author.avatar_url_as(format=None, static_format='png')).split("?")[0], text="Gerado por {0}".format(ctx.message.author.name))
            await ctx.reply(embed=embed)


    # !banlist - displays banlist
    @commands.command(description="Display banlist")
    @commands.has_permissions(administrator=True)
    async def banlist(self, ctx):
        banned_users = await ctx.guild.bans()

        if len(banned_users) == 0:
            embed = discord.Embed(
                color = discord.Color(0xD65F27),
                timestamp = datetime.utcnow(),
                title = "Usuários Banidos",
                description = "**Nenhum usuário foi banido ainda!**"
            )
        else:
            embed = discord.Embed(
                color = discord.Color(0xD65F27),
                timestamp = datetime.utcnow(),
                title = "Usuários Banidos"
            )

        embed.set_thumbnail(url='https://media1.tenor.com/images/d5b357ce7362ca918a14db90a9a7f277/tenor.gif?itemid=18032514')
        embed.set_footer(icon_url='{}'.format(ctx.message.author.avatar_url_as(format=None, static_format='png')).split("?")[0], text="Gerado por {0}".format(ctx.message.author.name))

        for ban_entry in banned_users:
            user = ban_entry.user
            reason = ban_entry.reason

            if reason == None:
                reason = "Sem motivo informado"

            embed.add_field(name="{} ({})".format(user, user.id), value="**Motivo: **{}".format(reason), inline=False)

        await ctx.reply(embed=embed)

    # Checking if arguments are valid
    @banlist.error
    async def banlist_error(self, ctx, error):
        if isinstance(error, commands.MissingPermissions):
            embed = discord.Embed(
                color = discord.Color(0xff0000),
                timestamp = datetime.utcnow(),
                description = "**Você não possui permissão para acessar a Lista de Banidos!**"
            )
            
            embed.set_footer(icon_url='{}'.format(ctx.message.author.avatar_url_as(format=None, static_format='png')).split("?")[0], text="Gerado por {0}".format(ctx.message.author.name))
            await ctx.reply(embed=embed)


    # !all - mention everyone
    @commands.command(description="Mention @everyone")
    @commands.has_permissions(administrator=True)
    async def all(self, ctx):
        # deleting user's message
        await ctx.message.delete()
        await ctx.send("@everyone")

    # Checking if arguments are valid
    @all.error
    async def all_error(self, ctx, error):
        if isinstance(error, commands.MissingPermissions):
            embed = discord.Embed(
                color = discord.Color(0xff0000),
                timestamp = datetime.utcnow(),
                description = "**Você não possui permissão para mencionar @everyone!**"
            )

            embed.set_footer(icon_url='{}'.format(ctx.message.author.avatar_url_as(format=None, static_format='png')).split("?")[0], text="Gerado por {0}".format(ctx.message.author.name))
            await ctx.reply(embed=embed)


def setup(client):
    client.add_cog(Admin(client))
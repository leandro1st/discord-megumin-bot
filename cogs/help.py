from collections import OrderedDict
import discord
from discord.ext import commands
from datetime import datetime

class Help(commands.Cog, name="Help"):
    """Help"""


    def __init__(self, client):
        self.client = client


    # !help - help command
    @commands.command(description="Help")
    async def help(self, ctx):
        # Descrição do embed
        descricao = ""

        # Dictionary sorted by key -> OrderedDict(sorted(self.client.cogs.items()) also works
        # Sorting by cog name
        sorted_cogs = OrderedDict(sorted(self.client.cogs.items(), key=lambda t: t[0].lower()))

        # Percorrendo todos os cogs que foram carregados
        for cog in sorted_cogs:
            # "Escondendo" o cog eventos e help
            if (cog == "Eventos") or (cog == "Help"):
                continue
            else:
                # Nome do cog e sua descrição
                descricao += "**__{}__**\n*{}*\n\n".format(cog, self.client.get_cog(cog).description)

                # Sorting list by object attribute (name)
                sorted_commands = sorted(self.client.get_cog(cog).get_commands(), key=lambda x: x.name.lower())

                # Exibindo todos os comandos de determinado cog
                for command in sorted_commands:
                    # Se o comando apresentar argumentos
                    # Mostra o prefixo, nome do comando, argumentos definidos em usage de cada comando e a descrição
                    if command.usage:
                        descricao += "`{}{} {}`\n{}\n".format(self.client.command_prefix, command, command.usage, command.description)
                    else:
                        descricao += "`{}{}`\n{}\n".format(self.client.command_prefix, command, command.description)
                        
                    # Se o comando tiver apelidos
                    if len(command.aliases) > 0:
                        descricao += "**Aliases: **{}\n\n".format(", ".join(command.aliases))
                    else:
                        descricao += "\n"

        embed = discord.Embed(
            color = discord.Color.green(),
            timestamp = datetime.utcnow(),
            description = descricao
        )  

        # .split("?")[0] to avoid image resizing
        embed.set_author(name="Megumin's Commands", icon_url='{}'.format(self.client.user.avatar_url_as(format=None, static_format='png')).split("?")[0])
        embed.set_footer(icon_url='{}'.format(ctx.message.author.avatar_url_as(format=None, static_format='png')).split("?")[0], text="Gerado por {0}".format(ctx.message.author.name))
        embed.set_thumbnail(url='https://media1.tenor.com/images/abb2dd90f2d5b836e78ebc9c1f544a09/tenor.gif?itemid=18015941')
        await ctx.reply(embed=embed)


def setup(client):
    client.add_cog(Help(client))
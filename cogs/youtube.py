import asyncio
import discord
from discord.errors import ClientException
from discord.ext import commands
from datetime import datetime
from youtube_dl.utils import DownloadError
from outros.youtube_basic import *

class Youtube(commands.Cog, name="YouTube"):
    """Comandos para usar o YouTube"""


    def __init__(self, client):
        self.client = client


    # !yt - plays a song from youtube
    @commands.command(usage="<url/search query>", description="Play a song")
    async def yt(self, ctx, *, url):
        # Bot can play only 1 song at a time
        try:
            if ctx.author.voice is not None:
                channel = ctx.author.voice.channel
                # Connecting the bot if its not connected to a voice channel
                if ctx.voice_client is None:
                    await channel.connect()
                # Moving the bot if already in some vc
                else:
                    await ctx.voice_client.move_to(channel)
                    
                player = await YTDLSource.from_url(url, stream=True)
                ctx.voice_client.play(player, after=lambda e: print('Player error: %s' % e) if e else None)

                # reacting with catJAM
                await ctx.message.add_reaction('<a:catJAM:841531588298145812>')

                embed = discord.Embed(
                    color = discord.Color(0xf8ff1f),
                    timestamp = datetime.utcnow(),
                    title = player.title,
                    url = "https://www.youtube.com/watch?v={}".format(player.data['id']),
                    description = 'Now playing: **{}**'.format(player.title)
                )

                embed.set_footer(icon_url='{}'.format(ctx.message.author.avatar_url_as(format=None, static_format='png')).split("?")[0], text="Gerado por {0}".format(ctx.message.author.name))
                await ctx.reply(embed=embed)
            else:
                embed = discord.Embed(
                    color = discord.Color(0xff0000),
                    timestamp = datetime.utcnow(),
                    description = "**You're not connected to a voice channel!**"
                )

                embed.set_footer(icon_url='{}'.format(ctx.message.author.avatar_url_as(format=None, static_format='png')).split("?")[0], text="Gerado por {0}".format(ctx.message.author.name))
                await ctx.reply(embed=embed)
        # If bot is already playing audio
        except ClientException as e:
            embed = discord.Embed(
                color = discord.Color(0xff0000),
                timestamp = datetime.utcnow(),
                description = "**{}**".format(e)
            )

            embed.set_footer(icon_url='{}'.format(ctx.message.author.avatar_url_as(format=None, static_format='png')).split("?")[0], text="Gerado por {0}".format(ctx.message.author.name))
            await ctx.reply(embed=embed)
        # If no results are found
        except IndexError:
            embed = discord.Embed(
                color = discord.Color(0xff0000),
                timestamp = datetime.utcnow(),
                description = "**No results found!**"
            )

            embed.set_footer(icon_url='{}'.format(ctx.message.author.avatar_url_as(format=None, static_format='png')).split("?")[0], text="Gerado por {0}".format(ctx.message.author.name))
            await ctx.reply(embed=embed)
        # Incorrect YouTube URL or Unsupported URL
        except DownloadError as e:
            embed = discord.Embed(
                color = discord.Color(0xff0000),
                timestamp = datetime.utcnow(),
                description = "**{}**".format(e)
            )

            embed.set_footer(icon_url='{}'.format(ctx.message.author.avatar_url_as(format=None, static_format='png')).split("?")[0], text="Gerado por {0}".format(ctx.message.author.name))
            await ctx.reply(embed=embed)

    # Checking if arguments are valid
    @yt.error
    async def yt_error(self, ctx, error):
        if isinstance(error, commands.MissingRequiredArgument):
            embed = discord.Embed(
                color = discord.Color(0xff0000),
                timestamp = datetime.utcnow(),
                description = "**Sintaxe incorreta! Use !yt <url/search query>**"
            )

            embed.set_footer(icon_url='{}'.format(ctx.message.author.avatar_url_as(format=None, static_format='png')).split("?")[0], text="Gerado por {0}".format(ctx.message.author.name))
            await ctx.reply(embed=embed)


    # Evento para o bot desconectar do canal de voz
    @commands.Cog.listener()
    async def on_voice_state_update(self, member, before, after):
        voice_state = member.guild.voice_client

        # Checking if the bot is connected to a channel and if there is only 1 member connected to it (the bot itself)
        if voice_state is not None and len(voice_state.channel.members) == 1:
            # Sleeping for 45 seconds
            await asyncio.sleep(45)

            # Checking again if the bot is connected to a channel and if there is only 1 member connected to it (the bot itself)
            if voice_state is not None and len(voice_state.channel.members) == 1:
                # Disconnecting
                await voice_state.disconnect()

                embed = discord.Embed(
                    color = discord.Color(0xff0000),
                    timestamp = datetime.utcnow(),
                    description = "Desconectando de <#{}> por inatividade...".format(voice_state.channel.id)
                )

                embed.set_footer(icon_url='{}'.format(self.client.user.avatar_url_as(format=None, static_format='png')).split("?")[0], text="Gerado por {0}".format(self.client.user.name))

                # Sending message about disconnection
                await self.client.get_channel(695739459848896533).send(embed=embed)


    # !volume - adjusts song's volume
    @commands.command(usage="<int>", description="Set new volume")
    async def volume(self, ctx, volume: int):
        # User can only use this command if connected to a vc
        if ctx.author.voice is not None:
            # Only adjusts the volume if bot is connected to a voice channel
            if ctx.voice_client is None:
                embed = discord.Embed(
                    color = discord.Color(0xff0000),
                    timestamp = datetime.utcnow(),
                    description = "**I'm not connected to a voice channel!**"
                )

                embed.set_footer(icon_url='{}'.format(ctx.message.author.avatar_url_as(format=None, static_format='png')).split("?")[0], text="Gerado por {0}".format(ctx.message.author.name))
                await ctx.reply(embed=embed)
            else:
                # User can only use this command if connected to the same vc as the bot
                if ctx.author.voice.channel == ctx.voice_client.channel:
                    # Volume cant exceed 200%
                    if volume <= 200:
                        # if volume is a negative value, set to 0
                        if volume < 0:
                            volume = 0

                        ctx.voice_client.source.volume = volume / 100
                
                        embed = discord.Embed(
                            color = discord.Color(0xffc01f),
                            timestamp = datetime.utcnow(),
                            description = "Changed volume to {}%".format(volume)
                        )

                        embed.set_footer(icon_url='{}'.format(ctx.message.author.avatar_url_as(format=None, static_format='png')).split("?")[0], text="Gerado por {0}".format(ctx.message.author.name))
                        await ctx.reply(embed=embed)
                    else:
                        embed = discord.Embed(
                            color = discord.Color(0xff0000),
                            timestamp = datetime.utcnow(),
                            description = '**The limit is 200%!**'
                        )

                        embed.set_footer(icon_url='{}'.format(ctx.message.author.avatar_url_as(format=None, static_format='png')).split("?")[0], text="Gerado por {0}".format(ctx.message.author.name))
                        await ctx.reply(embed=embed)
                else:
                    embed = discord.Embed(
                        color = discord.Color(0xff0000),
                        timestamp = datetime.utcnow(),
                        description = "**You're not connected to the same voice channel as me!**"
                    )

                    embed.set_footer(icon_url='{}'.format(ctx.message.author.avatar_url_as(format=None, static_format='png')).split("?")[0], text="Gerado por {0}".format(ctx.message.author.name))
                    await ctx.reply(embed=embed)
        else:
            embed = discord.Embed(
                color = discord.Color(0xff0000),
                timestamp = datetime.utcnow(),
                description = "**You're not connected to a voice channel!**"
            )

            embed.set_footer(icon_url='{}'.format(ctx.message.author.avatar_url_as(format=None, static_format='png')).split("?")[0], text="Gerado por {0}".format(ctx.message.author.name))
            await ctx.reply(embed=embed)

    # Checking if arguments are valid
    @volume.error
    async def volume_error(self, ctx, error):
        if isinstance(error, commands.BadArgument):
            embed = discord.Embed(
                color = discord.Color(0xff0000),
                timestamp = datetime.utcnow(),
                description = "**Use um valor inteiro!**"
            )

            embed.set_footer(icon_url='{}'.format(ctx.message.author.avatar_url_as(format=None, static_format='png')).split("?")[0], text="Gerado por {0}".format(ctx.message.author.name))
            await ctx.reply(embed=embed)
        elif isinstance(error, commands.MissingRequiredArgument):
            embed = discord.Embed(
                color = discord.Color(0xff0000),
                timestamp = datetime.utcnow(),
                description = "**Sintaxe incorreta! Use !volume <int>**"
            )

            embed.set_footer(icon_url='{}'.format(ctx.message.author.avatar_url_as(format=None, static_format='png')).split("?")[0], text="Gerado por {0}".format(ctx.message.author.name))
            await ctx.reply(embed=embed)


    # !stop - stops song and disconnect bot from voice channel
    @commands.command(description="Stop the current playing song")
    async def stop(self, ctx):
        # User can only use this command if connected to a vc
        if ctx.author.voice is not None:
            # Only disconnects if bot is connected to a voice channel
            if ctx.voice_client is None:
                embed = discord.Embed(
                    color = discord.Color(0xff0000),
                    timestamp = datetime.utcnow(),
                    description = "**I'm not connected to a voice channel!**"
                )

                embed.set_footer(icon_url='{}'.format(ctx.message.author.avatar_url_as(format=None, static_format='png')).split("?")[0], text="Gerado por {0}".format(ctx.message.author.name))
                await ctx.reply(embed=embed)
            else:
                # User can only use this command if connected to the same vc as the bot
                if ctx.author.voice.channel == ctx.voice_client.channel:
                    # Disconnecting and reacting users message
                    await ctx.voice_client.disconnect()
                    await ctx.message.add_reaction('<:peepoSad:695438016633634877>')
                else:
                    embed = discord.Embed(
                        color = discord.Color(0xff0000),
                        timestamp = datetime.utcnow(),
                        description = "**You're not connected to the same voice channel as me!**"
                    )

                    embed.set_footer(icon_url='{}'.format(ctx.message.author.avatar_url_as(format=None, static_format='png')).split("?")[0], text="Gerado por {0}".format(ctx.message.author.name))
                    await ctx.reply(embed=embed)
        else:
            embed = discord.Embed(
                color = discord.Color(0xff0000),
                timestamp = datetime.utcnow(),
                description = "**You're not connected to a voice channel!**"
            )

            embed.set_footer(icon_url='{}'.format(ctx.message.author.avatar_url_as(format=None, static_format='png')).split("?")[0], text="Gerado por {0}".format(ctx.message.author.name))
            await ctx.reply(embed=embed)


def setup(client):
    client.add_cog(Youtube(client))
import discord
from discord.ext import commands
from datetime import datetime, timezone
import random as r
from pytz import timezone #timezone()
import re
import requests
from saucenao_api import SauceNao, VideoSauce, BookSauce
import tweepy
from os import environ


# Authenticate to Twitter
auth = tweepy.OAuthHandler(environ.get('consumer_key'), environ.get('consumer_secret'))
auth.set_access_token(environ.get('access_token'), environ.get('access_token_secret'))

# Create API object
api = tweepy.API(auth)

# Replace the key with your own
sauce = SauceNao(environ.get('SauceNao_key'))
sauce2 = SauceNao(environ.get('SauceNao_key2'))


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

    
    # Method that is going to search for sauce
    async def search_sauce(self, ctx, url):
        # If url is from Twitter
        if re.compile('^https?:\/\/twitter\.com\/(?:#!\/)?(\w+)\/status(es)?\/(\d+)').search(url):
            # Getting tweet id  
            id = re.search('/status/(\d+)', url).group(1)
            status = api.get_status(id, tweet_mode='extended')

            # If an image/video is included on the tweet
            if 'media' in status.entities:
                # Getting only first image
                url_twitter = status.extended_entities['media'][0]['media_url_https']
                # Results
                results = sauce.from_url(url_twitter)
            # No media
            else:
                embed = discord.Embed(
                    color = discord.Color(0xff0000),
                    timestamp = datetime.utcnow(),
                    description = "**There is nothing to search for!**"
                )

                embed.set_footer(icon_url='{}'.format(ctx.message.author.avatar_url_as(format=None, static_format='png')).split("?")[0], text="Gerado por {0}".format(ctx.message.author.name))
                await ctx.reply(embed=embed)

                # return to stop the execution of the method
                return
        # Other links
        else:
            # Trying to find the source
            try:
                # Results
                results = sauce.from_url(url)
            # No media
            except Exception as ex:
                embed = discord.Embed(
                    color = discord.Color(0xff0000),
                    timestamp = datetime.utcnow(),
                    description = "**There is nothing to search for!**"
                )

                embed.set_footer(icon_url='{}'.format(ctx.message.author.avatar_url_as(format=None, static_format='png')).split("?")[0], text="Gerado por {0}".format(ctx.message.author.name))
                await ctx.reply(embed=embed)

                # return to stop the execution of the method
                return

        # Getting the source with highest similarity
        best = results[0]

        # Embed
        embed = discord.Embed(
            color = discord.Color(0xffc338),
            timestamp = datetime.utcnow(),
            title = best.title
        )

        # Similarity
        embed.add_field(name="Similarity".format(), value="{}%".format(best.similarity), inline=True)

        # Author
        if best.author:
            embed.add_field(name="Author".format(), value="{}".format(best.author), inline=True)
        else:
            embed.add_field(name="Author".format(), value="–", inline=True)

        # Material
        if 'material' in best.raw['data']:
            if best.raw['data']['material']:
                embed.add_field(name="Material", value="{}".format(best.raw['data']['material']), inline=False)

        # Characters
        if 'characters' in best.raw['data']:
            if best.raw['data']['characters']:
                embed.add_field(name="Characters", value="{}".format(best.raw['data']['characters']), inline=False)

        # If source is from an anime
        if isinstance(best, VideoSauce):
            # Part/episode
            if 'part' in best.raw['data']:
                if best.raw['data']['part']:
                    embed.add_field(name="Episode", value="{}".format(best.raw['data']['part']), inline=False)
            # Year
            if 'year' in best.raw['data']:
                if best.raw['data']['year']:
                    embed.add_field(name="Year", value="{}".format(best.raw['data']['year']), inline=False)
            # Estimated time
            if 'est_time' in best.raw['data']:
                if best.raw['data']['est_time']:
                    embed.add_field(name="Est Time", value="{}".format(best.raw['data']['est_time']), inline=False)
        # If source is from a book
        elif isinstance(best, BookSauce):
            # Part/volume
            if 'part' in best.raw['data']:
                if best.raw['data']['part']:
                    embed.add_field(name="Part", value="{}".format(best.raw['data']['part']), inline=False)            

        # Source
        if 'source' in best.raw['data']:
            if best.raw['data']['source']:
                # Pixiv link because https://i.pximg.net is 'broken'
                if re.compile('^https:\/\/i\.pximg\.net').search(best.raw['data']['source']):
                    embed.add_field(name="Source", value='https://www.pixiv.net/en/artworks/' + best.raw['data']['source'].split('/')[-1], inline=False)
                # Other links
                else:
                    embed.add_field(name="Source", value=best.raw['data']['source'], inline=False)

        # Links
        for count, link in enumerate(best.urls, start=1):
            embed.add_field(name="Link {}".format(count), value="{}".format(link), inline=False)

        # Thumbnail
        embed.set_thumbnail(url='{}'.format(best.thumbnail))
        embed.set_footer(icon_url='{}'.format(ctx.message.author.avatar_url_as(format=None, static_format='png')).split("?")[0], text="Gerado por {0}".format(ctx.message.author.name))
        await ctx.reply(embed=embed)


    # !sauce (url) - search for sauce
    @commands.command(usage="(url)", description="Search for sauce (You can also get the sauce by uploading an image or replying to a message)")
    async def sauce(self, ctx, url = None):
        # If an URL is passed
        if url:
            await self.search_sauce(ctx, url)
        # No URL
        else:
            # If user wanna find out the source of an image from their pc
            if ctx.message.attachments:
                await self.search_sauce(ctx, ctx.message.attachments[0].url)
                # await ctx.reply(ctx.message.attachments[0].url)
            # If user wanna find out the source from a reply
            elif ctx.message.reference:
                # Original message
                message = await ctx.fetch_message(ctx.message.reference.message_id)

                # Image uploaded by an user
                if message.attachments:
                    await self.search_sauce(ctx, message.attachments[0].url)
                    # await ctx.reply(message.attachments[0].url)
                # Preview image from an URL
                elif message.embeds:
                    # Embed with an image
                    if message.embeds[0].image.url:
                        await self.search_sauce(ctx, message.embeds[0].image.url)
                        # await ctx.reply(message.embeds[0].image.url)
                    # Embed with a thumbnail image
                    elif message.embeds[0].thumbnail.url:
                        await self.search_sauce(ctx, message.embeds[0].thumbnail.url)
                        # await ctx.reply(message.embeds[0].thumbnail.url)
                    # Embed with no image
                    else:
                        embed = discord.Embed(
                            color = discord.Color(0xff0000),
                            timestamp = datetime.utcnow(),
                            description = "**Reply to a message that contains an image!**"
                        )

                        embed.set_footer(icon_url='{}'.format(ctx.message.author.avatar_url_as(format=None, static_format='png')).split("?")[0], text="Gerado por {0}".format(ctx.message.author.name))
                        await ctx.reply(embed=embed)
                # No image
                else:
                    embed = discord.Embed(
                        color = discord.Color(0xff0000),
                        timestamp = datetime.utcnow(),
                        description = "**Reply to a message that contains an image!**"
                    )

                    embed.set_footer(icon_url='{}'.format(ctx.message.author.avatar_url_as(format=None, static_format='png')).split("?")[0], text="Gerado por {0}".format(ctx.message.author.name))
                    await ctx.reply(embed=embed)
            # When user types only "!sauce"
            else:
                embed = discord.Embed(
                    color = discord.Color(0xff0000),
                    timestamp = datetime.utcnow(),
                    description = "**There is nothing to search for!**"
                )

                embed.set_footer(icon_url='{}'.format(ctx.message.author.avatar_url_as(format=None, static_format='png')).split("?")[0], text="Gerado por {0}".format(ctx.message.author.name))
                await ctx.reply(embed=embed)


    # Checking if arguments are valid
    @sauce.error
    async def sauce_error(self, ctx, error):
        embed = discord.Embed(
            color = discord.Color(0xff0000),
            timestamp = datetime.utcnow(),
            description = "**{}**".format(error)
        )

        embed.set_footer(icon_url='{}'.format(ctx.message.author.avatar_url_as(format=None, static_format='png')).split("?")[0], text="Gerado por {0}".format(ctx.message.author.name))
        await ctx.reply(embed=embed)


    # !junior - display junior's pic
    @commands.command(description="Junior zuado")
    async def teste(self, ctx):
        embed = discord.Embed(
            color = discord.Color.gold(),
            timestamp = datetime.utcnow()
        )

        embed.set_image(url='https://gekinetu.com/wp-content/uploads/2021/07/img_1625613824-300x150.png')
        embed.set_thumbnail(url='https://static.wikia.nocookie.net/rezero/images/c/cc/Emilia_-_Re_Zero_Anime_BD_-_13.png/revision/latest/scale-to-width-down/1000?cb=20160915153714')
        embed.set_footer(icon_url='{}'.format(ctx.message.author.avatar_url_as(format=None, static_format='png')).split("?")[0], text="Gerado por {0}".format(ctx.message.author.name))
        message = await ctx.reply(embed=embed)


def setup(client):
    client.add_cog(Outros(client))
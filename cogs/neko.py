import discord
from discord.ext import commands
from datetime import datetime
import random as r
import nekos # https://github.com/Nekos-life/nekos.py/blob/master/nekos/nekos.py

class Neko(commands.Cog, name="owo"):
    """Comandos para interação"""


    def __init__(self, client):
        self.client = client


    # !waifu - pick a random user as a waifu
    @commands.command(usage="(optional member)", description="Display user's waifu from server")
    async def waifu(self, ctx, member: discord.Member = None):
        # If member name is given
        if member:
            embed = discord.Embed(
                color = discord.Color(0x45e0ff),
                timestamp = datetime.utcnow(),
                description = "<@!{}> é a waifu de <@!{}>".format(member.id, ctx.message.author.id)
            )

            embed.set_image(url='{}'.format(member.avatar_url_as(format=None, static_format='png', size=4096)))
            embed.set_footer(icon_url='{}'.format(ctx.message.author.avatar_url_as(format=None, static_format='png')).split("?")[0], text="Gerado por {0}".format(ctx.message.author.name))
            await ctx.reply(embed=embed)
        else:
            member = r.choice(ctx.guild.members)

            embed = discord.Embed(
                color = discord.Color(0x45e0ff),
                timestamp = datetime.utcnow(),
                description = "<@!{}> é a waifu de <@!{}>".format(member.id, ctx.message.author.id)
            )

            embed.set_image(url='{}'.format(member.avatar_url_as(format=None, static_format='png', size=4096)))
            embed.set_footer(icon_url='{}'.format(ctx.message.author.avatar_url_as(format=None, static_format='png')).split("?")[0], text="Gerado por {0}".format(ctx.message.author.name))
            await ctx.reply(embed=embed)

    # Checking if arguments are valid
    @waifu.error
    async def waifu_error(self, ctx, error):
        if isinstance(error, commands.BadArgument):
            embed = discord.Embed(
                color = discord.Color(0xff0000),
                timestamp = datetime.utcnow(),
                description = "**Mencione um membro do canal! <a:rikkaBongo:697839129257312286>**"
            )

            embed.set_footer(icon_url='{}'.format(ctx.message.author.avatar_url_as(format=None, static_format='png')).split("?")[0], text="Gerado por {0}".format(ctx.message.author.name))
            await ctx.reply(embed=embed)


    # !pat - pat a member
    @commands.command(usage="<member>", description="Pat a member")
    async def pat(self, ctx, member: discord.Member = None):
        target = "pat"
        
        if member:
            embed = discord.Embed(
                color = discord.Color(0x45e0ff),
                timestamp = datetime.utcnow(),
                description = "<@!{}> pats <@!{}>".format(ctx.message.author.id, member.id)
            )

            embed.set_image(url=nekos.img(target))
            embed.set_footer(icon_url='{}'.format(ctx.message.author.avatar_url_as(format=None, static_format='png')).split("?")[0], text="Gerado por {0}".format(ctx.message.author.name))
            await ctx.reply(embed=embed)
        else:
            embed = discord.Embed(
                color = discord.Color(0xff0000),
                timestamp = datetime.utcnow(),
                description = "**Preciso de um usuário! <a:rikkaBongo:697839129257312286>**"
            )

            embed.set_footer(icon_url='{}'.format(ctx.message.author.avatar_url_as(format=None, static_format='png')).split("?")[0], text="Gerado por {0}".format(ctx.message.author.name))
            await ctx.reply(embed=embed)

    # Checking if arguments are valid
    @pat.error
    async def pat_error(self, ctx, error):
        if isinstance(error, commands.BadArgument):
            embed = discord.Embed(
                color = discord.Color(0xff0000),
                timestamp = datetime.utcnow(),
                description = "**Mencione um membro do canal! <a:rikkaBongo:697839129257312286>**"
            )

            embed.set_footer(icon_url='{}'.format(ctx.message.author.avatar_url_as(format=None, static_format='png')).split("?")[0], text="Gerado por {0}".format(ctx.message.author.name))
            await ctx.reply(embed=embed)


    # !poke - poke a member
    @commands.command(usage="<member>", description="Poke a member")
    async def poke(self, ctx, member: discord.Member = None):
        target = "poke"
        
        if member:
            embed = discord.Embed(
                color = discord.Color(0x45e0ff),
                timestamp = datetime.utcnow(),
                description = "<@!{}> cutuca <@!{}>".format(ctx.message.author.id, member.id)
            )

            embed.set_image(url=nekos.img(target))
            embed.set_footer(icon_url='{}'.format(ctx.message.author.avatar_url_as(format=None, static_format='png')).split("?")[0], text="Gerado por {0}".format(ctx.message.author.name))
            await ctx.reply(embed=embed)
        else:
            embed = discord.Embed(
                color = discord.Color(0xff0000),
                timestamp = datetime.utcnow(),
                description = "**Preciso de um usuário! <a:rikkaBongo:697839129257312286>**"
            )

            embed.set_footer(icon_url='{}'.format(ctx.message.author.avatar_url_as(format=None, static_format='png')).split("?")[0], text="Gerado por {0}".format(ctx.message.author.name))
            await ctx.reply(embed=embed)

    # Checking if arguments are valid
    @poke.error
    async def poke_error(self, ctx, error):
        if isinstance(error, commands.BadArgument):
            embed = discord.Embed(
                color = discord.Color(0xff0000),
                timestamp = datetime.utcnow(),
                description = "**Mencione um membro do canal! <a:rikkaBongo:697839129257312286>**"
            )

            embed.set_footer(icon_url='{}'.format(ctx.message.author.avatar_url_as(format=None, static_format='png')).split("?")[0], text="Gerado por {0}".format(ctx.message.author.name))
            await ctx.reply(embed=embed)


    # !kiss - kiss a member
    @commands.command(usage="<member>", description="Kiss a member")
    async def kiss(self, ctx, member: discord.Member = None):
        target = "kiss"
        
        if member:
            embed = discord.Embed(
                color = discord.Color(0x45e0ff),
                timestamp = datetime.utcnow(),
                description = "<@!{}> beija <@!{}>".format(ctx.message.author.id, member.id)
            )

            embed.set_image(url=nekos.img(target))
            embed.set_footer(icon_url='{}'.format(ctx.message.author.avatar_url_as(format=None, static_format='png')).split("?")[0], text="Gerado por {0}".format(ctx.message.author.name))
            await ctx.reply(embed=embed)
        else:
            embed = discord.Embed(
                color = discord.Color(0xff0000),
                timestamp = datetime.utcnow(),
                description = "**Preciso de um usuário! <a:rikkaBongo:697839129257312286>**"
            )

            embed.set_footer(icon_url='{}'.format(ctx.message.author.avatar_url_as(format=None, static_format='png')).split("?")[0], text="Gerado por {0}".format(ctx.message.author.name))
            await ctx.reply(embed=embed)

    # Checking if arguments are valid
    @kiss.error
    async def kiss_error(self, ctx, error):
        if isinstance(error, commands.BadArgument):
            embed = discord.Embed(
                color = discord.Color(0xff0000),
                timestamp = datetime.utcnow(),
                description = "**Mencione um membro do canal! <a:rikkaBongo:697839129257312286>**"
            )

            embed.set_footer(icon_url='{}'.format(ctx.message.author.avatar_url_as(format=None, static_format='png')).split("?")[0], text="Gerado por {0}".format(ctx.message.author.name))
            await ctx.reply(embed=embed)


    # !neko - some random neko pic
    @commands.command(description="Random neko")
    async def neko(self, ctx):
        target = "neko"
        
        embed = discord.Embed(
            color = discord.Color(0x45e0ff),
            timestamp = datetime.utcnow(),
        )

        embed.set_image(url=nekos.img(target))
        embed.set_footer(icon_url='{}'.format(ctx.message.author.avatar_url_as(format=None, static_format='png')).split("?")[0], text="Gerado por {0}".format(ctx.message.author.name))
        await ctx.reply(embed=embed)


    # !foxgirl - some random foxgirl pic
    @commands.command(description="Random foxgirl")
    async def foxgirl(self, ctx):
        target = "fox_girl"
        
        embed = discord.Embed(
            color = discord.Color(0x45e0ff),
            timestamp = datetime.utcnow(),
        )

        embed.set_image(url=nekos.img(target))
        embed.set_footer(icon_url='{}'.format(ctx.message.author.avatar_url_as(format=None, static_format='png')).split("?")[0], text="Gerado por {0}".format(ctx.message.author.name))
        await ctx.reply(embed=embed)


    # !baka - b-baka
    @commands.command(usage="<member>", description="B-baka")
    async def baka(self, ctx, member: discord.Member = None):
        target = "baka"
        
        if member:
            embed = discord.Embed(
                color = discord.Color(0x45e0ff),
                timestamp = datetime.utcnow(),
                description = "<@!{}>, b-baka!".format(member.id)
            )

            embed.set_image(url=nekos.img(target))
            embed.set_footer(icon_url='{}'.format(ctx.message.author.avatar_url_as(format=None, static_format='png')).split("?")[0], text="Gerado por {0}".format(ctx.message.author.name))
            await ctx.reply(embed=embed)
        else:
            embed = discord.Embed(
                color = discord.Color(0xff0000),
                timestamp = datetime.utcnow(),
                description = "**Preciso de um usuário! <a:rikkaBongo:697839129257312286>**"
            )

            embed.set_footer(icon_url='{}'.format(ctx.message.author.avatar_url_as(format=None, static_format='png')).split("?")[0], text="Gerado por {0}".format(ctx.message.author.name))
            await ctx.reply(embed=embed)

    # Checking if arguments are valid
    @baka.error
    async def baka_error(self, ctx, error):
        if isinstance(error, commands.BadArgument):
            embed = discord.Embed(
                color = discord.Color(0xff0000),
                timestamp = datetime.utcnow(),
                description = "**Mencione um membro do canal! <a:rikkaBongo:697839129257312286>**"
            )

            embed.set_footer(icon_url='{}'.format(ctx.message.author.avatar_url_as(format=None, static_format='png')).split("?")[0], text="Gerado por {0}".format(ctx.message.author.name))
            await ctx.reply(embed=embed)


    # !hug - hug a member
    @commands.command(usage="<member>", description="Hug a member")
    async def hug(self, ctx, member: discord.Member = None):
        target = "hug"
        
        if member:
            embed = discord.Embed(
                color = discord.Color(0x45e0ff),
                timestamp = datetime.utcnow(),
                description = "<@!{}> hugs <@!{}>".format(ctx.message.author.id, member.id)
            )

            embed.set_image(url=nekos.img(target))
            embed.set_footer(icon_url='{}'.format(ctx.message.author.avatar_url_as(format=None, static_format='png')).split("?")[0], text="Gerado por {0}".format(ctx.message.author.name))
            await ctx.reply(embed=embed)
        else:
            embed = discord.Embed(
                color = discord.Color(0xff0000),
                timestamp = datetime.utcnow(),
                description = "**Preciso de um usuário! <a:rikkaBongo:697839129257312286>**"
            )

            embed.set_footer(icon_url='{}'.format(ctx.message.author.avatar_url_as(format=None, static_format='png')).split("?")[0], text="Gerado por {0}".format(ctx.message.author.name))
            await ctx.reply(embed=embed)

    # Checking if arguments are valid
    @hug.error
    async def hug_error(self, ctx, error):
        if isinstance(error, commands.BadArgument):
            embed = discord.Embed(
                color = discord.Color(0xff0000),
                timestamp = datetime.utcnow(),
                description = "**Mencione um membro do canal! <a:rikkaBongo:697839129257312286>**"
            )

            embed.set_footer(icon_url='{}'.format(ctx.message.author.avatar_url_as(format=None, static_format='png')).split("?")[0], text="Gerado por {0}".format(ctx.message.author.name))
            await ctx.reply(embed=embed)


    # !cuddle - cuddle a member
    @commands.command(usage="<member>", description="Cuddle a member")
    async def cuddle(self, ctx, member: discord.Member = None):
        target = "cuddle"
        
        if member:
            embed = discord.Embed(
                color = discord.Color(0x45e0ff),
                timestamp = datetime.utcnow(),
                description = "<@!{}> cuddles <@!{}>".format(ctx.message.author.id, member.id)
            )

            embed.set_image(url=nekos.img(target))
            embed.set_footer(icon_url='{}'.format(ctx.message.author.avatar_url_as(format=None, static_format='png')).split("?")[0], text="Gerado por {0}".format(ctx.message.author.name))
            await ctx.reply(embed=embed)
        else:
            embed = discord.Embed(
                color = discord.Color(0xff0000),
                timestamp = datetime.utcnow(),
                description = "**Preciso de um usuário! <a:rikkaBongo:697839129257312286>**"
            )

            embed.set_footer(icon_url='{}'.format(ctx.message.author.avatar_url_as(format=None, static_format='png')).split("?")[0], text="Gerado por {0}".format(ctx.message.author.name))
            await ctx.reply(embed=embed)

    # Checking if arguments are valid
    @cuddle.error
    async def cuddle_error(self, ctx, error):
        if isinstance(error, commands.BadArgument):
            embed = discord.Embed(
                color = discord.Color(0xff0000),
                timestamp = datetime.utcnow(),
                description = "**Mencione um membro do canal! <a:rikkaBongo:697839129257312286>**"
            )

            embed.set_footer(icon_url='{}'.format(ctx.message.author.avatar_url_as(format=None, static_format='png')).split("?")[0], text="Gerado por {0}".format(ctx.message.author.name))
            await ctx.reply(embed=embed)


    # !slap - slap a member
    @commands.command(usage="<member>", description="Slap a member")
    async def slap(self, ctx, member: discord.Member = None):
        target = "slap"
        
        if member:
            embed = discord.Embed(
                color = discord.Color(0x45e0ff),
                timestamp = datetime.utcnow(),
                description = "<@!{}> slaps <@!{}>".format(ctx.message.author.id, member.id)
            )

            embed.set_image(url=nekos.img(target))
            embed.set_footer(icon_url='{}'.format(ctx.message.author.avatar_url_as(format=None, static_format='png')).split("?")[0], text="Gerado por {0}".format(ctx.message.author.name))
            await ctx.reply(embed=embed)
        else:
            embed = discord.Embed(
                color = discord.Color(0xff0000),
                timestamp = datetime.utcnow(),
                description = "**Preciso de um usuário! <a:rikkaBongo:697839129257312286>**"
            )

            embed.set_footer(icon_url='{}'.format(ctx.message.author.avatar_url_as(format=None, static_format='png')).split("?")[0], text="Gerado por {0}".format(ctx.message.author.name))
            await ctx.reply(embed=embed)

    # Checking if arguments are valid
    @slap.error
    async def slap_error(self, ctx, error):
        if isinstance(error, commands.BadArgument):
            embed = discord.Embed(
                color = discord.Color(0xff0000),
                timestamp = datetime.utcnow(),
                description = "**Mencione um membro do canal! <a:rikkaBongo:697839129257312286>**"
            )

            embed.set_footer(icon_url='{}'.format(ctx.message.author.avatar_url_as(format=None, static_format='png')).split("?")[0], text="Gerado por {0}".format(ctx.message.author.name))
            await ctx.reply(embed=embed)


    # !tickle - tickle a member
    @commands.command(usage="<member>", description="Tickle a member")
    async def tickle(self, ctx, member: discord.Member = None):
        target = "tickle"
        
        if member:
            embed = discord.Embed(
                color = discord.Color(0x45e0ff),
                timestamp = datetime.utcnow(),
                description = "<@!{}> tickles <@!{}>".format(ctx.message.author.id, member.id)
            )

            embed.set_image(url=nekos.img(target))
            embed.set_footer(icon_url='{}'.format(ctx.message.author.avatar_url_as(format=None, static_format='png')).split("?")[0], text="Gerado por {0}".format(ctx.message.author.name))
            await ctx.reply(embed=embed)
        else:
            embed = discord.Embed(
                color = discord.Color(0xff0000),
                timestamp = datetime.utcnow(),
                description = "**Preciso de um usuário! <a:rikkaBongo:697839129257312286>**"
            )

            embed.set_footer(icon_url='{}'.format(ctx.message.author.avatar_url_as(format=None, static_format='png')).split("?")[0], text="Gerado por {0}".format(ctx.message.author.name))
            await ctx.reply(embed=embed)

    # Checking if arguments are valid
    @tickle.error
    async def tickle_error(self, ctx, error):
        if isinstance(error, commands.BadArgument):
            embed = discord.Embed(
                color = discord.Color(0xff0000),
                timestamp = datetime.utcnow(),
                description = "**Mencione um membro do canal! <a:rikkaBongo:697839129257312286>**"
            )

            embed.set_footer(icon_url='{}'.format(ctx.message.author.avatar_url_as(format=None, static_format='png')).split("?")[0], text="Gerado por {0}".format(ctx.message.author.name))
            await ctx.reply(embed=embed)


    # !feed - feed a member
    @commands.command(usage="<member>", description="Feed a member")
    async def feed(self, ctx, member: discord.Member = None):
        target = "feed"
        
        if member:
            embed = discord.Embed(
                color = discord.Color(0x45e0ff),
                timestamp = datetime.utcnow(),
                description = "<@!{}> feeds <@!{}>".format(ctx.message.author.id, member.id)
            )

            embed.set_image(url=nekos.img(target))
            embed.set_footer(icon_url='{}'.format(ctx.message.author.avatar_url_as(format=None, static_format='png')).split("?")[0], text="Gerado por {0}".format(ctx.message.author.name))
            await ctx.reply(embed=embed)
        else:
            embed = discord.Embed(
                color = discord.Color(0xff0000),
                timestamp = datetime.utcnow(),
                description = "**Preciso de um usuário! <a:rikkaBongo:697839129257312286>**"
            )

            embed.set_footer(icon_url='{}'.format(ctx.message.author.avatar_url_as(format=None, static_format='png')).split("?")[0], text="Gerado por {0}".format(ctx.message.author.name))
            await ctx.reply(embed=embed)

    # Checking if arguments are valid
    @feed.error
    async def feed_error(self, ctx, error):
        if isinstance(error, commands.BadArgument):
            embed = discord.Embed(
                color = discord.Color(0xff0000),
                timestamp = datetime.utcnow(),
                description = "**Mencione um membro do canal! <a:rikkaBongo:697839129257312286>**"
            )

            embed.set_footer(icon_url='{}'.format(ctx.message.author.avatar_url_as(format=None, static_format='png')).split("?")[0], text="Gerado por {0}".format(ctx.message.author.name))
            await ctx.reply(embed=embed)


    # !wallpaper - some random wallpaper
    @commands.command(description="Random wallpaper")
    async def wallpaper(self, ctx):
        target = "wallpaper"
        
        embed = discord.Embed(
            color = discord.Color(0x45e0ff),
            timestamp = datetime.utcnow(),
        )

        embed.set_image(url=nekos.img(target))
        embed.set_footer(icon_url='{}'.format(ctx.message.author.avatar_url_as(format=None, static_format='png')).split("?")[0], text="Gerado por {0}".format(ctx.message.author.name))
        await ctx.reply(embed=embed)


    # !random_avatar - some random avatar
    @commands.command(description="Random avatar")
    async def random_avatar(self, ctx):
        target = "avatar"
        
        embed = discord.Embed(
            color = discord.Color(0x45e0ff),
            timestamp = datetime.utcnow(),
        )

        embed.set_image(url=nekos.img(target))
        embed.set_footer(icon_url='{}'.format(ctx.message.author.avatar_url_as(format=None, static_format='png')).split("?")[0], text="Gerado por {0}".format(ctx.message.author.name))
        await ctx.reply(embed=embed)


    # !random_waifu - some random waifu
    @commands.command(description="Random waifu")
    async def random_waifu(self, ctx):
        target = "waifu"
        
        embed = discord.Embed(
            color = discord.Color(0x45e0ff),
            timestamp = datetime.utcnow(),
        )

        embed.set_image(url=nekos.img(target))
        embed.set_footer(icon_url='{}'.format(ctx.message.author.avatar_url_as(format=None, static_format='png')).split("?")[0], text="Gerado por {0}".format(ctx.message.author.name))
        await ctx.reply(embed=embed)


    # !smug - some random smug pic
    @commands.command(description="Smug")
    async def smug(self, ctx):
        target = "smug"
        
        embed = discord.Embed(
            color = discord.Color(0x45e0ff),
            timestamp = datetime.utcnow(),
        )
        
        embed.set_image(url=nekos.img(target))
        embed.set_footer(icon_url='{}'.format(ctx.message.author.avatar_url_as(format=None, static_format='png')).split("?")[0], text="Gerado por {0}".format(ctx.message.author.name))
        await ctx.reply(embed=embed)


def setup(client):
    client.add_cog(Neko(client))
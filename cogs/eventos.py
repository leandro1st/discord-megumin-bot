import asyncio
from itertools import cycle
import discord
from discord.ext import commands
import random as r

class Eventos(commands.Cog, name="Eventos"):
    """Eventos"""


    def __init__(self, client):
        self.client = client


    @commands.Cog.listener()
    async def on_ready(self):
        print('{0.user} is online!'.format(self.client))
        self.client.loop.create_task(self.change_status())


    @commands.Cog.listener()
    async def on_member_join(self, member):
        channel = discord.utils.get(member.guild.text_channels, name="bem_vindo")
        # channel = self.client.get_channel(303571164171862017)
        await channel.send("Welcome to {}, <@!{}>! <:PogYou:695437835964252222>".format(member.guild.name, member.id))


    @commands.Cog.listener()
    async def on_member_remove(self, member):
        channel = discord.utils.get(member.guild.text_channels, name="bem_vindo")
        # channel = self.client.get_channel(303571164171862017)
        await channel.send("<@!{}> has left the server! <:SadChamp:695437902032797766>".format(member.id))


    @commands.Cog.listener()
    async def on_message(self, message):
        # channel = message.channel
        if message.content.startswith("<@!{}>".format(self.client.user.id)) and message.author != self.client.user:
            await message.reply('Sup', mention_author=True)
        if message.content == '<:PogChampion:706621494477717565>':
            await message.add_reaction('<:PogChampion:706621494477717565>')
        if message.content == ':rikkaBongo:':
            await message.add_reaction('<a:rikkaBongo:697839129257312286>')
            await message.reply('<a:rikkaBongo:697839129257312286>')
        if message.content == 'catJAM':
            await message.add_reaction('<a:catJAM:841531588298145812>')
        if message.author == self.client.user:
            return
        

    # Random status
    async def change_status(self):
        await self.client.wait_until_ready()

        status1 = ["!help", "with lolis", "Terraria", "osu!", "Visual Studio Code", "Nekopara", "Genshin Impact", "Princess Connect! Re: Dive", "Muse Dash", "Geometry Dash", "Little Witch Nobeta", "Euro Truck Simulator 2", "Apex Legends"]
        status2 = ["conhecimento", "osu!", "!help"]
        status3 = ["Lo-Fi", "Renai Circulation", "your cries", "Spotify", "GHOST / 星街すいせい", "Minato Aqua - For The Win", "Palette/常闇トワ", "YOASOBI「群青」", "ヨルシカ - 藍二乗", "YUC'e - Future Cake", "ツユ - くらべられっ子"]
        status4 = ["você", "Sword Art Online", "Koe no Katachi", "Made in Abyss", "Kyoukai no Kanata", "Boku no Hero Academia", "Kimi no Na wa.", "anime", "	Re:Zero kara Hajimeru Isekai Seikatsu", "Charlotte", "Tenki no Ko", "Machikado Mazoku", "Karakai Jouzu no Takagi-san", "KonoSuba", "Kaguya-sama wa Kokurasetai: Tensai-tachi no Renai Zunousen", "Seishun Buta Yarou wa Bunny Girl Senpai no Yume wo Minai", "Gotoubun no Hanayome", "Tate no Yuusha no Nariagari", "Hunter x Hunter", "Violet Evergarden", "Shingeki no Kyojin", "Charlotte", "Hotarubi no Mori e", "Minato Aqua", "Uruha Rushia", "Houshou Marine", "Nakiri Ayame", "Hoshimachi Suisei", "Shirakami Fubuki", "Usada Pekora", "Inugami Korone", "Sakura Miko", "Haachama", "Tokoyami Towa", "Tsunomaki Watame", "Nekomata Okayu", "Shirogane Noel", "Amane Kanata"]
        # Order --> playing, streaming, listening, watching

        msg1 = cycle(status1)
        msg2 = cycle(status2)
        msg3 = cycle(status3)
        msg4 = cycle(status4)

        while self.client:
            rand_number = r.randint(1,4)
            current_status1 = next(msg1)
            current_status2 = next(msg2)
            current_status3 = next(msg3)
            current_status4 = next(msg4)

            if rand_number == 1:
                await self.client.change_presence(activity=discord.Activity(type=discord.ActivityType.playing, name=current_status1))
            elif rand_number == 2:
                await self.client.change_presence(activity=discord.Activity(type=discord.ActivityType.streaming, name=current_status2, url='https://www.twitch.tv/leandro1st'))
            elif rand_number == 3:
                await self.client.change_presence(activity=discord.Activity(type=discord.ActivityType.listening, name=current_status3))
            elif rand_number == 4:
                await self.client.change_presence(activity=discord.Activity(type=discord.ActivityType.watching, name=current_status4))

            await asyncio.sleep(r.randint(60,90))


    # When command is not found/errors
    '''@commands.Cog.listener()
    async def on_command_error(self, ctx, error):
        if isinstance(error, commands.CommandNotFound):
            embed = discord.Embed(
                color = discord.Color(0xff0000),
                timestamp = datetime.utcnow(),
                description = "**Comando inexistente!**"
            )
            embed.set_footer(icon_url='{}'.format(ctx.message.author.avatar_url_as(format=None, static_format='png')).split("?")[0], text="Gerado por {0}".format(ctx.message.author.name))
            await ctx.reply(embed=embed)
    '''


def setup(client):
    client.add_cog(Eventos(client))
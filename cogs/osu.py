import discord
from discord.ext import commands
from datetime import datetime, timezone
from pytz import timezone #timezone()
import requests
import math
from decimal import Decimal, ROUND_HALF_UP
from dateutil.parser import parse #osu
from os import environ

osu_token = environ.get('OSU_API_KEY')

class Osu(commands.Cog, name="osu!"):
    """Comandos relacionados ao osu!"""


    def __init__(self, client):
        self.client = client


    # Osu - displays player's info
    @commands.command(usage="<username/id>", description="Display osu player's info")
    async def osu(self, ctx, *, username=None):
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
            message = await ctx.reply(embed=embed)
            await message.add_reaction('<:PogChampion:706621494477717565>')
            # await ctx.reply(r.json_user())
        # Username is incorrect or is not given
        else:
            if username == None:
                embed = discord.Embed(
                    color = discord.Color(0xff0000),
                    timestamp = datetime.utcnow(),
                    description = "**Sintaxe incorreta! Use !osu <username/id>**"
                )

                embed.set_footer(icon_url='{}'.format(ctx.message.author.avatar_url_as(format=None, static_format='png')).split("?")[0], text="Gerado por {0}".format(ctx.message.author.name))
                await ctx.reply(embed=embed)
            elif not json_user:
                embed = discord.Embed(
                    color = discord.Color(0xff0000),
                    timestamp = datetime.utcnow(),
                    description = "**Usuário não existe! <a:rikkaBongo:697839129257312286>**"
                )

                embed.set_footer(icon_url='{}'.format(ctx.message.author.avatar_url_as(format=None, static_format='png')).split("?")[0], text="Gerado por {0}".format(ctx.message.author.name))
                await ctx.reply(embed=embed)


    # !top10 - Osu user's top 10 plays
    @commands.command(usage="<username/id>", description="Display Top 10 Plays")
    async def top10(self, ctx, *, username=None):
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
                message = await ctx.reply(embed=embed)
                await message.add_reaction('<:PogYou:695437835964252222>')
            # If user doesnt have scores
            else:
                embed.add_field(name="No awesome performance records yet!", value=":sob:", inline=False)
                embed.set_thumbnail(url=avatar)
                embed.set_footer(icon_url='{}'.format(ctx.message.author.avatar_url_as(format=None, static_format='png')).split("?")[0], text="Gerado por {0}".format(ctx.message.author.name))
                message = await ctx.reply(embed=embed)
                await message.add_reaction('<:SadChamp:695437902032797766>')
        # Username is incorrect or is not given
        else:
            if username == None:
                embed = discord.Embed(
                    color = discord.Color(0xff0000),
                    timestamp = datetime.utcnow(),
                    description = "**Sintaxe incorreta! Use !top10 <username/id>**"
                )

                embed.set_footer(icon_url='{}'.format(ctx.message.author.avatar_url_as(format=None, static_format='png')).split("?")[0], text="Gerado por {0}".format(ctx.message.author.name))
                await ctx.reply(embed=embed)
            elif not json_user:
                embed = discord.Embed(
                    color = discord.Color(0xff0000),
                    timestamp = datetime.utcnow(),
                    description = "**Usuário não existe! <a:rikkaBongo:697839129257312286>**"
                )

                embed.set_footer(icon_url='{}'.format(ctx.message.author.avatar_url_as(format=None, static_format='png')).split("?")[0], text="Gerado por {0}".format(ctx.message.author.name))
                await ctx.reply(embed=embed)


def setup(client):
    client.add_cog(Osu(client))
from megumin import *
from itertools import cycle

# Silly method for random status
status1 = ["!help", "com lolis", "Terraria", "osu!", "Visual Studio Code", "Nekopara"]
status2 = ["conhecimento", "osu!", "!help"]
status3 = ["Lo-Fi", "Renai Circulation", "your cries", "Spotify"]
status4 = ["você", "Sword Art Online", "Koe no Katachi", "Made in Abyss", "Kyoukai no Kanata", "Boku no Hero Academia", "Kimi no Na wa", "anime", "	Re:Zero kara Hajimeru Isekai Seikatsu", "Charlotte"]
# Order --> playing, streaming, listening, watching

async def change_status():
    await client.wait_until_ready()
    msg1 = cycle(status1)
    msg2 = cycle(status2)
    msg3 = cycle(status3)
    msg4 = cycle(status4)

    while client:
        rand_number = random.randint(1,4)
        current_status1 = next(msg1)
        current_status2 = next(msg2)
        current_status3 = next(msg3)
        current_status4 = next(msg4)

        if rand_number == 1:
            await client.change_presence(activity=discord.Activity(type=discord.ActivityType.playing, name=current_status1))
        elif rand_number == 2:
            await client.change_presence(activity=discord.Activity(type=discord.ActivityType.streaming, name=current_status2, url='https://www.twitch.tv/leandro1st'))
        elif rand_number == 3:
            await client.change_presence(activity=discord.Activity(type=discord.ActivityType.listening, name=current_status3))
        elif rand_number == 4:
            await client.change_presence(activity=discord.Activity(type=discord.ActivityType.watching, name=current_status4))

        await asyncio.sleep(random.randint(60,90))

@client.event
async def on_ready():
    print('{0.user} is online!'.format(client))

@client.event
async def on_message(message):
    channel = message.channel
    if message.content.startswith("<@!{}>".format(client.user.id)):
        await channel.send('Howdy {0.author.mention}'.format(message))
    if message.content == '<:PogChampion:706621494477717565>':
        await message.add_reaction('<:PogChampion:706621494477717565>')
    if message.content == ':rikkaBongo:':
        await message.add_reaction('<a:rikkaBongo:697839129257312286>')
        await channel.send('https://cdn.discordapp.com/emojis/697839129257312286.gif')
    if message.content == '!stop':
        await message.add_reaction('<:peepoSad:695438016633634877>')
    if message.author == client.user:
        return

    # Overriding the default provided on_message forbids any extra commands from running
    # To fix this, add a bot.process_commands(message) line at the end of your on_message
    await client.process_commands(message)
    
client.loop.create_task(change_status())
client.run(token)

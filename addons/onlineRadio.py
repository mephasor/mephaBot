import discord
import re
import urllib.request
import xml.etree.ElementTree as ET

radio = {}
radioNames = {}
radioWhosPlaying = {}
radioNowPlaying = ''
playerStatus = 0
defaultChannel = ''
voice = ''

async def botWhatIsPlaying(client, message):
    if playerStatus is 0:
        await client.send_message(message.channel, 'А ничего и не играет.')
    else:
        if radioNowPlaying in radioWhosPlaying:
            print('Getting whos playing for' + radioNowPlaying)
            src = radioWhosPlaying[radioNowPlaying]
            response = urllib.request.urlopen(src[0])
            html = response.read()
            codec = response.info().get_param('charset', 'utf8')
            html = html.decode(codec)
            p = re.compile(src[1])
            result = re.search(p, html)
            if result is not None:
                gr = result.groups()
                if len(gr) is 3:
                    msg = "{:s} - {:s} ({:s})".format(gr[0], gr[1], gr[2])
                elif len(gr) is 2:
                    msg = "{:s} - {:s}".format(gr[0], gr[1])
                else:
                    msg = 'Ляляля играет. Я хз'
                await client.send_message(message.channel, msg)
            else:
                await client.send_message(message.channel, 'Не знаю что играет.')
        else:
            await client.send_message(message.channel,
                                      'Информация не доступна для этой станции')



async def botJoinVoiceChannel(client, message):
    print(message)
    if client.is_voice_connected(message.server):
        await client.send_message(message.channel,
                                  'Я уже в голосовом канале.')
    channel_name = defaultChannel 
    print('Trying to join: %s' % (channel_name))
    check = lambda c: c.name == channel_name and c.type == discord.ChannelType.voice
    channel = discord.utils.find(check, message.server.channels)
    if channel is None:
        await client.send_message(message.channel,
                                  'Не могу найти канал с таким названием.')
    else:
        global voice
        voice = await client.join_voice_channel(channel)
        client.starter = message.author


async def botStop(client, message):
    global playerStatus
    client.player.stop()
    client.loop.create_task(client.change_status())
    playerStatus = 0


async def botPlayRadio(client, message):
    global playerStatus
    global radioNowPlaying

    if not client.is_voice_connected(message.server):
        await botJoinVoiceChannel(client, message)

    if(playerStatus is not 0):
        print('Have to stop Radio first')
        print('PlayerStatus: ' + str(playerStatus))
        client.player.stop()
        radioNowPlaying = ''

    station = message.content[1:]

    #Handle special short cuts (desired by discord members)
    if station is '1':
        station = 'piterfm'
    elif station is '2':
        station = 'nashe'

    if station in radio:
        radioUrl = radio[station]
        print('Starting to play Radio Station: '+radioNames[station])
        client.player = voice.create_ffmpeg_player(radioUrl)
        client.player.start()
        radioNowPlaying = station
        playerStatus = 1

        game = discord.Game(name=radioNames[station])
        client.loop.create_task(client.change_status(game))
    else:
        print('No such station in list.')

commands = {
    '!bot': botJoinVoiceChannel,
    '!1': botPlayRadio,
    '!2': botPlayRadio,
    '!0': botStop,
    '!stop': botStop,
    '!a': botWhatIsPlaying,
}


def load(config):
    global radio
    global radioNames
    global radioWhosPlaying
    global defaultChannel
    # Open radio config and populate the command list, radio URL list and

    # radio name list.
    # configFile = open('cfg/radio.cfg').readlines()
    # for line in configFile:
    #     tmp = line.split(', ')
    #     radio[tmp[0]] = tmp[1].rstrip('\n')
    #     radioNames[tmp[0]] = tmp[2].rstrip('\n')
    #     commands['!'+tmp[0]] = botPlayRadio
    #     radioWhosPlaying[tmp[0]] = [tmp[3], tmp[4].rstrip('\n')]

    defaultChannel = config.getDefaultChannel()

    data = open('cfg/radio.xml').read()
    root = ET.fromstring(data)
    for station in root:
        cmd = station.find('command').text
        name = station.get('name')
        strURL = station.find('streamURL').text
        nowURL = station.find('nowPlayingURL').text
        nowRE = station.find('nowPlayingRE').text

        radio[cmd] = strURL.strip(' \t\n')
        radioNames[cmd] = name.strip('\n')
        commands['!'+cmd] = botPlayRadio

        # If we have now playing settings available
        if(nowURL is not None and nowRE is not None):
            radioWhosPlaying[cmd] = [nowURL.strip(' \n\t'), nowRE.strip(' \t\n')]


    return commands

def getName():
    return 'onlineRadio'

def getDescription():
    return 'Plays online radio stations found in cfg/radio.cfg.'

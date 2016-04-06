import discord
radio = {}
radioNames = {}

playerStatus = 0

async def botJoinVoiceChannel(client, message):
    print(message)
    if client.is_voice_connected():
        await client.send_message(message.channel,
                                  'Я уже в голосовом канале.')
    channel_name = '♫ Муз. Студия ♫'
    print('Trying to join: %s' % (channel_name))
    check = lambda c: c.name == channel_name and c.type == discord.ChannelType.voice
    channel = discord.utils.find(check, message.server.channels)
    if channel is None:
        await client.send_message(message.channel,
                                  'Не могу найти канал с таким названием.')
    else:
        await client.join_voice_channel(channel)
        client.starter = message.author


async def botStop(client, message):
    global playerStatus
    client.player.stop()
    client.loop.create_task(client.change_status())
    playerStatus = 0


async def botPlayRadio(client, message):
    global playerStatus

    if not client.is_voice_connected():
        await botJoinVoiceChannel(client, message)

    if(playerStatus is not 0):
        print('Have to stop Radio first')
        print('PlayerStatus: ' + str(playerStatus))
        client.player.stop()

    station = message.content[1:]

    #Handle special short cuts (desired by discord members)
    if station is '1':
        station = 'piterfm'
    elif station is '2':
        station = 'nashe'

    if station in radio:
        radioUrl = radio[station]
        print('Starting to play Radio Station: '+radioNames[station])
        client.player = client.voice.create_ffmpeg_player(radioUrl)
        client.player.start()
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
}


def load():
    # Open radio config and populate the command list, radio URL list and
    # radio name list.
    configFile = open('cfg/radio.cfg').readlines()
    for line in configFile:
        tmp = line.split(', ')
        radio[tmp[0]] = tmp[1].rstrip('\n')
        radioNames[tmp[0]] = tmp[2].rstrip('\n')
        commands['!'+tmp[0]] = botPlayRadio

    return commands

def getName():
    return 'onlineRadio'

def getDescription():
    return 'Plays online radio stations found in cfg/radio.cfg.'

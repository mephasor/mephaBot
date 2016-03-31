import discord
import asyncio


import configReader

if not discord.opus.is_loaded():
    # the 'opus' library here is opus.dll on windows
    # or libopus.so on linux in the current directory
    # you should replace this with the location the
    # opus library is located in and with the proper filename.
    discord.opus.load_opus('/usr/local/lib/libopus.so')


client = discord.Client()


class MephaBot:

    # Class Variables:

    # Config Reader Result:
    cfg = ''

    # Discord Client
    client = ''

    # Audio Player and its status
    player = 0

    # TODO: change this to an enum
    # 0 stopped, 1 playing, 2 paused
    playerStatus = 0

    # command list
    commands = {
        '!shrug': botShrug,
        '!exit': botExit,
        '!bot': botJoinVoiceChannel,
        '!piterfm': botPlayPiterFM,
        '!nashe': botPlayNashe,
        '!1live': botPlay1Live,
        '!stop': botStop
    }

    # Constructor
    def __init__(self, cfg, client):
        self.cfg = cfg
        self.client = client

    def runBot(self):
        client.run(self.cfg.getUsername(), self.cfg.getPW())

    #Command Execution functions
    async def botShrug(message):
        await client.send_message(message.channel,
                                  message.author.mention + u": ¯\_(ツ)_/¯")

    async def botExit(message):
        await client.send_message(message.channel, "Bot exiting now. bye bye :( ")
        client.logout()
        exit()

    async def botJoinVoiceChannel(message):
        if client.is_voice_connected():
            await client.send_message(message.channel,
                                      'Already connected to a voice channel')
        channel_name = '♫ Муз. Студия ♫'
        print('Trying to join: %s' % (channel_name))
        check = lambda c: c.name == channel_name and c.type == discord.ChannelType.voice
        channel = discord.utils.find(check, message.server.channels)
        if channel is None:
            await client.send_message(message.channel,
                                      'Cannot find a voice channel by that name.')
        else:
            await client.join_voice_channel(channel)
            client.starter = message.author

    async def botPlayPiterFM(message):
        global player
        global playerStatus

        if(playerStatus is not 0):
            player.stop()

        player = client.voice.create_ffmpeg_player(
            'http://icecast.piktv.cdnvideo.ru/piterfm?81')
        player.start()
        playerStatus = 1

    async def botPlayNashe(message):
        global player
        global layerStatus

        if(playerStatus is not 0):
            player.stop()

        player = client.voice.create_ffmpeg_player(
            'http://nashe1.hostingradio.ru:80/nashe-128.mp3')
        player.start()
        playerStatus = 1

    async def botPlay1Live(message):
        global player
        global playerStatus

        if(playerStatus is not 0):
            player.stop()

        player = client.voice.create_ffmpeg_player(
            'http://1live.akacast.akamaistream.net/7/706/119434/v1/gnl.akacast.akamaistream.net/1live')
        #piterPlayer = client.voice.create_stream_player('http://icecast.piktv.cdnvideo.ru/piterfm')
        player.start()
        playerStatus = 1


    async def botStop(message):
        player.stop()
        playerStatus = 0
        print(player.is_done())



# Event Handlers
    @client.event
    async def on_ready():
        print('Logged in as')
        print(client.user.name)
        print(client.user.id)
        print('------')


    @client.event
    async def on_message(message):

        for key in commands:
            if(message.content.startswith(key)):
                rtrn = await commands[key](message)
                await client.delete_message(message)


def main():
    cfg = configReader.ConfigReader()
    cfg.readConfig()
    myBot = MephaBot(cfg, client)


if __name__ == "__main__":
    main()

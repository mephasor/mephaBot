import discord
import asyncio


import configReader

if not discord.opus.is_loaded():
    # the 'opus' library here is opus.dll on windows
    # or libopus.so on linux in the current directory
    # you should replace this with the location the
    # opus library is located in and with the proper filename.
    discord.opus.load_opus('/usr/local/lib/libopus.so')




class MephaBot(discord.Client):

    # Class Variables:

    # Config Reader Result:
    cfg = ''
    commands = {}

    # Radio station dictionary
    radio = {}

    # Audio Player status
    player = 0

    defChannelName = '♫ Муз. Студия ♫'

    # TODO: change this to an enum
    # 0 stopped, 1 playing, 2 paused
    playerStatus = 0

    # Constructor
    def __init__(self, cfg):
        super().__init__()
        self.cfg = cfg

        configFile = open('cfg/radio.cfg').readlines()
        for line in configFile:
            tmp = line.split(', ')
            self.radio[tmp[0]] = tmp[1].rstrip('\n')


    def runBot(self):
       super().run(self.cfg.getUsername(), self.cfg.getPW())

    #Command Execution functions
    async def botShrug(self, message):
        await self.send_message(message.channel,
                                  message.author.mention + u": ¯\_(ツ)_/¯")

    async def botExit(self, message):
        await self.send_message(message.channel, "Bot exiting now. bye bye :( ")
        self.logout()
        exit()

    async def botJoinVoiceChannel(self, message):
        if self.is_voice_connected():
            await self.send_message(message.channel,
                                      'Already connected to a voice channel')
        channel_name = '♫ Муз. Студия ♫'
        print('Trying to join: %s' % (channel_name))
        check = lambda c: c.name == channel_name and c.type == discord.ChannelType.voice
        channel = discord.utils.find(check, message.server.channels)
        if channel is None:
            await self.send_message(message.channel,
                                      'Cannot find a voice channel by that name.')
        else:
            await self.join_voice_channel(channel)
            self.starter = message.author


    async def botStop(self, message):
        self.player.stop()
    async def botPlayRadio(self, message):
        if(self.playerStatus is not 0):
            self.player.stop()

        station = message.content[1:]
        radioUrl = self.radio[station]
        print('Starting to play Radio Station: '+station)
        self.player = self.voice.create_ffmpeg_player(radioUrl)
        self.player.start()
        self.playerStatus = 1

    # command list
    commands = {
        '!shrug': botShrug,
        '!exit': botExit,
        '!bot': botJoinVoiceChannel,
        '!piterfm': botPlayRadio,
        '!nashe': botPlayRadio,
        '!1live': botPlayRadio,
        '!stop': botStop
    }


# Event Handlers
    async def on_ready(self):
        print('Logged in as')
        print(self.user.name)
        print(self.user.id)
        print('------')


    async def on_message(self, message):


        for key in self.commands:
            if(message.content.startswith(key)):
                print(self.user.name)
                rtrn = await self.commands[key](self, message)
                await self.delete_message(message)


def main():
    cfg = configReader.ConfigReader()
    cfg.readConfig()
    myBot = MephaBot(cfg)
    myBot.runBot()

if __name__ == "__main__":
    main()

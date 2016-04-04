import discord
import asyncio
import urllib
import re


from include.chatterbotapi import ChatterBotFactory, ChatterBotType
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
    radioNames = {}

    # Audio Player status
    player = 0

    defChannelName = '♫ Муз. Студия ♫'

    # TODO: change this to an enum
    # 0 stopped, 1 playing, 2 paused
    playerStatus = 0




    def runBot(self):
       super().run(self.cfg.getUsername(), self.cfg.getPW())

    #Command Execution functions
    async def botShrug(self, message):
        await self.send_message(message.channel,
                                  message.author.mention + u": ¯\_(ツ)_/¯")

    async def botExit(self, message):
        await self.send_message(message.channel, "Ну я пошел. Пока! ")
        self.logout()
        exit()

    async def botJoinVoiceChannel(self, message):
        if self.is_voice_connected():
            await self.send_message(message.channel,
                                      'Я уже в голосовом канале.')
        channel_name = '♫ Муз. Студия ♫'
        print('Trying to join: %s' % (channel_name))
        check = lambda c: c.name == channel_name and c.type == discord.ChannelType.voice
        channel = discord.utils.find(check, message.server.channels)
        if channel is None:
            await self.send_message(message.channel,
                                      'Не могу найти канал с таким названием.')
        else:
            await self.join_voice_channel(channel)
            self.starter = message.author


    async def botStop(self, message):
        self.player.stop()
        self.loop.create_task(self.change_status())
        self.playerStatus = 0


    async def botPlayRadio(self, message):
        if not self.is_voice_connected():
            await self.botJoinVoiceChannel(message)

        if(self.playerStatus is not 0):
            print('Have to stop Radio first')
            print('PlayerStatus: ' + str(self.playerStatus))
            self.player.stop()

        station = message.content[1:]

        #Handle special short cuts (desired by discord members)
        if station is '1':
            station = 'piterfm'
        elif station is '2':
            station = 'nashe'

        if station in self.radio:
            radioUrl = self.radio[station]
            print('Starting to play Radio Station: '+self.radioNames[station])
            self.player = self.voice.create_ffmpeg_player(radioUrl)
            self.player.start()
            self.playerStatus = 1

            game = discord.Game(name=self.radioNames[station])
            self.loop.create_task(self.change_status(game))
        else:
            print('No such station in list.')


    async def botListCommands(self, message):
        for key in self.commands:
            print(key, str(self.commands[key]))


    async def botCleverbot(self, message):
        p = re.compile('\|([A-F0-9][A-F0-9][A-F0-9][A-F0-9])')

        msg = message.content[2:]
        sendMsg = msg
        print('message: '+sendMsg)
        response = self.bot1session.think(sendMsg)
        res = re.findall(p,response)
        for i in res:
            response = response.replace('|'+i, chr(int(i, 16)))

        await self.send_message(message.channel,response)
        print(response)

    # command list
    commands = {
        '!shrug': botShrug,
        '!exit': botExit,
        '!bot': botJoinVoiceChannel,
        '!1': botPlayRadio,
        '!2': botPlayRadio,
        '!0': botStop,
        '!stop': botStop,
        '!list': botListCommands,
        '=': botCleverbot
    }

    # Constructor
    def __init__(self, cfg):
        super().__init__()
        self.cfg = cfg

        # Open radio config and populate the command list, radio URL list and
        # radio name list.
        configFile = open('cfg/radio.cfg').readlines()
        for line in configFile:
            tmp = line.split(', ')
            self.radio[tmp[0]] = tmp[1].rstrip('\n')
            self.radioNames[tmp[0]] = tmp[2].rstrip('\n')
            self.commands['!'+tmp[0]] = MephaBot.botPlayRadio

        # Init Cleverbot
        factory = ChatterBotFactory()
        self.bot1 = factory.create(ChatterBotType.CLEVERBOT)
        self.bot1session = self.bot1.create_session()



# Event Handlers
    async def on_ready(self):
        print('Logged in as')
        print(self.user.name)
        print(self.user.id)
        print('------')


    async def on_message(self, message):

        for key in self.commands:
            # command has to match the key exactly
            cmd = message.content.split(' ')[0]
            if cmd == key:
                rtrn = await self.commands[key](self, message)
                if key != '=':
                    await self.delete_message(message)


def main():
    cfg = configReader.ConfigReader()
    cfg.readConfig()
    myBot = MephaBot(cfg)
    myBot.runBot()

if __name__ == "__main__":
    main()

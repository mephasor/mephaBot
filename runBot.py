import discord
import asyncio
import urllib
import re
import importlib

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

    # Addon list
    addonList = []

    def runBot(self):
       super().run(self.cfg.getUsername(), self.cfg.getPW())

    #Command Execution functions
    async def botExit(self, message):
        await self.send_message(message.channel, "Ну я пошел. Пока! ")
        self.logout()
        exit()
        

    async def botListCommands(self, message):
        for key in self.commands:
            print(key, str(self.commands[key]))

    # command list
    commands = {
        '!exit': botExit,
        '!list': botListCommands,
    }

    def initAddons(self):
        names = self.cfg.getAddonList()

        # load addon modules
        for name in names:
            self.addonList.append(importlib.import_module('addons.'+name))

        # load addon commands
        for addon in self.addonList:
            newCmds = addon.load()
            for cmd in newCmds:
                self.commands[cmd] = newCmds[cmd]

    # Constructor
    def __init__(self, cfg):
        super().__init__()
        self.cfg = cfg
        
        # Load addons
        self.initAddons()



# Event Handlers
    async def on_ready(self):
        print('Logged in as')
        print(self.user.name)
        print(self.user.id)
        print('------')

# The main dispatcher. Calls functions based on key words. 
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

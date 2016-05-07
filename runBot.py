#!/usr/bin/python3.5
import discord
import asyncio
import urllib
import re
import importlib
import sys

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
       super().run(self.cfg.getToken())

    #Command Execution functions
    async def botExit(self, message):
        await self.send_message(message.channel, "Ну я пошел. Пока! ")
        self.logout()
        sys.exit(0)


    async def botListCommands(self, message):
        msg = 'Лист доступных команд:\n'
        for key in self.commands:
            msg = msg + key + '\n'
            print(key, str(self.commands[key]))
        await self.send_message(message.channel, msg)

    # command list
    commands = {
        '!exit': botExit,
        '!list': botListCommands,
    }

    def initAddons(self, cfg):
        names = self.cfg.getAddonList()

        # load addon modules
        for name in names:
            self.addonList.append(importlib.import_module('addons.'+name))

        # load addon commands
        for addon in self.addonList:
            newCmds = addon.load(cfg)
            for cmd in newCmds:
                self.commands[cmd] = newCmds[cmd]

    # Constructor
    def __init__(self, cfg):
        super().__init__()
        self.cfg = cfg

        # Load addons
        self.initAddons(cfg)


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

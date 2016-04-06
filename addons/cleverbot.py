import discord
import re
from include.chatterbotapi import ChatterBotFactory, ChatterBotType

bot = ''
botSession = ''


# async functions
async def botCleverbot(client, message):
    global botSession

    p = re.compile('\|([A-F0-9][A-F0-9][A-F0-9][A-F0-9])')

    msg = message.content[2:]
    sendMsg = msg
    response = botSession.think(sendMsg)

    # handle funny behaviour with unicode
    res = re.findall(p,response)
    for i in res:
        response = response.replace('|'+i, chr(int(i, 16)))

    await client.send_message(message.channel,response)

# command list
commands = {
    '=': botCleverbot
}

# addon init function
def load():
    global bot
    global botSession
    # Init Cleverbot
    factory = ChatterBotFactory()
    bot = factory.create(ChatterBotType.CLEVERBOT)
    botSession = bot.create_session()

    return commands

# addon name function
def getName():
    return 'cleverbot'


# addon description
def getDescription():
    return 'Allows the bot to use the CleverbotAPI and be talked to in chat'

import discord


async def botShrug(client,  message):
    await client.send_message(message.channel,
                              message.author.mention + u": ¯\_(ツ)_/¯")

commands = {
    '!shrug': botShrug
}

def load(config):
    return commands

def getName():
    return 'shrug addon'

def getDescription():
    return 'Posts a ¯\_(ツ)_/¯ into the chat where the command is executed.'

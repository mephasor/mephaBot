import re

p = re.compile(r"DiscordName=(.*)\nDiscordPW=(.*)\n.*\n.*\nOwnerID=(.*)")

configPath = 'cfg/botConfig.cfg'


class ConfigReader:

    username = ''
    password = ''
    ownerID = ''

    ''' Read in the config file and set parameters'''

    def readConfig(self):
        cfgFile = open(configPath, 'r')
        cfgContent = cfgFile.read()

        result = re.search(p, cfgContent)
        self.username = result.groups()[0]
        self.password = result.groups()[1]
        self.ownerID = result.groups()[2]

    def getUsername(self):
        return self.username

    def getPW(self):
        return self.password

    def getOwnerID(self):
        return self.ownerID

import re
p = re.compile(r"DiscordToken=(.*)\n\n.*\nOwnerID=(.*)")
q = re.compile(r"ADDON=(.*)\n")
r = re.compile(r"DefaultVoiceChannel=(.*)")

configPath = 'cfg/botConfig.cfg'


class ConfigReader:

    token = ''
    ownerID = ''

    addonList = []

    ''' Read in the config file and set parameters'''

    def readConfig(self):
        cfgFile = open(configPath, 'r')
        cfgContent = cfgFile.read()

        result = re.search(p, cfgContent)
        self.token = result.groups()[0]
        self.ownerID = result.groups()[1]

        addonResults = re.findall(q, cfgContent)

        self.defaultChannel = re.search(r, cfgContent).groups()[0]
        print('Default Channel: ' + self.defaultChannel)
        for addon in addonResults:
            print('cfgAddonFound: '+addon)
            self.addonList.append(addon)

    def getToken(self):
        return self.token

    def getOwnerID(self):
        return self.ownerID

    def getAddonList(self):
        return self.addonList

    def getDefaultChannel(self):
        return self.defaultChannel

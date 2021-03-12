# mephaBot

# !!! THIS BOT IS CURRENTLY NOT MAINTAINED !!!

Little Discord Bot that I use to play radio streams and other random stuff.

The bot uses an addon structure. Addons can be enable and disabled in the config file. New addons can be added using the interfaces.

Currently it is mainly used to play online radion stations contained in cfg/radio.xml

Additionally it  has cleverbot support. More features to come. 

Have a request? create an issue and maybe I can quickly implement it.

## Command list so far: 
| Command |   Function |
|---------|------------|
| !shrug  | ¯\_(ツ)_/¯ |
| !bot | Connects to the predefined channel|
| !RADIOSHORT| Plays the radio station as defined in the config file. |
| = <message>| Talks to a cleverbot|
| !list | lists all commands available|

## radio.xml structure

Each station has to be created according to the following example code: 
```xml
    <!-- Питер FM -->
  <station name="Питер FM">
    <command>piterfm</command>
    <streamURL>
      http://icecast.piktv.cdnvideo.ru/piterfm
    </streamURL>
    <nowPlayingURL>http://www.radiopiterfm.ru/login/div_musicblock.php</nowPlayingURL>
    <nowPlayingRE><![CDATA[;"><strong>(.*)<\/strong> &mdash; (.*) <span>(\d*:\d*)<\/span>
    ]]>
    </nowPlayingRE>
  </station>

```

Usage: 

1. Install ffmpeg (http://ffmpeg.org/)
2. Install discordpy (`pip3 install -r requirements.txt`)
3. ./run

Ctrl+c to stop bot script

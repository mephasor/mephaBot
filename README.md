# mephaBot
Little Discord Bot that I use to play radio streams and other random stuff.

Currently it is mainly used to play online radion stations contained in cfg/radio.xml

Additionally it  has cleverbot support. More features to come. 

Have a request? create an issue and maybe I can quickly implement it.

##Command list so far: 

- !shrug: ¯\_(ツ)_/¯
- !bot: Connects to the predefined channel
- !RADIOSHORT: Plays the radio station as defined in the config file. 
- = <message>: Talks to a cleverbot

##radio.xml structure

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

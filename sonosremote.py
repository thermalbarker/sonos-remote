#!/usr/bin/env python
import soco
import lirc

lirc_client = "sonosremote"
sonos_room = "Kitchen"

meta_template = """
<DIDL-Lite xmlns:dc="http://purl.org/dc/elements/1.1/"
    xmlns:upnp="urn:schemas-upnp-org:metadata-1-0/upnp/"
    xmlns:r="urn:schemas-rinconnetworks-com:metadata-1-0/"
    xmlns="urn:schemas-upnp-org:metadata-1-0/DIDL-Lite/">
    <item id="R:0/0/0" parentID="R:0/0" restricted="true">
        <dc:title>{title}</dc:title>
        <upnp:class>object.item.audioItem.audioBroadcast</upnp:class>
        <desc id="cdudn" nameSpace="urn:schemas-rinconnetworks-com:metadata-1-0/">
            {service}
        </desc>
    </item>
</DIDL-Lite>' """

tunein_service = 'SA_RINCON65031_'

g_sonos = None

def get_sonos(force = True):
    global g_sonos
    
    if force:
        g_sonos = None

    if g_sonos is None:
        for zone in soco.discover():
            if zone.player_name == sonos_room:
                print zone.player_name
                g_sonos = zone
    return g_sonos

def ungroup_if_grouped(zone):
    print zone.group
    if zone.group is not None:
        # Check if current player is the co-ordinator
        if zone.group.coordinator is not zone:
            print "Leaving group"
            zone.unjoin()
            

def play_radio(station):
    zone = get_sonos()

    preset = station - 1

    if zone is not None:
        stations = zone.get_favorite_radio_stations()
        print 'returned %s of a possible %s radio stations:' % (
            stations['returned'], stations['total'])
        
        if stations['returned'] > preset:
            station = stations['favorites'][preset]
            print station['title']
            uri = station['uri']
            # TODO seems at least & needs to be escaped - should move this to
            # play_uri and maybe escape other chars.
            uri = uri.replace('&', '&amp;')

            metadata = meta_template.format(title=station['title'], service=tunein_service)

            ungroup_if_grouped(zone)
            zone.play_uri(uri, metadata)

def play():
    print "Play"
    zone = get_sonos()
    if zone is not None:
        playing = zone.get_current_transport_info()['current_transport_state']
        print playing
        if playing != 'PLAYING':
            zone.play()
        else:
            ungroup_if_grouped(zone)
            zone.pause()

def volume_up():
    zone = get_sonos()
    volume_now = zone.volume
    print "Current Volume: ", volume_now
    zone.volume = volume_now + 2

def volume_down():
    zone = get_sonos()
    volume_now = zone.volume
    print "Current Volume: ", volume_now
    zone.volume = volume_now - 2


def one():
    play_radio(1)

def two():
    play_radio(2)

def three():
    play_radio(3)

def four():
    play_radio(4)

def five():
    play_radio(5)

def six():
    play_radio(6)

def seven():
    play_radio(7)

def eight():
    play_radio(8)

def nine():
    play_radio(9)

def zero():
    play_radio(10)


switcher = {
    'play'  : play,
    'volume_up' : volume_up,
    'volume_down' : volume_down,
    'one'   : one,
    'two'   : two,
    'three' : three,
    'four'  : four,
    'five'  : five,
    'six'   : six,
    'seven' : seven,
    'eight' : eight,
    'nine'  : nine,
    'zero'  : zero
}
    

def main():

    while True:
        try:
            print "LIRC Init:"
            lirc.init(lirc_client)
            print "Find Sonos:"
            get_sonos(True)
    
            while True:
                print "Waiting for IR press"
                codes = lirc.nextcode()
                print "Got code: ", codes
                for code in codes:
                    print "Key press: ", code
                    if code in switcher.keys():
                        func = switcher.get(code)
                        func()

        except Exception as e:
            print "Exception:"
            print e
            pass

        lirc.deinit()


if __name__ == "__main__":
    main()




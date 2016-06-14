'''
Created on May 4, 2016

@author: pldkowalsk
'''

import gobject
import dbus
import dbus.service
from dbus.mainloop.glib import DBusGMainLoop

bus_name = "com.example.audio"

class Player(dbus.service.Object):
    interface = bus_name + ".Player"
    def __init__(self, bus, name):
        self.path = "/player/"+name
        dbus.service.Object.__init__(self, bus, self.path)
        self.tracks = []
        self.now_playing = None
        self.now_playing_source = None

    @dbus.service.method(dbus_interface=interface,
                         in_signature='si')
    def AddTrack(self, name, time):
        self.tracks.append((name, time))
        print "[%s] Added track to play: '%s' [%sd]"%(self.path, name, time)
    
    @dbus.service.method(dbus_interface=interface,
                         out_signature='a(si)')
    def GetTracks(self):
        return self.tracks
    
    @dbus.service.method(dbus_interface=interface,
                         in_signature='i')
    def Play(self, index):
        if index >=0 and index < len(self.tracks):
            self.PlayTrack(index)
        else:
            raise dbus.exceptions.DBusException("There is no track with index: %d"%index, name="com.example.audio.NoTrack")
    
    @dbus.service.signal(dbus_interface=interface,
                         signature='si')
    def NowPlaying(self, name, time):
        pass
    
    @dbus.service.signal(dbus_interface=interface,
                         signature='si')
    def Played(self, name, time):
        pass
    
    def PlayTrack(self, index):
        name, time = self.tracks[index]
        self.now_playing = index 
        print "[%s] Now playing: '%s' [%ds]"%(self.path, name, time)
        self.NowPlaying(name, time)
        if (self.now_playing_source):
            gobject.source_remove(self.now_playing_source)
        self.now_playing_source = \
            gobject.timeout_add_seconds(time, self.PlayedTrack, self.now_playing)
    
    def PlayedTrack(self, index):
        name, time = self.tracks[index]
        print "[%s] Played: '%s' [%ds]"%(self.path, name, time)
        self.Played(name, time)
        index += 1
        if index >=0 and index < len(self.tracks):
            self.PlayTrack(index)
        else:
            print "[%s] End of tracks"%self.path

class MasterAudio(dbus.service.Object):
    interface = bus_name
    def __init__(self, bus):
        self.bus = bus
        dbus.service.Object.__init__(self, bus, "/master")
        self.players = {}

    @dbus.service.method(dbus_interface=interface,
                         in_signature='s', out_signature='s')
    def AddPlayer(self, name):
        player = Player(self.bus, name)
        self.players[name] = player
        path = player.path
        print "Added player '%s' under path: %s"%(name,path)
        return path

def main():
    DBusGMainLoop(set_as_default=True)
    
    bus = dbus.SessionBus()
    busname = dbus.service.BusName(bus_name, bus)
    obj = MasterAudio(bus)
    
    loop = gobject.MainLoop()
    loop.run()


if __name__ == '__main__':
    main()
'''
Created on May 4, 2016

@author: pldkowalsk
'''

import gobject
import dbus
import dbus.service
from dbus.mainloop.glib import DBusGMainLoop

bus_name = "com.harman.audio"

class Player(dbus.service.Object):
    interface = bus_name + ".Player"
    def __init__(self, bus, name):
        self.path = "/player/"+name
        dbus.service.Object.__init__(self, bus, self.path)
        self.tracks = []
        self.now_playing = None

    @dbus.service.method(dbus_interface=interface,
                         in_signature='si')
    def AddTrack(self, name, time):
        self.tracks.append((name, time))
        print "Added track to play: '%s' [%sd]"%(name, time)
    
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
            raise dbus.exceptions.DBusException("There is no track with index: %d"%index, name="com.harman.audio.NoTrack")
    
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
        print "Now playing: %s [%ds]"%(name, time)      
        gobject.timeout_add_seconds(time, self.PlayedTrack, self.now_playing)
    
    def PlayedTrack(self, index):
        name, time = self.tracks[index]
        print "Played: %s [%ds]"%(name, time)
        index += 1
        if index >=0 and index < len(self.tracks):
            self.PlayTrack(index)
        else:
            print "End of tracks"

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

def hello():
    print "Hello world"

DBusGMainLoop(set_as_default=True)

#gobject.timeout_add(100, make_calls)
val = gobject.timeout_add_seconds(3, hello)
gobject.source_remove(val)

bus = dbus.SessionBus()
busname = dbus.service.BusName(bus_name, bus)
obj = MasterAudio(bus)

loop = gobject.MainLoop()
loop.run()


if __name__ == '__main__':
    pass
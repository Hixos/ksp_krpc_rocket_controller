from ksp_krpc import SpaceCenterStreams, KRPCStreams


class GlobalStreams:
    def __init__(self):
        self.streams = {}

    def addStream(self, name, stream):
        if name not in self.streams:
            self.streams[name] = stream

    def closeStreams(self):
        for k in self.streams.keys():
            self.streams[k].remove()

    def __getattr__(self, item):
        if item in self.streams:
            return self.streams[item]
        else:
            exc_msg = "No attribute called '".format(item)
            raise AttributeError(exc_msg)


global_streams = GlobalStreams()

global_streams.addStream('ut', SpaceCenterStreams.UTStream())
global_streams.addStream('physics_warp', SpaceCenterStreams.physicsWarpStream())
global_streams.addStream('game_paused', KRPCStreams.gamePausedStream())

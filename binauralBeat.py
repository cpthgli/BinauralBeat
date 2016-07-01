#coding: utf-8
import struct, pyaudio as pa
from math import sin, pi

class StereoSound:

    def __init__(self, format, rate):
        self.format = format
        self.rate = rate
        self.cast = {
            pa.paFloat32:(float,'f'),
            pa.paInt32:(int,'q'),
            pa.paInt24:(int,'3b'),
            pa.paInt16:(int,'i'),
            pa.paInt8:(int,'h'),
            pa.paUInt8:(int,'I'),
        }

    def generateSinWave(self, left, right, volume=1, time=1):
        length = time * self.rate
        data = [0.0]*(length<<1)
        left_theta = 2 * pi * left / self.rate
        right_theta = 2 * pi * right / self.rate
        for n, l, r in zip(range(0,length),range(0,length<<1,2),range(1,length<<1,2)):
            data[l] = volume * sin(left_theta * n)
            data[r] = volume * sin(right_theta * n)
        data = [self.cast[self.format][0](x) for x in data]
        self.data = struct.pack(self.cast[self.format][1] * (length<<1), *data)

    def play(self, repeat=1):
        p = pa.PyAudio()
        stream = p.open(format=self.format,
                        channels=2,
                        rate=self.rate,
                        output=True)
        while repeat>0:
            stream.write(self.data)
            repeat-=1
        stream.close()
        p.terminate()

if __name__ == "__main__" :
    sound = StereoSound(pa.paFloat32, 192000)
    sound.generateSinWave(440, 450, 0.05)
    sound.play(3)

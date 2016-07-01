#coding: utf-8
import sys, struct, wave, pyaudio as pa
from math import sin, pi

class StereoSound:

    def __init__(self, format=pa.paInt16, sampling=44100, bit=16):
        self.format = format
        self.sampling = int(sampling)
        self.cast = {
            pa.paFloat32:(float,2,'f'),
            pa.paInt32:(int,32,'i'),
            pa.paInt24:(int,24,'3b'),
            pa.paInt16:(int,16,'h'),
            pa.paInt8:(int,8,'b'),
        }
        self.bit = int(bit)

    def generateSinWave(self, left, right, volume=0.98, time=1.0):
        length = int(time * self.sampling)
        d = [0.0]*(length<<1)
        left_theta = 2 * pi * left / self.sampling
        right_theta = 2 * pi * right / self.sampling
        for n, l, r in zip(range(0,length),range(0,length<<1,2),range(1,length<<1,2)):
            d[l] = volume * sin(left_theta * n)
            d[r] = volume * sin(right_theta * n)
        d = [self.cast[self.format][0](x * float(2**(self.cast[self.format][1]-1)-1)) for x in d]
        self. d = d
        self.data = struct.pack(self.cast[self.format][2] * (length<<1), *d)

    def play(self, repeat=1):
        p = pa.PyAudio()
        stream = p.open(format=self.format,
                        channels=2,
                        rate=self.sampling,
                        output=True)
        while repeat>0:
            stream.write(self.data)
            repeat-=1
        stream.close()
        p.terminate()

if __name__ == "__main__" :
    sound = StereoSound(pa.paInt16, 44100)
    f1 = 440
    f2 = 450
    sound.generateSinWave(f1, f2, 0.5)
    sound.play(10)
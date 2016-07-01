#coding: utf-8
import struct, pyaudio as pa
from math import sin, pi

class StereoSound:

    def __init__(self, format=pa.paInt16, sampling=44100):
        self.form = format
        self.samp = sampling

    def generateSinWave(self, left, right, volume=0.98, time=1.0):
        cast = {pa.paFloat32:(float, 1.0, 'f'),
                pa.paInt32:(int, 2147483647.0, 'i'),
                pa.paInt24:(int, 8388607.0, '3b'),
                pa.paInt16:(int, 32767.0, 'h'),
                pa.paInt8:(int, 127.0, 'b'),}
        length = int(time * self.samp)
        num = length << 1
        data = [0.0] * num
        left_theta = 2 * pi * float(left) / self.samp
        right_theta = 2 * pi * float(right) / self.samp
        for (n, l), r in zip(enumerate(range(0, num,2)), range(1, num,2)):
            data[l] = volume * sin(left_theta * n)
            data[r] = volume * sin(right_theta * n)
        data = [cast[self.form][0](x * cast[self.form][1]) for x in data]
        self.data = struct.pack(cast[self.form][2] * num, *data)

    def play(self, repeat=1):
        p = pa.PyAudio()
        stream = p.open(format=self.form,
                        channels=2,
                        rate=int(self.samp),
                        output=True)
        while repeat != 0:
            stream.write(self.data)
            repeat -= 1
        stream.close()
        p.terminate()

if __name__ == "__main__" :
    sound = StereoSound()
    f1 = 440
    f2 = 450
<<<<<<< HEAD:binauralBeat.py
    sound.generateSinWave(f1, f2, 0.002)
    sound.play(-1)
=======
    sound.generateSinWave(f1, f2, 0.05)
    sound.play(5)
>>>>>>> bfe4ddf880ee27cf91761eda47ebb3e5d29ca90b:BinauralBeat.py
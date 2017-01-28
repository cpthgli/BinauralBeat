'''
binauralBeats.py is generate Binaural bets and play.
'''
import time
import numpy as np
import pyaudio as pa


class SampleFormatNotSuportedException(Exception):
    '''
    Exception for Portaudio Sample Formats that not be supported.
    '''

    def __init__(self, fmt):
        self._fmt = fmt

    def __str__(self):
        return "pyaudio. " + self._fmt + ' is not supported.'


class StereoSounds():
    '''
    Stereo sounds class.
    '''

    def __init__(self, fmt=pa.paInt16, rate=44100):
        self.fmt = fmt
        self.rate = rate
        self.amp = 1 if fmt == pa.paFloat32 else 128**pa.get_sample_size(
            fmt) / 2 - 1
        if fmt == pa.paFloat32:
            self.dtype = np.float32  # pylint: disable=E1101
        elif fmt == pa.paInt32:
            self.dtype = np.Int32  # pylint: disable=E1101
        elif fmt == pa.paInt24:
            raise SampleFormatNotSuportedException('paInt24')
        elif fmt == pa.paInt16:
            self.dtype = np.int16
        elif fmt == pa.paInt8:
            self.dtype = np.int8
        elif fmt == pa.paUInt8:
            self.dtype = np.uint8
        else:
            raise SampleFormatNotSuportedException('paCustomFormat')
        self.data = b''

    def generate_sine_wave(self, left, right, volume=0.98):
        '''
        Generate a sine wave.
        '''
        data = np.ones(self.rate * 2) * volume
        ldata = np.sin(2 * np.pi * left / self.rate * np.arange(self.rate))
        rdata = np.sin(2 * np.pi * right / self.rate * np.arange(self.rate))
        index = np.arange(0, self.rate * 2, 2)
        np.multiply.at(data, index, ldata)
        np.multiply.at(data, index + 1, rdata)
        self.data = (data * self.amp).astype(self.dtype).tobytes()

    def play(self, repeat=1):
        '''
        Play sounds.
        '''
        audio = pa.PyAudio()
        stream = audio.open(
            format=self.fmt,
            channels=2,
            rate=int(self.rate),
            output=True
        )
        start_time = time.time()
        while time.time() - start_time < repeat:
            stream.write(self.data)
        stream.close()
        audio.terminate()

if __name__ == "__main__":
    SOUNDS = StereoSounds()
    SOUNDS.generate_sine_wave(440, 445, 0.02)
    SOUNDS.generate_sine_wave(820, 800, 0.02)
    SOUNDS.play(5)

"""Helper functions to generate an audio buffer from given frequencies"""

import math, wave, struct
import numpy as np
import frequencies as fr

samplerate = 44100 # in Hz
sample_duration = int(samplerate * 0.1) # 0.1 = 100ms of tone duration

def make_single_tone_buffer(sr: int, freq_l: int, freq_h:int , dur: int) -> list:
    """Function that writes an audio buffer for two given frequencies that are mixed together.

    Parameters:
    sr (int): Defined samplerate.
    freq_l(int): Lower frequency of the DTMF-signal.
    freq_r(int): High frequency of the DTMF-signal.
    dur(int): Duration of the signal.

    Return:
    list: Audio buffer of a single DTMD-tone 
    """
    buffer = []
    for i in range(dur):
        tones = []
        sample_l = 0.5 * math.sin(2. * math.pi * i * freq_l / sr)
        tones.append(sample_l)
        sample_h = 0.5 * math.sin(2. * math.pi * i * freq_h / sr)
        tones.append(sample_h)
        tones_sum = np.sum(tones)
        buffer.append(tones_sum)
    return buffer

def generate_audio_sequence(tel_num: list) -> list:
    audio_buffer = []
    frequencies_low = []
    frequencies_high = []

    for digit in tel_num:
        digit_frequencies = fr.frequencies[digit]
        frequencies_low.append(digit_frequencies[0])
        frequencies_high.append(digit_frequencies[1])
    
    for i in range(len(frequencies_low)):
        local_audio_buffer = make_single_tone_buffer(samplerate, frequencies_low[i], frequencies_high[i], sample_duration)
        for j in range(len(local_audio_buffer)):
            local_audio_buffer[j] *= 1. - j / len(local_audio_buffer)
        for k in local_audio_buffer:
            audio_buffer.append(k)
    return audio_buffer

def buffer_to_bytearray(audio_buf: list) -> bytearray:
    bin_buf = bytearray()
    for sample in audio_buf:
        local_sample = sample * ((2**16 - 1) / (2**16))
        bin_buf = bin_buf + struct.pack('h', round(local_sample * 2 **16/2))
    return bin_buf


if __name__ == '__main__':

    telephone_number = ['0', '7', '2', '1', '6', '6', '2', '9', '2', '1', '2']

    audio_buffer = generate_audio_sequence(telephone_number)
    bin_buf = buffer_to_bytearray(audio_buffer)

    out = wave.open('test.wav', 'w')
    out.setnchannels(1)
    out.setsampwidth(2)
    out.setframerate(samplerate)
    out.writeframes(bin_buf)
    out.close()
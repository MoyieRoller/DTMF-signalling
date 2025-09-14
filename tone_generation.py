import math, wave, struct
import numpy as np
import frequencies as fr

frequencies_low = []
frequencies_high = []

samplerate = 44100
sample_duration = int(samplerate * 0.1) # 100ms of tone duration

def generate_frequencies(tel_num):
    for digit in tel_num:
        digit_frequencies = fr.frequencies[digit]
        frequencies_low.append(digit_frequencies[0])
        frequencies_high.append(digit_frequencies[1])

def make_audio_buffer(sr, freq_l, freq_h, dur):
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

def buf_to_byte(audio_buf):
    bin_buf = bytearray()
    for sample in audio_buf:
        local_sample = sample * ((2**16 - 1) / (2**16))
        bin_buf = bin_buf + struct.pack('h', round(local_sample * 2 **16/2))
    return bin_buf


if __name__ == '__main__':

    telephone_number = ['0', '7', '2', '1', '6', '6', '2', '9', '2', '1', '2']
    generate_frequencies(telephone_number)

    audio_buffer = []
    for i in range(len(frequencies_low)):
        local_audio_buffer = make_audio_buffer(samplerate, frequencies_low[i], frequencies_high[i], sample_duration)
        for j in range(len(local_audio_buffer)):
            local_audio_buffer[j] *= 1. - j / len(local_audio_buffer)
        for k in local_audio_buffer:
            audio_buffer.append(k)

    bin_buf = buf_to_byte(audio_buffer)

    wav = wave.open('test.wav', 'w')
    wav.setnchannels(1)
    wav.setsampwidth(2)
    wav.setframerate(samplerate)
    wav.writeframes(bin_buf)
    wav.close()
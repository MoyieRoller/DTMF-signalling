"""Main function to write a .wav-file and handle the input of the whole program"""

import wave, sys, os
import tone_generation as tg

input_number = []
input_path = ''

# two different input modes, either as commandline argument on program call or commandline input after program start
if len(sys.argv) == 1:
    while(True):
        user_input = input('Please insert a telephone number and a designated path the audiofile is saved to: ')

        if user_input == '':
            print('ERROR: No input given.')
            continue

        if user_input == 'exit':
            print('Exiting...')
            sys.exit(0)
        else:
            user_input = user_input.split(' ')

        try:
            val = int(user_input[0])
        except ValueError:
            print('ERROR: The inserted telephone number does not solely consist of digits.')
            continue
        else:
            input_number = list(user_input[0])
        
        try:
            if len(user_input) <= 1:
                raise SyntaxError
        except SyntaxError:
            print('ERROR: The designated path is missing.')
            continue

        try:
            if os.path.isdir(user_input[1]) == False:
                raise IsADirectoryError
        except IsADirectoryError:
            print('ERROR: The designated path is not a correct path.')
            continue
        else:
            input_path = user_input[1]
            break
else:
    user_input = list(sys.argv[1:])
    try:
        val = int(user_input[0])
    except ValueError:
        print('ERROR: The inserted telephone number does not solely consist of digits.')
        sys.exit(0)
    else:
        input_number = list(user_input[0])

    try:
        if len(user_input) <= 1:
            raise SyntaxError
    except SyntaxError:
        print('ERROR: The designated path is missing.')
        sys.exit(0)
    
    try:
        if os.path.isdir(user_input[1]) == False:
            raise IsADirectoryError
    except IsADirectoryError:
        print('ERROR: The designated path is not a correct path.')
        sys.exit(0)
    else:
        input_path = user_input[1]

# output the telephone number to the commandline
print(f'Telephone number: {int(user_input[0])}')

# in case a path is entered without '/' at the end, it is added, so no error occurs
if not input_path.endswith('/'):
    input_path += '/'

# add file name to path
path = f'{input_path}dtmf_signal.wav'

# call helper functions for signal generation
audio_buffer = tg.generate_audio_sequence(input_number)
bin_buf = tg.buffer_to_bytearray(audio_buffer)

# open the path and write a .wav-file out
out = wave.open(path, 'wb')
out.setnchannels(1) # mono audio
out.setsampwidth(2) # 2 bytes = 16-bit audio
out.setframerate(tg.samplerate) # 44100 Hz
out.writeframes(bin_buf)
out.close()
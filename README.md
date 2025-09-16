# DTMF-signalling
Final project for _Grundlagen des Programmierens_, code for the generation of dual-tone multi-frequency audio signals of given number-based inputs.

## 1. prerequisites
For the program to work, you need the python module `numpy` installed on your computer. To install, type `pip install numpy` into your command line.

## 2. how to use
To start the program you just have to execute the `main.py` by either starting the program without any arguments or adding a telephone number and a designated path, separated by a single space character, to the program call like so:

`python3 main.py <telephone_number> /path/to/file`

If no arguments where given the program asks you to enter them after starting it. Also enter the telephone number and path separated by a single space character like so:

`<telephone_number> /path/to/file`

If everything is correct, the program returns the telephone number to the commandline and writes the file to the given path. If one of the inputs is wrong, an error message is displayed.
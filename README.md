# NES-EZ-COMPRESS
A simple compression script designed for game developers working in Assembly on NES or Gameboy

## Algorithm
The operating compression algorithm is quite simple. Because encoding is finite, unlike most encoding algorithms, this has a limited dicitonary. The idea is simple. compress words, for simplicity. A word with multiplicity m and length l, should save (m-1)(l-1) bytes, since it saves l-1 bytes for each occurence after the first one. Simply take all words, and sort them by that quantity, and use the appropriate number from the top as your dictionary. Then, there's a LUT of some smaller size containing the most frequent words, and then an encoding of all the messages. Then, the program automatically produces assembly code, in the form of .txt files, to assign this lookup table within the encoding, and to load in all the compressed text data. 

## Configuration
All the configuration paramaters for each run can be set in the configs.py module. There are a few assumptions made that aren't configurable, in particular with zero-filling the numbers. If you encounter such a bug and submit an issue, I'll probably fix it, or if you know even a little python, you could probably as well. What is *not* configurable as written is the encoding, at least not yet. Configurable paramaters include

* path to the input file
* directory name of the folder to which outputs write
* an optional paramater to mark each run's output with a timestamp on the saved filenames
* the number of encoding bits used. This will probably be 8, and, in particular, not to waste bit, should almost always be a multiple of 8. Note this is combined for the encoding as well as the dictionary, and the encoding as natively written takes up 6 bytes, with some waste. 
* an option to check the file sizes are not too large. This is actually 2 paramaters. A boolean on whether or not to check for a maximum filesize and a number of kilobytes that may or may not matter depending on the boolean. The code throws an exception if it's too large. 
* a maximum number of bytes to write to a particular file before switching to a new file. This is used for switching between memory banks
* a character to mark the end of each message to be loaded in a different spot in memory.
* a maximum comment line length. The generated assembly code comments raw text for readability, and this controls the line wrapping on comments
* a number of bytes to load in per line, before wrapping to the next line

After setting the configs.py file to your desired configuration, simply run smlr.py, and the desired output will be produced. 

## Dependencies
Just python 3.7+, the program has no non-native python library dependencies. 

## Getting Started
To use this program from scratch, you must first install python, and download the code from this repository onto your computer. 

Once you have python installed, to use the program each time, simply modify configs.py as needed, and then run smlr.py. 

##############################################################################
##############################################################################
##                                                                          ##
##   ________  ________  ________   ________ ___  ________  ________        ##
##  |\   ____\|\   __  \|\   ___  \|\  _____\\  \|\   ____\|\   ____\       ##    
##  \ \  \___|\ \  \|\  \ \  \\ \  \ \  \__/\ \  \ \  \___|\ \  \___|_      ##
##   \ \  \    \ \  \\\  \ \  \\ \  \ \   __\\ \  \ \  \  __\ \_____  \     ##
##    \ \  \____\ \  \\\  \ \  \\ \  \ \  \_| \ \  \ \  \|\  \|____|\  \    ##
##     \ \_______\ \_______\ \__\\ \__\ \__\   \ \__\ \_______\____\_\  \   ##
##      \|_______|\|_______|\|__| \|__|\|__|    \|__|\|_______|\_________\  ##
##                                                            \|_________|  ##
##                                                                          ##
##############################################################################
##############################################################################

#this is a path to the input text file. Make it a full path or include it in
#this directory and just make it the name
input_file_path = 'hi.txt'

#this is the directory in which the outputs will go
output_dir_name = 'outputs'

#if true, each run of the program will generate a unique save marked with 
#the timestamp. If false, they will simply overwrite each other in the global
#file
uses_timestamp = False

#base file name of the output text file
base_output_msg_file = 'msgs'

#base file name of the output LUT file
base_output_LUT_file = 'lut'

#this is the number of bits used for the entire encoding and LUT. Will almost
#always be 8. 
num_encoding_bits = 8

#this has the ability to warn you about data at runtime, in case the output 
#file is too big 
checks_out_filesize = True
max_out_filesize = 1024 #kilobytes

#this is (the max filesize before rolling over to a new character) + 1
byte_counter_max = 16384 

#The char used to denote the end of the string.
end_of_string_char = '.'

#maximum size of a comment line. It will simply hang over after this. 
max_comment_line_length = 100

#max number of data bytes in a single line. 
line_bytes = 8
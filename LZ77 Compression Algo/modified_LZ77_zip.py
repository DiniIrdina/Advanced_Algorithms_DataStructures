# Dini Irdina Ahmad Ubaidah, 31279279
# Credits and References: Tutorial videos, lecture videos and slides, GitHub (https://github.com/wein98/Advanced-Algorithm-Data-Structure/blob/master/LZSS_Data_Compression/encoder_lzss.py)


import sys
from huffman import *
from elias import *
from bitarray import bitarray

def zalgo(string):
    zarray = [0] * len(string)
    zarray[0] = len(string)

    l, r = 0, 0

    i = 1
    while i < len(string):
        remaining = r - i + 1
        k = i - l

        # Case 1: outside box
        if i > r:
            for j in range(i, len(string)):
                if string[j] == string[j-i]:
                    zarray[i] += 1 
                else:
                    break
            l, r = i, i + zarray[i] - 1
        # Case 2: inside box
        else:
            # Case 2a
            if zarray[k] < remaining:
                zarray[i] = zarray[k]
            # Case 2b
            elif zarray[k] > remaining:
                zarray[i] = remaining
            # Case 2c
            elif zarray[k] == remaining:
                matches = 0
                for j in range(r+1, len(string)):
                    if string[j] == string[j - i]:
                        matches += 1
                    else:
                        break
                l, r = i, r + matches
                zarray[i] = r - i + 1
        i += 1

    return zarray


class LZ77Encoder:
    def __init__(self, filename, W, L):
        """LZ77 Encoder class that performs all of the computation required when an object of its class is instantiated."""
        self.filename = filename
        self.string = self.read_file()
        self.window = W 
        self.buffer = L
        self.length = len(self.string)

        self.huffman_obj = Huffman(self.string)     # a huffman object that stores the huffman codes for the string
        self.distinct_chars = []  # [binary of ASCII code, huffman code length , huffman code] * number of distinct char
        self.num_distinct_chars = 0     # number of distinct characters in the input file
        self.char_header()

        self.filename_ascii = None
        self.filename_ASCII_func()  # ASCII of characters in filename (e.g. filename = "AAA", filename_ascii = bitarray('100000100100000101000001') )

        self.fname_length_obj = EliasOmega(len(self.filename))
        self.fname_length_elias = self.fname_length_obj.get_code()   # length of the input filename using Elias coding

        self.file_size_obj = EliasOmega(self.length)
        self.filesize_elias = self.file_size_obj.get_code()  # size of the input file using Elias coding

        self.header = self.encode_header()      # stores all the metadata for the header (in bitarray)

        self.LZ77_data = self.compute_LZ77()    # stores the data part of the file (in bitarray)
        self.LZ77_encoding()

        self.final_bitstring_encoding = bitarray(self.header) + bitarray(self.LZ77_data)    # final bitarray to that contains both header and data
        self.write_file()


    def read_file(self):
        with open(self.filename) as file:
            output = file.read()
        return output

    def encode_header(self):
        """Function that combines all the header data together."""
        
        header = self.fname_length_elias + self.filename_ascii + self.filesize_elias + self.num_distinct_chars
        for i in range(len(self.distinct_chars)):
            header += self.distinct_chars[i][0] + self.distinct_chars[i][1] + self.distinct_chars[i][2]
        return header


    def filename_ASCII_func(self):
        """Function that computes a bitarray of ASCII characters in the filename. Each character in the filename is coded in its fixed-length 8-bit
           ASCII codeword."""
        char = bin(ord(self.filename[0]))
        char = bitarray(char[2:])
        char = self.filling_binary(char)    # pads the bitarray so that it is fixed-length 8-bit
        self.filename_ascii = char

        for i in range(1,len(self.filename)):
            char = bin(ord(self.filename[i]))
            char = bitarray(char[2:])
            char = self.filling_binary(char)
            self.filename_ascii = self.filename_ascii + char
            
    
    def char_header(self):
        """Function to fill up the distinct_char array with the corresponding ASCII code, huffman code length, and huffman code for each unique character."""
        huffman_chars = self.huffman_obj.get_codes()

        for i in range(len(huffman_chars)):
            if huffman_chars[i] != None:
                char = bin(i)
                char = bitarray(char[2:])   # ASCII code for character

                huffman_char_code = huffman_chars[i]    # huffman codeword for character
                huffman_length = EliasOmega(len(huffman_char_code))
                huffman_length = huffman_length.get_code()      # length of huffman codeword

                char = self.filling_binary(char)
                self.distinct_chars.append([char,huffman_length,huffman_char_code])

        num_of_chars = len(self.distinct_chars)
        num_of_chars = EliasOmega(num_of_chars)     # encoding the number of distinct characters using Elias
        self.num_distinct_chars = num_of_chars.get_code()   


    def filling_binary(self, b_code):
        """Function used to pad bitarray to make it 8-bit."""
        add_string = ""
        if len(b_code) < 8:
            difference =  8 - len(b_code)
            for _ in range(difference):
                add_string += "0"
            return bitarray(add_string) + b_code
        else:
            return b_code


    def LZ77_offset_length(self, buffer_start):
        """Function used to calculate the offset and length for an LZ77 tuple. The input it accepts is the position of the start of the buffer (character to start from).
           It uses Z Algorithm to check for the longest matching suffix in the window that matches the substring in the buffer."""
        window_start = buffer_start - self.window
        buffer_end = buffer_start + self.buffer
        window_size = self.window
        
        if window_start <= 0:   # Adjusts the window size if the number of characters are not enough to fill it
            window_start = 0
            window_size = buffer_start

        if buffer_end >= self.length:   # Adjusts the buffer end to end of string if it goes outside of its bounds
            buffer_end = self.length - 1

        buffer_size = buffer_end - buffer_start

        if window_size == 0:
            window_size = 1

        if window_size > self.window:
            window_size = self.window

        txt_portion = self.string[buffer_start:buffer_end] + "$" + self.string[window_start:buffer_end]     # The buffer is on the left side of the $, and we do string[window_start:buffer_end] 
                                                                                                            # to account for overlapping

        z_array = zalgo(txt_portion)   

        length = 0
        offset = 0

        for x in range(self.buffer, buffer_size+window_size+1):
            if z_array[x] == 0:
                continue

            if z_array[x] > length:
                length = z_array[x]
                offset = window_size - (x - buffer_size-1)

            elif z_array[x] == length:
                offset = window_size - (x - buffer_size - 1)
        
        return offset, length

    def compute_LZ77(self):
        """Computes the LZ77 tuples for the entire file's contents and appends them to a list to make it easier for encoding later."""
        pointer = 0

        result = [[0,0,ord(self.string[0])]]
        pointer += 1
        while pointer < self.length:
            offset, length = self.LZ77_offset_length(pointer)
            if length == 0:
                char = self.string[pointer]
                pointer += 1
            else:
                pointer += length + 1
                char = self.string[pointer-1]
            char = self.string[pointer-1]
            
            result.append([offset,length, ord(char)])
        return result

    def LZ77_encoding(self):
        """Function encodes the LZ77 tuples and combines all of them into one bitarray."""

        for i in range(len(self.LZ77_data)):
            offset_elias = EliasOmega(self.LZ77_data[i][0])
            offset_elias = offset_elias.get_code()

            length_elias = EliasOmega(self.LZ77_data[i][1])
            length_elias = length_elias.get_code()

            char_position = self.LZ77_data[i][2]
            char_huffman = self.huffman_obj.get_codes()
            char_huffman = char_huffman[char_position]
            
            self.LZ77_data[i][0] = offset_elias
            self.LZ77_data[i][1] = length_elias
            self.LZ77_data[i][2] = char_huffman

        combined_encoding = self.LZ77_data[0][0] + self.LZ77_data[0][1] + self.LZ77_data[0][2]

        for i in range(1, len(self.LZ77_data)):
            combined_encoding = combined_encoding + self.LZ77_data[i][0] + self.LZ77_data[i][1] + self.LZ77_data[i][2]
        self.LZ77_data = combined_encoding


    def write_file(self):
        remainder = len(self.final_bitstring_encoding) % 8  # check if bits can be packed into bytes (multiple of 8 bits)
        if remainder > 0:
            padding = 8 - remainder
            self.final_bitstring_encoding = self.final_bitstring_encoding + bitarray([0]*padding)
        
        output_file = open(self.filename, "wb") # use wb as mode for writing in binary.
    
        self.final_bitstring_encoding.tofile(output_file)
        output_file.close()


if __name__ == "__main__":
    input_file, W, L = sys.argv[1], sys.argv[2], sys.arg[3]
    output = LZ77Encoder(input_file, W, L)

  
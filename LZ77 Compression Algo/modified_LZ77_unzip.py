# Dini Irdina, 31279279
# Credits and References: Tutorial videos, lecture videos and slides, GitHub (https://github.com/wein98/Advanced-Algorithm-Data-Structure/blob/master/LZSS_Data_Compression/decoder_lzss.py)


import sys
from huffman import *
from elias import *
from bitarray import bitarray
from bitarray.util import ba2int

class LZ77Decoder:
    """Class used to decode a binary file, the input required to create an object of this class is the name of the encoded file."""
    def __init__(self, filename):

        self.filename = filename
        self.bitstream = bitarray()
        self.read_binary_file()

        self.huffman_tree = DecodeTree()
        self.total_bits = len(self.encoded_bits)
        self.current_position = 0   # used as pointer for the bitstream

        ### HEADER DATA ###
        self.header_decoder()

        ### FILE CONTENTS DATA ###
        self.final_data = ""
        self.data_decoder()

        self.write_file()   # outputs the decoded file


    def read_binary_file(self):
        """Function used to convert the binary input file into a bitarray format."""

        file = open(self.filename, "rb")
        byte = file.read(1)

        while byte:
            x = int.from_bytes(byte, byteorder='big')
            self.bitstream += bitarray('{0:08b}'.format(x))
            byte = file.read(1)


    def elias_decoding(self):
        """Function used to decode the Elias Omega encoding, a universal pointer (current_position) is used to travel through
           the bits. Hence, no input is needed for the function to work."""

        code = self.bitstream

        slice_length = 1
        is_number = False

        while is_number == False and self.current_position+slice_length < self.total_bits:
            bits = code[self.current_position:self.current_position + slice_length]
            self.current_position += slice_length

            if bits[0] == 1:
                is_number = True
                return ba2int(bits) - 1

            if len(bits) == 1 and bits[0] == 0:
                slice_length += 1
            elif bits[0] == 0:
                bits[0] = 1
                slice_length = ba2int(bits) + 1


    def header_decoder(self):
        """Function used to decode the header part of the file. It decodes everything including the filename length, filename, file size, number of distinct characters
           and the info for each distinct character [ASCII, huffman length, huffman code]. Also creates the Huffman Tree to be used for decoding the file contents later on."""
        
        self.fname_length = self.elias_decoding()   # decoding length of file name

        next_decode_length = self.fname_length * 8  # * 8 because we know that each ASCII character in the filename is encoded using fixed-length 8-bit.
        self.file_name = self.decode_ASCII(self.bitstream[self.current_position:self.current_position+next_decode_length])  # decoding file name
        self.current_position += next_decode_length
        
        self.file_size = self.elias_decoding()  # decoding file size
        self.num_distinct_chars = self.elias_decoding()  # decoding number of distinct characters
        self.distinct_chars = []

        for _ in range(self.num_distinct_chars):    # acquiring the huffman codes for each ASCII character and inserting them into the Huffman Tree
            current_data = [None, None, None]

            ascii_char = self.decode_ASCII(self.bitstream[self.current_position: self.current_position+8])
            self.current_position += 8
            current_data[0] = ascii_char

            huffman_length = self.elias_decoding()
            current_data[1] = huffman_length

            huffman_code = self.bitstream[self.current_position:self.current_position+huffman_length]
            current_data[2] = huffman_code
            self.current_position += huffman_length

            self.distinct_chars.append(current_data)
            
            self.huffman_tree.insert(ascii_char,huffman_code)


    def decode_ASCII(self, path):
        counter = 0
        temp = ""
        result = ""
        
        while counter <= len(path):

            if counter < len(path):
                bit = path[counter]

            if len(temp) == 8:
                ascii_code = ba2int(bitarray(temp))
                result += chr(ascii_code)
                temp = ""

            temp = temp + str(bit)
            counter += 1
    
        return result

    def data_decoder(self):
        while self.current_position < self.total_bits:
            if len(self.final_data) >= self.file_size:
                break

            offset = self.elias_decoding()
            length = self.elias_decoding()
            char = None
            found_char = False
            current_node = self.huffman_tree.root

            while not found_char and self.current_position < self.total_bits:
                bit = self.bitstream[self.current_position]

                if bit == 0:
                    if not current_node.left:
                        char = current_node.character
                        found_char = True                        
                    else:
                        current_node = current_node.left
                        self.current_position += 1
                else:
                    if not current_node.right:
                        char = current_node.character
                        found_char = True
                    else:
                        current_node = current_node.right
                        self.current_position += 1
            
            if not found_char:
                if bit == 0 and not current_node.is_leaf:
                    current_node = current_node.left
                    char = current_node.character
                elif bit == 1 and not current_node.is_leaf:
                    current_node = current_node.right
                    char = current_node.character
                else:
                    char = current_node.character

            window_start = len(self.final_data) - offset
            for i in range(length):
                self.final_data += self.final_data[window_start+i]

            self.final_data += char

        print(self.final_data)
                        
    def write_file(self):
        my_file = open(self.file_name,"w")
        my_file.write(self.final_data)
        my_file.close()



if __name__ == "__main__":
    # input_file = sys.argv[1]
    output = LZ77Decoder('x.asc.bin')
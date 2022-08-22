# Dini Irdina Ahmad Ubaidah, 31279279
# Credits and References: Tutorial videos, lecture videos and slides, GitHub (https://github.com/wein98/Advanced-Algorithm-Data-Structure/blob/master/LZSS_Data_Compression/EliasCode.py) 

from bitarray import bitarray
from bitarray.util import ba2int

class EliasOmega:
    def __init__(self, number):
        bin_number = bin(number+1)  # 
        self.elias_code = bitarray(bin_number[2:])
        self.elias_encode(len(self.elias_code))

    def get_code(self):
        return self.elias_code

    def elias_encode(self, length):
        if length == 1:
            return

        # length += 1
        if length > 1:
            current_length = length - 1
            bin_length = bin(current_length)
            bin_array = bitarray(bin_length[2:])
            bin_array[0] = 0
            self.elias_code = bin_array + self.elias_code
            self.elias_encode(len(bin_array))
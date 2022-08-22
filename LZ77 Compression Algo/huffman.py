#Dini Irdina Ahmad Ubaidah, 31279279
# Credits and References: Tutorial videos, lecture videos and slides, Wikipedia, GitHub (https://gist.github.com/jasonrdsouza/1c9c895f43497d15eb2e) (https://github.com/bhrigu123/huffman-coding/blob/master/huffman.py)
# (https://github.com/wein98/Advanced-Algorithm-Data-Structure/blob/master/LZSS_Data_Compression/HuffmanTree.py)

from bitarray import bitarray
from heapq import heapify, heappop, heappush
from importlib.resources import path

class HeapNode:
    def __init__(self, freq, char):
        self.char = char
        self.frequency = freq
        self.left = None
        self.right = None

    def __lt__(self, other):
        if self.frequency < other.frequency:
            return True
        else:
            return False

    def __eq__(self, other):
        if isinstance(other,HeapNode):
            if self.frequency == other.frequency:
                return True
        else:
            return False


class Huffman:
    def __init__(self, string):
        self.string = string
        self.heap =[]
        self.huffman_codes = [None] * 257
        self.huffman_codes = self.huffman_coding()

    def get_codes(self):
        return self.huffman_codes

    def huffman_coding(self):

        self.frequency_list = [None] * 256
        for i in self.string:
            char_num = ord(i)
            if self.frequency_list[char_num] == None:
                self.frequency_list[char_num] = 1
            else:
                self.frequency_list[char_num] += 1

        for i in range(len(self.frequency_list)):
            if self.frequency_list[i] == None:
                continue
            # print(chr(i) + " " + str(self.frequency_list[i]))

        self.heap = []
        heapify(self.heap)

        for i in range(len(self.frequency_list)):
            if self.frequency_list[i] == None:
                continue
            else:
                item = HeapNode(self.frequency_list[i], chr(i))
                heappush(self.heap,item)

        while len(self.heap) > 1:
            first = heappop(self.heap)
            second = heappop(self.heap)

            combined_count = first.frequency + second.frequency
            item = HeapNode(combined_count,  None)
            item.left = first
            item.right = second
            heappush(self.heap,item)
        
        final = heappop(self.heap)
        self.encode_helper(final,"")
        
        return self.huffman_codes

    def encode_helper(self,current,code):
        if not current:
            return
        
        if current.char != None:
            self.huffman_codes[ord(current.char)] = bitarray(code)
            return

        self.encode_helper(current.left, code+"0")
        self.encode_helper(current.right, code+"1")
        return 


class DecodeNode:
    def __init__(self):
        self.character = None        
        self.is_leaf = False
        self.left = None
        self.right = None


class DecodeTree:
    def __init__(self):
        self.root = DecodeNode()

    def insert(self, char, code):
        current = self.root

        for i in range(len(code)):

            bit = code[i]
            if code[i] == 0:
                if current.left is None:
                    current.left = DecodeNode()
                current = current.left
            else:
                if current.right is None:
                    current.right = DecodeNode()
                current = current.right

        current.character = char
        current.is_leaf = True
            

    def get_character(self, huffman):
        current = self.root

        for i in range(len(huffman)):
            if huffman[i] == 0:
                current = current.left
            else:
                current = current.right

        return current.character

    

if __name__ == "__main__":
    my_str = "aaaabbccdeqwertyyyy"
    str2 = "A_DEAD_DAD_CEDED_A_BAD_BABE_A_BEADED_ABACA_BED"

    huffy = Huffman(str2)
    table = huffy.huffman_coding()
    print("Huffman starts here:")
    # print(table)
    for i in range(len(table)):
        if table[i] != None:
            print(i)
            print(chr(i) + ": " + str(table[i]))
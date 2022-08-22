# Dini Irdina Ahmad Ubaidah, 31279279
# Acknowledgement & Credits: Lecture notes, tutorial videos, sanity check session, youtube video (Ben Langmead)

import sys
from audioop import reverse

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

def hamming_distance(pattern, string):
    """Function generates a z array for prefix and another z array for suffix. Then it proceeds to sum the prefixes with the
       corresponding suffixes. This result is calculated with the length of the pattern to determine if the hamming distance
       is <= 1. The function returns a list of tuples with the positions and their hamming distances."""
    results =[]
    if len(pattern) == 0 or len(string) == 0:
        return []

    if len(pattern) == 1:
        for i in range(len(string)):
            if string[i] == pattern:
                results.append((i+1,0))
            else:
                results.append((i+1,1))
        return results

    combined = pattern + "$" + string
    # reversing process to get the z suffix array
    rev_pat = pattern[::-1]
    rev_str = string[::-1]
    rev_combined = rev_pat + "$" + rev_str
    
    prefix_zarray = zalgo(combined)
    suffix_zarray = zalgo(rev_combined)

    end = len(combined) - len(pattern)
    counter = 0
    
    for i in range(len(pattern)+1, end+1):
        j = end - counter
        sum = prefix_zarray[i] + suffix_zarray[j] 
        ham_distance = len(pattern) - sum
        if ham_distance <= 1:
            if ham_distance < 0:   # if the result was a negative number, change it to 0
                ham_distance = 0
            results.append((counter+1, ham_distance))  # counter+1 because the indexing for the final answer starts from 1 and not 0
        counter += 1

    return results


def read_input(text_filename, pat_filename):

    # text file
    txt_file = open(text_filename, "r")
    txt = txt_file.read()
    txt_file.close()

    # pat file
    pat_file = open(pat_filename, "r")
    pat = pat_file.read()
    pat_file.close()

    return txt, pat


def write_output(filename):
    output_file = open("output_hd1_patmatch.txt", "w")
    for i in range(len(filename)):
        output_file.write(str(filename[i][0]) + " " + str(filename[i][1]))
        if i != len(filename)-1:
            output_file.write("\n")
    output_file.close()


if __name__ == "__main__":
    # the filename for the python run
    argument_00 = sys.argv[0]   # Assignment_Run.py
    # the actual argument
    argument_01 = sys.argv[1]   # argument_01 = "text.txt"    
    argument_02 = sys.argv[2]   # argument_02 = "pattern.lo
    txt, pat = read_input(argument_01, argument_02)

    # call function using the arguments from argument_01 to argument_02
    output = hamming_distance(pat, txt)
    write_output(output)